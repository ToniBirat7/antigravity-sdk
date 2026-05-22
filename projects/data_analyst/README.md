# Data Analyst Agent

A practical agent that helps analyze CSV files, generate insights, and create visualizations.

## What It Does

- **Explores data**: Reads CSV files and summarizes their structure
- **Generates insights**: Uses Gemini to identify patterns and anomalies
- **Creates reports**: Produces summary statistics and recommendations
- **Multi-turn workflow**: Maintains context across analysis steps

## Setup

1. Place sample CSV files in the `data/` directory
2. Run: `python main.py`

## Example Usage

```bash
python main.py
```

The agent will:
1. Ask what data file to analyze
2. Load and explore the data
3. Generate statistical insights
4. Suggest visualizations
5. Answer follow-up questions

## Sample Data

Create `data/sample.csv`:
```csv
product,sales,region,quarter
Laptop,15000,North,Q1
Laptop,16500,North,Q2
Mouse,2300,East,Q1
Mouse,2150,East,Q2
Monitor,8900,South,Q1
Monitor,9200,South,Q2
```

Then run the agent to analyze it.
