# AI Restaurant Recommender - Milestone 1

An AI-powered restaurant recommendation system organized into a clean, phase-based structure.

## Project Structure

```text
src/
  milestone_1/
    phase_0_setup/       # Configuration and utilities
    phase_1_ingestion/   # Data loading and preprocessing
    phase_2_preferences/ # User preference schemas and parsing
    phase_3_candidates/  # Filtering and candidate selection
    phase_4_llm/         # LLM prompt building and ranking
    phase_5_output/      # Formatting and presentation
    phase_6_api/         # FastAPI endpoints and service layer
    pipeline/            # End-to-end orchestrator
    cli.py               # Interactive CLI
    main.py              # API entry point
```

## Quick Start

### 1. Setup Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set API Keys
Create a `.env` file in the root directory:
```env
M1_GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run the CLI
```bash
$env:PYTHONPATH="src"
python src/milestone_1/cli.py
```

### 4. Run the API
```bash
$env:PYTHONPATH="src"
python src/milestone_1/main.py
```

## Running Tests
```bash
python test_e2e_api.py
```
