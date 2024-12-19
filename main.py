import os
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import json

app = FastAPI(title="Loyalty Financial Model Service")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CostProjection(BaseModel):
    category: str
    year_1: float
    year_2: float
    year_3: float
    description: str
    assumptions: List[str]

class RevenueProjection(BaseModel):
    category: str
    year_1: float
    year_2: float
    year_3: float
    description: str
    assumptions: List[str]

class ROIMetrics(BaseModel):
    payback_period: str
    net_present_value: float
    irr: float
    benefit_cost_ratio: float
    key_assumptions: List[str]

class FinancialModel(BaseModel):
    summary: str
    total_investment: float
    costs: List[CostProjection]
    revenue_uplift: List[RevenueProjection]
    roi_metrics: ROIMetrics
    sensitivity_analysis: List[str]
    risk_factors: List[str]

class PreviousData(BaseModel):
    loyalty_program_design: Optional[str] = None

class CurrentPromptData(BaseModel):
    existing_generated_output: str
    user_feedback: str

class FinancialModelRequest(BaseModel):
    company_name: str
    previous_data: Optional[PreviousData] = None
    current_prompt_data: Optional[CurrentPromptData] = None
    other_input_data: Optional[Dict] = {}

class FinancialModelResponse(BaseModel):
    generated_output: str
    structured_data: Dict

def construct_system_prompt() -> str:
    return """
You are an expert in loyalty program financial modeling and ROI analysis. Create detailed 
financial projections that include implementation costs, revenue uplift, and ROI metrics. Consider:

1. Cost Structure
   - Technology implementation
   - Program administration
   - Rewards and redemption costs
   - Marketing and communication

2. Revenue Impact
   - Increased purchase frequency
   - Higher average transaction value
   - Improved retention rates
   - New customer acquisition

3. ROI Analysis
   - Payback period
   - Net present value
   - Internal rate of return
   - Benefit-cost ratio

Provide your response in two parts:
1. A detailed explanation in natural language
2. A structured JSON object with this exact schema:
{
    "financial_model": {
        "summary": "Brief overview of financial projections",
        "total_investment": 1000000.00,
        "costs": [
            {
                "category": "Technology",
                "year_1": 500000.00,
                "year_2": 100000.00,
                "year_3": 100000.00,
                "description": "Description of costs",
                "assumptions": ["assumption1", "assumption2"]
            }
        ],
        "revenue_uplift": [
            {
                "category": "Increased Frequency",
                "year_1": 200000.00,
                "year_2": 400000.00,
                "year_3": 600000.00,
                "description": "Description of impact",
                "assumptions": ["assumption1", "assumption2"]
            }
        ],
        "roi_metrics": {
            "payback_period": "18 months",
            "net_present_value": 1500000.00,
            "irr": 25.5,
            "benefit_cost_ratio": 2.5,
            "key_assumptions": ["assumption1", "assumption2"]
        },
        "sensitivity_analysis": ["factor1", "factor2"],
        "risk_factors": ["risk1", "risk2"]
    }
}

Separate the two parts with [JSON_START] and [JSON_END] markers.
"""

def construct_user_prompt(
    company_name: str,
    program_design: Optional[str] = None,
    existing_output: Optional[str] = None,
    feedback: Optional[str] = None
) -> str:
    prompt = f"Please create a financial model for {company_name}'s loyalty program."
    
    if program_design:
        prompt += f"\n\nConsider this program design: {program_design}"
    
    if existing_output and feedback:
        prompt += f"""
\n\nPrevious financial model: {existing_output}
\nPlease refine the model based on this feedback: {feedback}
"""
    
    return prompt

def extract_json_from_text(text: str) -> dict:
    try:
        start_marker = "[JSON_START]"
        end_marker = "[JSON_END]"
        json_str = text[text.find(start_marker) + len(start_marker):text.find(end_marker)].strip()
        return json.loads(json_str)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse structured data from response: {str(e)}"
        )

def generate_financial_model(
    company_name: str,
    program_design: Optional[str] = None,
    existing_output: Optional[str] = None,
    feedback: Optional[str] = None
) -> tuple[str, dict]:
    """Generate financial model using OpenAI's API"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": construct_system_prompt()},
                {"role": "user", "content": construct_user_prompt(
                    company_name,
                    program_design,
                    existing_output,
                    feedback
                )}
            ],
            temperature=0.7,
            max_tokens=2500
        )
        
        full_response = response.choices[0].message.content
        analysis = full_response[:full_response.find("[JSON_START]")].strip()
        structured_data = extract_json_from_text(full_response)
        
        return analysis, structured_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate", response_model=FinancialModelResponse)
async def generate_model(request: FinancialModelRequest):
    # Extract data from request
    program_design = None
    if request.previous_data:
        program_design = request.previous_data.loyalty_program_design
    
    existing_output = None
    feedback = None
    if request.current_prompt_data:
        existing_output = request.current_prompt_data.existing_generated_output
        feedback = request.current_prompt_data.user_feedback
    
    # Generate financial model
    generated_text, structured_data = generate_financial_model(
        request.company_name,
        program_design,
        existing_output,
        feedback
    )
    
    return FinancialModelResponse(
        generated_output=generated_text,
        structured_data=structured_data
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)