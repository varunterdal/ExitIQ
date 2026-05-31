import pandas as pd
import json
import os

# Base path for data files
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def load_theme_results():
    return pd.read_csv(os.path.join(DATA_PATH, 'theme_results.csv'))

def load_sentiment_results():
    return pd.read_csv(os.path.join(DATA_PATH, 'sentiment_results.csv'))

def load_attrition_results():
    return pd.read_csv(os.path.join(DATA_PATH, 'attrition_results.csv'))

def load_risk_results():
    return pd.read_csv(os.path.join(DATA_PATH, 'risk_results.csv'))

def load_executive_insights():
    with open(os.path.join(DATA_PATH, 'executive_insights.json'), 'r') as f:
        return json.load(f)

def load_all():
    return {
        'themes':    load_theme_results(),
        'sentiment': load_sentiment_results(),
        'attrition': load_attrition_results(),
        'risk':      load_risk_results(),
        'insights':  load_executive_insights()
    }