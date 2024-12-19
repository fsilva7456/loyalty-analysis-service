# Loyalty Financial Model Service

This FastAPI service generates financial models and ROI analysis for loyalty programs using OpenAI's GPT-4 model.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/fsilva7456/loyalty-analysis-service.git
   cd loyalty-analysis-service
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'  # On Windows: set OPENAI_API_KEY=your-api-key-here
   ```

## Running the Service

1. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

2. The service will be available at `http://localhost:8000`

## API Documentation

- API documentation is available at `http://localhost:8000/docs`
- OpenAPI specification is available at `http://localhost:8000/openapi.json`

### Generate Financial Model Endpoint

`POST /generate`

Example request:
```json
{
  "company_name": "Example Corp",
  "previous_data": {
    "loyalty_program_design": "Program design details..."
  },
  "current_prompt_data": {
    "existing_generated_output": "Previous financial model...",
    "user_feedback": "Adjust technology cost assumptions"
  },
  "other_input_data": {}
}
```

Example response:
```json
{
  "generated_output": "Financial Model for Example Corp...\n1. Cost Structure...\n2. Revenue Projections...",
  "structured_data": {
    "financial_model": {
      "summary": "3-year financial projection for loyalty program",
      "total_investment": 1000000.00,
      "costs": [
        {
          "category": "Technology",
          "year_1": 500000.00,
          "year_2": 100000.00,
          "year_3": 100000.00,
          "description": "Initial platform development and ongoing maintenance",
          "assumptions": [
            "Cloud infrastructure costs",
            "Development team size: 5 FTE"
          ]
        }
      ],
      "revenue_uplift": [
        {
          "category": "Increased Frequency",
          "year_1": 200000.00,
          "year_2": 400000.00,
          "year_3": 600000.00,
          "description": "Higher purchase frequency from engaged members",
          "assumptions": [
            "10% increase in visit frequency",
            "Average basket size remains constant"
          ]
        }
      ],
      "roi_metrics": {
        "payback_period": "18 months",
        "net_present_value": 1500000.00,
        "irr": 25.5,
        "benefit_cost_ratio": 2.5,
        "key_assumptions": [
          "Discount rate: 10%",
          "Terminal growth rate: 2%"
        ]
      },
      "sensitivity_analysis": [
        "Member engagement rates",
        "Redemption rates"
      ],
      "risk_factors": [
        "Technology implementation delays",
        "Lower than expected engagement"
      ]
    }
  }
}
```

## Key Features

- Uses OpenAI's GPT-4 model for financial analysis
- Incorporates loyalty program design
- Supports iterative refinement through feedback
- Provides both narrative explanation and structured financial data
- Includes:
  - Detailed cost projections
  - Revenue uplift estimates
  - ROI metrics
  - Sensitivity analysis
  - Risk assessment

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)