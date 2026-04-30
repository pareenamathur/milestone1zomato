import streamlit as st
import pandas as pd
from src.milestone_1.phase_2_preferences.schema import UserPreferences, BudgetPreference
from src.milestone_1.phase_6_api.service import run_recommendation_pipeline, get_all_restaurants

# Page Config
st.set_page_config(page_title="Gourmet AI - Restaurant Recommender", page_icon="🍴", layout="wide")

# Custom CSS for Premium Feel
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #e2e8f0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #7c3aed;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #6d28d9;
        border: none;
    }
    .restaurant-card {
        padding: 1.5rem;
        border-radius: 15px;
        background-color: #1e293b;
        border: 1px solid #334155;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    h3 { color: #f8fafc !important; }
    p { color: #94a3b8 !important; }
    b { color: #fbbf24 !important; }
    i { color: #cbd5e1 !important; }
    </style>
""", unsafe_allow_html=True)

# Cache the dataset loading
@st.cache_data
def load_data():
    return get_all_restaurants()

# Main UI
st.title("🍴 Gourmet AI")
st.markdown("#### Discover your next favorite meal in Bangalore with intelligent recommendations.")

# Sidebar for Preferences
with st.sidebar:
    st.header("Search Preferences")
    location = st.text_input("Location", value="Bellandur", help="e.g. BTM, Indiranagar, Bellandur")
    cuisines = st.text_input("Cuisines", value="Italian, Indian", help="Comma-separated list")
    
    st.divider()
    budget_mode = st.radio("Budget Mode", ["Category", "Range"])
    if budget_mode == "Category":
        budget_cat = st.selectbox("Budget Category", ["low", "medium", "high"], index=1)
        budget = BudgetPreference(mode="category", category=budget_cat)
    else:
        min_cost = st.number_input("Min Cost", value=200, step=100)
        max_cost = st.number_input("Max Cost", value=2000, step=100)
        budget = BudgetPreference(mode="range", min_cost=min_cost, max_cost=max_cost)
        
    st.divider()
    rating_range = st.slider("Rating Range", 0.0, 5.0, (3.5, 5.0))
    
    st.divider()
    extra_prefs = st.text_area("Additional Preferences", placeholder="e.g. outdoor seating, romantic vibe")

    search_btn = st.button("Generate Recommendations")

# Execution
if search_btn:
    with st.spinner("AI is curating your perfect meal..."):
        try:
            # Construct Preferences object
            prefs = UserPreferences(
                location=location,
                budget=budget,
                cuisines=[c.strip() for c in cuisines.split(",") if c.strip()],
                min_rating=rating_range[0],
                max_rating=rating_range[1],
                extra_preferences=[p.strip() for p in extra_prefs.split(",") if p.strip()]
            )
            
            # Run Pipeline
            recs = run_recommendation_pipeline(prefs)
            
            if recs:
                st.success(f"Found {len(recs)} amazing places for you!")
                
                for rec in recs:
                    st.markdown(f"""
                        <div class="restaurant-card">
                            <h3>#{rec.rank} {rec.restaurant_name}</h3>
                            <p>⭐ <b>{rec.rating if rec.rating else 'N/A'}</b> | 💰 ₹{rec.estimated_cost if rec.estimated_cost else 'N/A'}</p>
                            <p><i>"{rec.explanation}"</i></p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No restaurants matched your criteria. Try widening your search!")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
else:
    # Landing page state
    col1, col2 = st.columns(2)
    with col1:
        st.info("👈 Fill out the sidebar to get started.")
    with col2:
        all_data = load_data()
        st.metric("Total Restaurants Indexed", len(all_data))
