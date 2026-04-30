## Problem statement: AI‑powered restaurant recommendation system (Zomato use case)

Build a restaurant recommendation application inspired by Zomato. The system should use **structured restaurant data** plus a **Large Language Model (LLM)** to generate **personalized, human‑readable recommendations** based on user preferences.

## Objective
Design and implement an application that:
- **Accepts user preferences** (e.g., location, budget, cuisine, rating threshold, and other constraints)
- **Uses a real-world restaurant dataset** as the source of candidates
- **Combines filtering + LLM reasoning** to rank and explain recommendations
- **Presents results clearly** in a user-friendly format

## Data source
- **Dataset**: Hugging Face — `ManikaSaini/zomato-restaurant-recommendation`  
  Link: `https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation`

## Inputs (user preferences)
Collect the following from the user (at minimum):
- **Location** (e.g., Delhi, Bangalore)
- **Budget** (e.g., low / medium / high, or a numeric range)
- **Cuisine** (e.g., Italian, Chinese)
- **Minimum rating**
- **Additional preferences** (optional): family-friendly, quick service, outdoor seating, etc.

## Expected workflow (high-level)
1. **Data ingestion & preprocessing**
   - Load and preprocess the dataset.
   - Extract relevant fields (as available), such as **restaurant name**, **location**, **cuisine**, **cost**, **rating**, and other metadata needed for filtering and display.

2. **Candidate selection (structured filtering)**
   - Filter restaurants using the user’s constraints (location, budget, cuisine, rating, etc.).
   - Prepare a compact structured summary of the top candidates for the LLM (to control token usage and keep prompts focused).

3. **LLM integration (ranking + explanation)**
   - Construct a prompt that provides:
     - The user’s preferences
     - The structured candidate list
     - Clear instructions for ranking and justifying choices
   - Use the LLM to **rank** the candidates and generate **short explanations** for why each recommendation matches.

4. **Results presentation**
   - Display the top recommendations with the key attributes and the LLM explanation.

## Output requirements
For each recommended restaurant, display:
- **Restaurant name**
- **Cuisine**
- **Rating**
- **Estimated cost / price category**
- **AI-generated explanation** (1–3 sentences, preference-aware)

## Success criteria
The solution is considered complete when it can:
- Take user preferences as input
- Retrieve and filter relevant restaurants from the dataset
- Produce a ranked list of recommendations using an LLM
- Show results in a readable format with consistent fields and clear explanations
