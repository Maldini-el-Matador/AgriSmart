"""
AgriSmart - AI Integrated Farming System (IFS) Dashboard
A Streamlit application for smallholder farmers to detect crop diseases,
assess climate risk, and receive IFS recommendations.
"""

import streamlit as st
import pandas as pd
import hashlib
import random
import time
from datetime import datetime

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="AgriSmart - IFS Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS INJECTION
# =====================================================
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #222429;
    }
    
    .stApp {
        background-color: #222429;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 100%);
        padding: 1rem;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    /* Card Styling */
    .card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
        border: 1px solid rgba(46, 125, 50, 0.1);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
        color: #2E7D32;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Upload Zone Styling */
    .upload-zone {
        background: linear-gradient(135deg, rgba(46, 125, 50, 0.08) 0%, rgba(76, 175, 80, 0.12) 100%);
        border: 2px dashed #2E7D32;
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-zone:hover {
        background: linear-gradient(135deg, rgba(46, 125, 50, 0.12) 0%, rgba(76, 175, 80, 0.18) 100%);
        border-color: #1B5E20;
    }
    
    .upload-icon {
        font-size: 3rem;
        color: #2E7D32;
        margin-bottom: 1rem;
    }
    
    .upload-text {
        color: #2E7D32;
        font-weight: 500;
        font-size: 1.1rem;
    }
    
    .upload-subtext {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Status Badges */
    .status-healthy {
        background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #FF9800 0%, #FFB74D 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-danger {
        background: linear-gradient(135deg, #f44336 0%, #e57373 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #2E7D32;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2E7D32;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #666;
        margin-top: 0.3rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.4);
    }
    
    /* Selectbox Styling */
    .stSelectbox > div > div {
        border-radius: 10px;
        border-color: #E0E0E0;
    }
    
    /* Tables */
    .dataframe {
        border-radius: 10px !important;
        overflow: hidden;
    }
    
    /* AI Insights */
    .ai-insight {
        background: linear-gradient(135deg, rgba(46, 125, 50, 0.05) 0%, rgba(76, 175, 80, 0.08) 100%);
        border-left: 4px solid #2E7D32;
        padding: 1rem;
        border-radius: 0 10px 10px 0;
        margin: 0.5rem 0;
    }
    
    /* Blockchain Badge */
    .blockchain-badge {
        background: linear-gradient(135deg, #1565C0 0%, #42A5F5 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        word-break: break-all;
    }
    
    /* Nav Items */
    .nav-item {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.8rem 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .nav-item:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    .nav-item.active {
        background: rgba(255, 255, 255, 0.25);
        border-left: 3px solid white;
    }
    
    /* Header Title */
    .main-title {
        color: #1B5E20;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        color: #666;
        font-size: 1rem;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Confidence Meter */
    .confidence-meter {
        background: #E8F5E9;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
    }
    
    .confidence-bar {
        background: linear-gradient(90deg, #2E7D32 0%, #4CAF50 100%);
        height: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)


# =====================================================
# DATA DICTIONARIES
# =====================================================

IFS_RECOMMENDATIONS = {
    "High Altitude Cold Desert": {
        "livestock": "Sheep, goats, rabbits, yak",
        "crops": "Millets, wheat, barley",
        "systems": "Pastures, forestry",
        "description": "Focus on hardy livestock and cold-resistant grains. Integration of pasture-based grazing with small grain cultivation provides year-round income stability."
    },
    "Arid/Desert": {
        "livestock": "Camels, sheep, goats",
        "crops": "Pearl millet, pulses, oilseeds",
        "systems": "Animal husbandry focus",
        "description": "Prioritize drought-tolerant crops and desert-adapted livestock. Water-efficient farming with emphasis on animal products for income diversification."
    },
    "Western/Central Himalayas": {
        "livestock": "Poultry, sheep, goats, yak",
        "crops": "Maize, wheat, rice",
        "systems": "Horticulture integration",
        "description": "Combine terrace farming with orchard cultivation. Livestock provides manure for organic farming while fruit trees offer additional income."
    },
    "Indo-Gangetic Plains": {
        "livestock": "Dairy cattle (primary)",
        "crops": "Rice, maize, wheat, mustard",
        "systems": "Intensive cropping + Dairy",
        "description": "Leverage fertile alluvial soil for intensive multi-crop rotation. Dairy integration maximizes farm productivity and ensures steady cash flow."
    },
    "Central/Southern Highlands": {
        "livestock": "Dairy cattle, sheep, goat, poultry",
        "crops": "Millets, pulses, cotton",
        "systems": "Dryland farming systems",
        "description": "Mixed farming approach with drought-resistant crops and diverse livestock. Cotton provides cash crop income while millets ensure food security."
    },
    "Western Ghats": {
        "livestock": "Cattle, sheep, goats",
        "crops": "Plantation crops, rice, pulses",
        "systems": "Agroforestry + Plantation",
        "description": "Integrate plantation crops (coffee, tea, spices) with food crops. Multi-tier cropping maximizes land use in high-rainfall areas."
    },
    "Delta/Coastal Plains": {
        "livestock": "Fish, poultry (integrated)",
        "crops": "Rice, pulses",
        "systems": "Rice-fish integration",
        "description": "Utilize waterlogged conditions for rice-fish farming. Aquaculture provides high-value protein while rice remains the staple crop."
    }
}

SOIL_TYPES = ["Alluvial", "Black Cotton", "Red Laterite", "Desert Sandy", "Mountain Forest", "Coastal Saline"]
CROPS = ["Rice", "Wheat", "Maize", "Cotton", "Sugarcane", "Pulses", "Millets", "Vegetables"]
STATUS_OPTIONS = ["All", "Active", "Needs Attention", "Critical"]

DISEASE_RESULTS = [
    {"status": "Healthy", "class": "status-healthy", "message": "Your crop appears healthy with no visible signs of disease or nutrient deficiency."},
    {"status": "Early Blight (Risk)", "class": "status-warning", "message": "Detected early signs of fungal blight. Recommend immediate fungicide application and improved drainage."},
    {"status": "Nitrogen Deficiency", "class": "status-danger", "message": "Yellowing patterns indicate nitrogen deficiency. Apply urea or organic nitrogen supplements immediately."}
]


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def get_ifs_recommendation(region: str) -> dict:
    """Returns IFS recommendation based on the agro-climatic region."""
    return IFS_RECOMMENDATIONS.get(region, {
        "livestock": "General livestock",
        "crops": "Regional crops",
        "systems": "Mixed farming",
        "description": "Please select a specific region for tailored recommendations."
    })


def simulate_blockchain_hash(data: str) -> str:
    """Generates SHA-256 hash for blockchain simulation."""
    timestamp = datetime.now().isoformat()
    combined_data = f"{data}|{timestamp}"
    return hashlib.sha256(combined_data.encode()).hexdigest()


def verify_data_on_chain(data: str) -> dict:
    """Simulates blockchain verification for insurance proof."""
    tx_hash = simulate_blockchain_hash(data)
    return {
        "network": "Polygon Testnet (Mumbai)",
        "tx_hash": tx_hash,
        "status": "Verified",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    }


def get_dummy_weather() -> dict:
    """Returns simulated weather data."""
    return {
        "temperature": random.randint(25, 38),
        "humidity": random.randint(40, 85),
        "rainfall": random.randint(0, 50),
        "wind_speed": random.randint(5, 25),
        "conditions": random.choice(["Sunny", "Partly Cloudy", "Cloudy", "Light Rain"])
    }


def get_nutrient_data() -> pd.DataFrame:
    """Returns simulated soil nutrient data."""
    return pd.DataFrame({
        "Nutrient": ["Nitrogen (N)", "Phosphorus (P)", "Potassium (K)", "pH Level", "Organic Carbon", "Zinc"],
        "Current Level": [random.randint(180, 280), random.randint(15, 45), random.randint(150, 250), 
                         round(random.uniform(5.5, 8.0), 1), round(random.uniform(0.3, 0.8), 2), round(random.uniform(0.4, 1.2), 1)],
        "Optimal Range": ["250-300 kg/ha", "25-35 kg/ha", "200-280 kg/ha", "6.0-7.5", "0.5-0.75%", "0.6-1.0 ppm"],
        "Status": ["⚠️ Low", "✅ Optimal", "✅ Optimal", "✅ Optimal", "⚠️ Low", "✅ Optimal"]
    })


def simulate_disease_detection():
    """Simulates AI disease detection with random results."""
    return random.choice(DISEASE_RESULTS), random.randint(89, 98)


# =====================================================
# SIDEBAR CONSTRUCTION
# =====================================================

with st.sidebar:
    # App Logo & Name
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0 2rem 0;">
            <div style="font-size: 3rem;">🌾</div>
            <h1 style="margin: 0.5rem 0 0 0; font-size: 1.5rem;">AgriSmart</h1>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.85rem; margin-top: 0.3rem;">IFS Dashboard</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.markdown("""
        <div class="nav-item active">
            <span>🏠</span>
            <span>Home</span>
        </div>
        <div class="nav-item">
            <span>📊</span>
            <span>Database</span>
        </div>
        <div class="nav-item">
            <span>📋</span>
            <span>Reports</span>
        </div>
        <div class="nav-item">
            <span>⚙️</span>
            <span>Settings</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Weather Widget
    st.markdown("### 🌤️ Local Weather")
    weather = get_dummy_weather()
    st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); border-radius: 12px; padding: 1rem; margin-top: 0.5rem;">
            <div style="font-size: 2rem; text-align: center;">{weather['temperature']}°C</div>
            <div style="text-align: center; color: rgba(255,255,255,0.8);">{weather['conditions']}</div>
            <div style="margin-top: 1rem; font-size: 0.8rem;">
                <div>💧 Humidity: {weather['humidity']}%</div>
                <div>🌧️ Rainfall: {weather['rainfall']}mm</div>
                <div>💨 Wind: {weather['wind_speed']} km/h</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # User Profile
    st.markdown("""
        <div style="position: fixed; bottom: 1rem; display: flex; align-items: center; gap: 0.8rem; padding: 0.8rem; background: rgba(255,255,255,0.1); border-radius: 12px;">
            <div style="width: 40px; height: 40px; background: #4CAF50; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem;">👨‍🌾</div>
            <div>
                <div style="font-weight: 600;">Farmer User</div>
                <div style="font-size: 0.75rem; color: rgba(255,255,255,0.7);">Premium Plan</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


# =====================================================
# MAIN CONTENT AREA
# =====================================================

# Header
st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 class="main-title">🌱 Soil Health & Disease Analysis</h1>
        <p class="sub-title">AI-powered insights for sustainable farming • Integrated Farming System Recommendations</p>
    </div>
""", unsafe_allow_html=True)

# Filter Row
st.markdown("### 🎛️ Analysis Filters")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    region = st.selectbox("🗺️ Region (Climatic Zone)", list(IFS_RECOMMENDATIONS.keys()))
with col2:
    soil_type = st.selectbox("🏔️ Soil Type", SOIL_TYPES)
with col3:
    crop = st.selectbox("🌿 Crop", CROPS)
with col4:
    date_range = st.selectbox("📅 Date Range", ["Last 7 Days", "Last 30 Days", "Last 90 Days", "This Year"])
with col5:
    status = st.selectbox("📊 Status", STATUS_OPTIONS)


# Upload Zone
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
    <div class="upload-zone">
        <div class="upload-icon">☁️📤</div>
        <div class="upload-text">Drag & Drop or Click to Upload</div>
        <div class="upload-subtext">Soil Report (PDF/CSV) or Crop Image (JPG/PNG)</div>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png", "pdf", "csv"], label_visibility="collapsed")


# =====================================================
# RESULTS CONTAINER (Shows after upload)
# =====================================================

if uploaded_file is not None:
    st.markdown("---")
    
    # Scanning Animation
    with st.spinner("🔬 AI is analyzing your upload..."):
        time.sleep(2)  # Simulate processing
    
    st.success("✅ Analysis Complete!")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Results Grid
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        # Uploaded Image Display (if image)
        if uploaded_file.type.startswith('image'):
            st.markdown("#### 📷 Uploaded Crop Image")
            st.image(uploaded_file, use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Disease Detection Results
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">✨ AI Disease Detection Results</div>', unsafe_allow_html=True)
        
        disease_result, confidence = simulate_disease_detection()
        
        st.markdown(f"""
            <div style="margin-bottom: 1rem;">
                <span class="{disease_result['class']}">{disease_result['status']}</span>
            </div>
            <div class="ai-insight">
                <strong>🤖 AI Insight:</strong> {disease_result['message']}
            </div>
            <div class="confidence-meter">
                <div style="bacground:transparent;display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span><strong>Confidence Score</strong></span>
                    <span style="color: #7d6f2e; font-weight: 700;">{confidence}%</span>
                </div>
                <div style="background: #7d6f2e; border-radius: 5px; overflow: hidden;">
                    <div class="confidence-bar" style="width: {confidence}%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Nutrient Table
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">🧪 Soil Nutrient Analysis</div>', unsafe_allow_html=True)
        
        nutrient_df = get_nutrient_data()
        st.dataframe(nutrient_df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        # IFS Recommendations
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">🌾 IFS Recommendation</div>', unsafe_allow_html=True)
        
        ifs_rec = get_ifs_recommendation(region)
        
        st.markdown(f"""
            <div style="margin-bottom: 1rem;">
                <strong style="color: #2E7D32;">Region:</strong> {region}
            </div>
            <div class="ai-insight">
                <p><strong>🐄 Recommended Livestock:</strong><br>{ifs_rec['livestock']}</p>
            </div>
            <div class="ai-insight">
                <p><strong>🌾 Recommended Crops:</strong><br>{ifs_rec['crops']}</p>
            </div>
            <div class="ai-insight">
                <p><strong>🔄 Farming Systems:</strong><br>{ifs_rec['systems']}</p>
            </div>
            <div style="padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                <strong>💡 Expert Advice:</strong><br>
                {ifs_rec['description']}
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Action Buttons
        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.button("📞 Contact Expert", use_container_width=True)
        with col_btn2:
            st.button("📥 Download Report", use_container_width=True)
        
        # Climate Risk Alert
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">⚠️ Climate Risk Assessment</div>', unsafe_allow_html=True)
        
        weather = get_dummy_weather()
        risk_level = "Low" if weather['humidity'] < 60 else ("Medium" if weather['humidity'] < 75 else "High")
        risk_color = "#4CAF50" if risk_level == "Low" else ("#FF9800" if risk_level == "Medium" else "#f44336")
        
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <div style="background: {risk_color}; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">
                    {risk_level} Risk
                </div>
                <span>Based on current weather conditions</span>
            </div>
            <div style="font-size: 0.9rem; color: #666;">
                Current conditions: {weather['temperature']}°C, {weather['humidity']}% humidity, {weather['conditions']}
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Blockchain Verification Section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔗 Blockchain Data Verification")
    
    # Prepare data for blockchain
    verification_data = f"Region:{region}|Soil:{soil_type}|Crop:{crop}|Weather:{weather['conditions']}|Temp:{weather['temperature']}C"
    blockchain_result = verify_data_on_chain(verification_data)
    
    st.markdown(f"""
        <div class="blockchain-badge">
            <div style="margin-bottom: 0.8rem;">
                <span style="background: rgba(255,255,255,0.2); padding: 0.3rem 0.6rem; border-radius: 5px; margin-right: 0.5rem;">✓ {blockchain_result['status']}</span>
                <span>on {blockchain_result['network']}</span>
            </div>
            <div style="margin-bottom: 0.5rem;">
                <strong>Transaction Hash:</strong><br>
                0x{blockchain_result['tx_hash'][:32]}...
            </div>
            <div style="font-size: 0.75rem; color: rgba(255,255,255,0.7);">
                Timestamp: {blockchain_result['timestamp']} | Insurance-ready verification
            </div>
        </div>
        <p style="font-size: 0.85rem; color: #666; margin-top: 1rem;">
            🛡️ This verification proves to insurers that weather and soil conditions were accurately recorded at this timestamp.
        </p>
    """, unsafe_allow_html=True)


# =====================================================
# FOOTER
# =====================================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #999; font-size: 0.85rem; padding: 2rem 0; border-top: 1px solid #E0E0E0;">
        <p>🌱 AgriSmart IFS Dashboard v1.0 | Supporting SDG 2: Zero Hunger</p>
        <p>Built for Smallholder Farmers • AI-Powered • Blockchain Verified</p>
    </div>
""", unsafe_allow_html=True)
