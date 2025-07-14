# AI powered platform to support investment decisions — Data Infrastructure & Analytics
## Problem Statement

Building an AI-powered platform to support investment decisions. A core challenge is enabling users (typically PE analysts) to upload large Excel datasets and instantly derive insights — without needing to manually reprogram analyses in Excel formulas.

However, the data is:
* Highly heterogeneous (Excel with unknown structure)
* Often large (1M+ rows, with expectation of 10M–100M rows in the future)
* Manually transformed and under-documented
* Not yet reliably auditable or explainable
* Difficult to integrate into AI workflows due to missing structure and verifiability

The goal of this challenge is to design and build a first version of an analytical pipeline that addresses:
* File upload and schema inference
* Data normalization and anomaly detection
* A core analysis: Concentration Analysis
* AI-assisted insight generation

# Ideal Architecture (Long-Term Vision)
```            
                     [ Front-End ]
                         ├── Screen 1: Upload Excel/CSV
                         ├── Screen 2: Normalize / Fix columns / Validate
                         └── Screen 3: Run analysis, explore results, AI agent
                          │
        ┌─────────────────▼─────────────────┐
        │             API Gateway           │
        └─────────────────┬─────────────────┘
                          │
      ┌───────────────────┼────────────────────┐
      │                   │                    │
┌─────▼──────┐    ┌───────▼────────┐   ┌───────▼────────┐
│ Ingestion  │    │ Transformation │   │     AI Agent   │
│            │    │ (ETL + Audit)  │   │  (LLM, RAG)    │
└─────┬──────┘    └───────┬────────┘   └───────┬────────┘
      │                   │────────────────────│
      ▼                   ▼                    ▼
 ┌───────────┐       ┌────────────┐       ┌─────────────┐
 │ PostgreSQL│ ◄──── │ Data Store │ ◄──── │  Prompt Logs │
 └───────────┘       └────────────┘       └─────────────┘
```

Key Features:
1) Schema inference & profiling engine
2) Data lineage + auditability layer
3) LLM interaction as a microservice
4) Scalable data backend 

# POC Architecture

For the take-home POC, we simplify the ideal vision:
```
                    [Streamlit App]
                           │
     ┌─────────────────────┼──────────────────────┐
     │                     │                      │
 [ingestion.py]    [concentration_analysis.py]   [insights_engine.py]
     │                     │                      │
     ▼                     ▼                      ▼
[data/raw/]         [data/processed/]         [data/insights/]
```
* All data is handled as local CSV/Excel files
* Logs are stored as JSON or plain text
* LLM container (e.g., Ollama with Mistral) is used via HTTP API

# Development Strategy: Critical First

We adopt a baby-steps strategy with focus on:
* Making the critical path work end-to-end
* Mocking advanced features until the core is stable
* Writing modular, testable components

## Incremental Steps
Step	What we do	What we mock
* [ ] Setup	Create modular structure + Docker	Use dummy for everything
* [ ] Upload & preview	Upload Excel, read with Pandas, show preview	Skip schema inference logic
* [ ] Schema inference	Detect column types, missing data, categories	Use static rules for types
* [ ] Concentration analysis	Aggregate and calculate top 10/20/50% per period	Use one static period (e.g., year)
* [ ] Insight generation	Integrate with Ollama via API	Use static prompt/response
* [ ] Export & audit	Save analysis and logs to CSV/JSON	Skip fancy formatting


# Docker Strategy
* Main container runs the full Streamlit app:
-> app/
--> services/
--> data/ # Saves to

* Second container runs Ollama with Mistral model
Exposes http://localhost:11434
Communicates via REST from main app

## How to use:
### Build container:
```bash
docker-compose build
```
### Run app:
```bash
docker-compose up app
```

### Run tests:
```bash
docker-compose run --rm tests
```

## Project Structure
```
investment_decisions_AI/
├── app/
│   └── streamlit_ui.py
├── services/
│   ├── ingestion.py
│   ├── concentration_analysis.py
│   └── insights_engine.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── logs/
├── tests/
│   ├── test1.py
│   ├── test2.py
│   └── ...
├── requirements.txt
├── Dockerfile
├── docker-compose.yml 
└── README.md
```
