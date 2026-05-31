def load_css():
    return """
    <style>

    /* ==================================================
       GLOBAL THEME
    ================================================== */

    .stApp {
        background-color: #0A0A0A;
        color: #FFFFFF;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* ==================================================
       SIDEBAR
    ================================================== */

    [data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #2A2A2A;
    }

    [data-testid="stSidebar"] * {
        color: #E5E7EB !important;
    }

    /* ==================================================
       HEADINGS
    ================================================== */

    h1 {
        color: #FFFFFF !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
        margin-bottom: 0.5rem !important;
    }

    h2 {
        color: #F5F5F5 !important;
        font-weight: 700 !important;
        margin-top: 1rem !important;
    }

    h3 {
        color: #E5E7EB !important;
        font-weight: 600 !important;
    }

    p, li {
        color: #D1D5DB !important;
    }

    /* ==================================================
       METRIC CARDS
    ================================================== */

    [data-testid="metric-container"] {
        background: #141414;
        border: 1px solid #2A2A2A;
        border-radius: 16px;
        padding: 20px;
        transition: all 0.25s ease;
        box-shadow: 0 2px 12px rgba(0,0,0,0.35);
    }

    [data-testid="metric-container"]:hover {
        border-color: #404040;
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }

    [data-testid="metric-container"] label {
        color: #9CA3AF !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }

    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }

    /* ==================================================
       BUTTONS
    ================================================== */

    .stButton > button {
        background: #FFFFFF !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 0.65rem 1.2rem !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background: #E5E5E5 !important;
        transform: translateY(-2px);
    }

    /* ==================================================
       DOWNLOAD BUTTON
    ================================================== */

    .stDownloadButton > button {
        background: #FFFFFF !important;
        color: #000000 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 0.75rem 1.4rem !important;
    }

    /* ==================================================
       INPUTS
    ================================================== */

    .stTextInput input,
    .stTextArea textarea {
        background-color: #141414 !important;
        color: #FFFFFF !important;
        border: 1px solid #2A2A2A !important;
        border-radius: 10px !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #6B7280 !important;
        box-shadow: none !important;
    }

    /* ==================================================
       SELECT BOXES
    ================================================== */

    .stSelectbox > div > div {
        background-color: #141414 !important;
        border: 1px solid #2A2A2A !important;
        border-radius: 10px !important;
        color: white !important;
    }

    /* ==================================================
       CHAT
    ================================================== */

    [data-testid="stChatMessage"] {
        background: #141414 !important;
        border: 1px solid #2A2A2A !important;
        border-radius: 16px !important;
        padding: 12px !important;
        margin: 8px 0 !important;
    }

    /* ==================================================
       TABLES / DATAFRAMES
    ================================================== */

    [data-testid="stDataFrame"] {
        border: 1px solid #2A2A2A !important;
        border-radius: 14px !important;
        overflow: hidden;
    }

    /* ==================================================
       ALERTS
    ================================================== */

    .stSuccess {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid #3F3F46 !important;
        border-radius: 12px !important;
    }

    .stInfo {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid #52525B !important;
        border-radius: 12px !important;
    }

    .stWarning {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid #737373 !important;
        border-radius: 12px !important;
    }

    .stError {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid #525252 !important;
        border-radius: 12px !important;
    }

    /* ==================================================
       PROGRESS BAR
    ================================================== */

    .stProgress > div > div > div > div {
        background-color: #FFFFFF !important;
    }

    /* ==================================================
       DIVIDERS
    ================================================== */

    hr {
        border-color: #2A2A2A !important;
    }

    /* ==================================================
       CAPTIONS
    ================================================== */

    .stCaption {
        color: #9CA3AF !important;
    }

    /* ==================================================
       CUSTOM EXECUTIVE CARDS
    ================================================== */

    .executive-card {
        background: #141414;
        border: 1px solid #2A2A2A;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 16px;
    }

    .executive-title {
        color: #9CA3AF;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .executive-value {
        color: #FFFFFF;
        font-size: 2rem;
        font-weight: 800;
    }

    </style>
    """