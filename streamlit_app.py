import streamlit as st
import pandas as pd
from src.milestone_1.phase_2_preferences.schema import UserPreferences, BudgetPreference
from src.milestone_1.phase_6_api.service import run_recommendation_pipeline, get_all_restaurants

# Page Config
st.set_page_config(page_title="Gourmet AI - Restaurant Recommender", page_icon="🍴", layout="wide")

# Custom CSS for Premium Feel
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    :root {
        --primary: #7c3aed;
        --secondary: #a855f7;
        --bg-dark: #0f172a;
        --card-bg: rgba(30, 41, 59, 0.7);
        --text-main: #e2e8f0;
        --text-dim: #94a3b8;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at top right, #1e1b4b, #0f172a);
        color: var(--text-main);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .stSidebar [data-testid="stMarkdownContainer"] h1 {
        font-size: 1.5rem;
        background: linear-gradient(90deg, #fff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        font-weight: 700;
        border: none;
        padding: 1rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 0.85rem;
        margin-top: 2rem;
    }
    
    .stButton>button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 15px 30px -5px rgba(124, 58, 237, 0.4);
        background: linear-gradient(135deg, #6d28d9 0%, #9333ea 100%);
    }

    /* Cards */
    .restaurant-card {
        padding: 2.5rem;
        border-radius: 28px;
        background: var(--card-bg);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .restaurant-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        opacity: 0.5;
    }
    
    .restaurant-card:hover {
        transform: translateY(-8px);
        background: rgba(30, 41, 59, 0.85);
        border-color: rgba(124, 58, 237, 0.4);
        box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.3);
    }

    .rank-badge {
        background: rgba(124, 58, 237, 0.15);
        color: #c084fc;
        padding: 6px 16px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 800;
        border: 1px solid rgba(124, 58, 237, 0.2);
        display: inline-flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 1.5rem;
    }

    .card-title { 
        color: #ffffff !important; 
        font-size: 1.8rem; 
        font-weight: 700; 
        letter-spacing: -0.5px;
        margin-bottom: 0.75rem;
    }
    
    .card-meta { 
        display: flex;
        gap: 20px;
        margin-bottom: 1.5rem;
    }
    
    .meta-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.95rem;
        font-weight: 600;
    }
    
    .rating-val { color: #fbbf24; }
    .cost-val { color: #34d399; }
    .cuisine-tag {
        font-size: 0.75rem;
        background: rgba(255,255,255,0.05);
        padding: 4px 10px;
        border-radius: 8px;
        color: var(--text-dim);
    }

    .card-explanation { 
        color: #cbd5e1 !important; 
        line-height: 1.7; 
        margin-top: 1.5rem;
        font-size: 1.05rem;
        padding: 1.5rem;
        background: rgba(0,0,0,0.2);
        border-radius: 16px;
        position: relative;
    }
    
    .card-explanation::after {
        content: '“';
        position: absolute;
        top: -10px;
        left: 10px;
        font-size: 3rem;
        color: var(--primary);
        opacity: 0.3;
        font-family: serif;
    }

    /* Input Fields */
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-testid="stSelectbox"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    .stTextInput input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Cache the dataset loading
@st.cache_data
def load_data():
    return get_all_restaurants()

# Main UI
st.title("🍴 Gourmet AI")
st.markdown("##### <span style='color: #94a3b8;'>Intelligent restaurant recommendations powered by AI.</span>", unsafe_allow_html=True)

# Sidebar for Preferences
with st.sidebar:
    st.markdown("### <i class='fas fa-sliders-h'></i> Search Filters", unsafe_allow_html=True)
    location = st.text_input("📍 Location", value="Bellandur", help="e.g. BTM, Indiranagar, Bellandur")
    cuisines = st.text_input("🍲 Cuisines", value="Italian, Indian", help="Comma-separated list")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### <i class='fas fa-wallet'></i> Budget", unsafe_allow_html=True)
    budget_mode = st.radio("Mode", ["Category", "Range"], horizontal=True)
    if budget_mode == "Category":
        budget_cat = st.selectbox("Category", ["low", "medium", "high"], index=1)
        budget = BudgetPreference(mode="category", category=budget_cat)
    else:
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            min_cost = st.number_input("Min (₹)", value=200, step=100)
        with col_b2:
            max_cost = st.number_input("Max (₹)", value=2000, step=100)
        budget = BudgetPreference(mode="range", min_cost=min_cost, max_cost=max_cost)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### <i class='fas fa-star'></i> Rating Range", unsafe_allow_html=True)
    rating_range = st.slider("", 0.0, 5.0, (3.5, 5.0))
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### <i class='fas fa-comment-dots'></i> Vibes", unsafe_allow_html=True)
    extra_prefs = st.text_area("", placeholder="e.g. outdoor seating, romantic vibe, quiet place", label_visibility="collapsed")

    search_btn = st.button("Generate Recommendations")

# Execution
if search_btn:
    with st.spinner("✨ AI is analyzing 51,000+ restaurants..."):
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
                st.balloons()
                st.markdown(f"#### <i class='fas fa-check-circle' style='color: #34d399;'></i> Found {len(recs)} Top Matches", unsafe_allow_html=True)
                
                for rec in recs:
                    st.markdown(f"""
                        <div class="restaurant-card">
                            <div class="rank-badge"><i class="fas fa-crown"></i> RANK #{rec.rank}</div>
                            <div class="card-title">{rec.restaurant_name}</div>
                            <div class="card-meta">
                                <div class="meta-item"><span class="rating-val"><i class="fas fa-star"></i> {rec.rating if rec.rating else 'N/A'}</span></div>
                                <div class="meta-item"><span class="cost-val"><i class="fas fa-tag"></i> ₹{rec.estimated_cost if rec.estimated_cost else 'N/A'}</span></div>
                            </div>
                            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                                {" ".join([f'<span class="cuisine-tag">{c}</span>' for c in rec.cuisines[:4]])}
                            </div>
                            <div class="card-explanation">
                                {rec.explanation}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No restaurants matched your criteria. Try widening your search!")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
else:
    # Landing page state
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("""
            <h2 style='font-weight: 800; font-size: 2.5rem; margin-bottom: 1.5rem;'>
                Your next <span style='color: #7c3aed;'>culinary journey</span> starts here.
            </h2>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px;'>
                <div style='padding: 20px; background: rgba(255,255,255,0.03); border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);'>
                    <i class='fas fa-filter' style='color: #7c3aed; font-size: 1.5rem; margin-bottom: 1rem;'></i>
                    <h5 style='margin-bottom: 0.5rem;'>Smart Filtering</h5>
                    <p style='color: #94a3b8; font-size: 0.85rem;'>Advanced matching across location, budget, and cuisine.</p>
                </div>
                <div style='padding: 20px; background: rgba(255,255,255,0.03); border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);'>
                    <i class='fas fa-brain' style='color: #a855f7; font-size: 1.5rem; margin-bottom: 1rem;'></i>
                    <h5 style='margin-bottom: 0.5rem;'>AI Powered</h5>
                    <p style='color: #94a3b8; font-size: 0.85rem;'>LLM-driven ranking based on your unique 'vibes'.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("👈 Use the sidebar to configure your perfect meal.")
        
    with col2:
        all_data = load_data()
        st.markdown(f"""
            <div style='text-align: center; padding: 40px; background: linear-gradient(135deg, rgba(124, 58, 237, 0.1), rgba(168, 85, 247, 0.1)); border-radius: 30px; border: 1px dashed rgba(124, 58, 237, 0.3);'>
                <h1 style='font-size: 3.5rem; margin-bottom: 0;'>{len(all_data):,}</h1>
                <p style='color: #c084fc; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; font-size: 0.7rem;'>Unique Restaurants Indexed</p>
                <div style='margin-top: 20px; display: flex; justify-content: center; gap: 10px;'>
                    <i class='fab fa-github' style='opacity: 0.5;'></i>
                    <i class='fas fa-database' style='opacity: 0.5;'></i>
                    <i class='fas fa-bolt' style='opacity: 0.5;'></i>
                </div>
            </div>
        """, unsafe_allow_html=True)
