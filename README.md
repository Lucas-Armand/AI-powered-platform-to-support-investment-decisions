# AI powered platform to support investment decisions — Data Infrastructure & Analytics
![Demostration](https://github.com/Lucas-Armand/AI-powered-platform-to-support-investment-decisions/blob/main/use.gif)

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
     │                     │                      │ (async)
 [ingestion.py]    [concentration.py]         [insights.py]
     │                     │                      │
     ▼                     ▼                      ▼
[data/raw/]         [data/processed/]         [data/insights/]
```
* All data is handled as local CSV/Excel files
* Logs are stored as JSON or plain text
* LLM container (e.g., Ollama with Mistral) is used via HTTP API

# Development Strategy: Critical First

I adopt a baby-steps strategy with focus on:
* Making the critical path work end-to-end
* Mocking advanced features until the core is stable
* Writing modular, testable components

## Incremental Steps
Step	What we do	What we mock
* [x] (13/07/2025) Setup	Create modular structure + Docker	Use dummy for everything
* [x] (13/07/2025) Upload & preview	
* [x] (16/07/2025) Upload Excel, read with Pandas, show preview	Skip schema inference logic
* [x] (16/07/2025) Schema inference	Detect column types, missing data, categories	Use static rules for types
* [x] (16/07/2025) Concentration analysis	Aggregate and calculate top 10/20/50% per period	Use one static period (e.g., year)
* [x] (18/07/2025)Insight generation	Integrate with Ollama via API	Use static prompt/response
* [ ] ~~Export & audit	Save analysis and logs to CSV/JSON	Skip fancy formatting~~


# Docker Strategy
* Main container runs the full Streamlit app:
localhost:8501

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
Access the app at: http://localhost:8501

### Run the LLM server

```bash
docker-compose up llm
```
You can query the Ollama server at: http://localhost:11434
It will load the model mistral-local defined in the Modelfile.

### Run tests:
```bash
docker-compose run --rm tests
```

### Clean Up (Optional)

To remove unused images, containers, and volumes:

```bash
docker system prune -a --volumes
```

## Project Structure
```
./
├── docker-compose.yml
├── Dockerfile
├── llm.Dockerfile
├── main.py
├── Modelfile
├── README.md
├── requirements.txt
├── services
│   ├── concentration.py
│   ├── ingestion.py
│   ├── insights.py
│   ├── profiling.py
│   └── __init__.py
├── temp
│   └── suggestions/ # async LLM outputs
└── tests
    ├── assets/
    ├── test_concentration.py
    ├── test_ingestion.py
    ├── test_profiling.py
    ├── test_streamlit.py
    └── test_insights.py


```

# Progress Log
## DAY 1 – Setup & Foundation
 * Defined problem scope and ideal architecture based on the challenge prompt
 * Wrote full README with long-term vs POC architecture and development strategy
 * Created initial folder structure (app/, services/, data/, etc.)
 * Built a minimal working Streamlit UI with 3 navigable screens (Upload, Normalize, Analyze)
 * Integrated Docker with local volume for file persistence
 * Wrote and passed initial Streamlit UI tests using streamlit.testing.v1
        Validated sidebar navigation and default rendering
        Learned limitations of testing file_uploader, switched to session-based assertions
 * Tested logic for upload and UI transitions
 * Started planning ingestion and normalization logic

## DAY 2 – Concentration Analysis & Modularization
 * Refactored codebase to modular architecture (services/ for all business logic)
 * Implemented concentration_pivot function to compute bucket-vs-period analysis
 * Validated logic against the challenge's reference example
 * Developed dynamic column suggestion utility for time, categorical, and numeric axes
 * Added clear docstrings and Pythonic best practices to all service functions
 * Created unit tests for each service function
 * Enabled parameterization of buckets and time granularity for future flexibility
 * Documented progress, prepared for custom period combination and AI on next days

## DAY 3 – LLM Integration & Async Insights
* Added services/insights.py with analyze_columns_with_llm() that:
  * builds a few-shot prompt from df.head(3)
  * calls the Mistral model via Ollama
  * parses JSON output (time/category/numeric columns + optional merge_code)
  * applies merge_code in a lightweight sandbox
*Implemented background thread that generates suggestions immediately after upload and stores them as JSON in temp/suggestions/{file_id}.json.
* Streamlit “Analyze” page now:
  * polls for the suggestion file,
  * shows LLM Suggestion banner and LLM Advice rationale,
  * pre-selects suggested columns in the UI,
  * falls back if the LLM is offline.
  * Wrote a little more pytest test_insights.py plus coverage for fallback mode.
  * Updated README
