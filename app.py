from flask import Flask, render_template
from pytrends.request import TrendReq
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

app = Flask(__name__)

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# List of keywords to track
KEYWORDS = [
    "AI",
    "Machine Learning",
    "Prompt Engineering",
    "LLM",
    "Large Language Model",
    "ChatGPT",
    "GPT-4",
    "BERT",
    "Transformer",
    "Neural Networks"
]

@app.route('/')
def index():
    # Get trends data
    trends_data = get_trends_data(KEYWORDS)
    
    # Create plot
    fig = create_trends_plot(trends_data)
    
    # Convert plot to HTML
    plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    return render_template('widget.html', plot_html=plot_html)

def get_trends_data(keywords):
    # Set timeframe to last 30 days
    timeframe = f'today 30-d'
    
    # Get interest over time data
    pytrends.build_payload(keywords, timeframe=timeframe)
    interest_over_time_df = pytrends.interest_over_time()
    
    # Clean data
    interest_over_time_df = interest_over_time_df.drop('isPartial', axis=1)
    
    return interest_over_time_df

def create_trends_plot(data):
    fig = go.Figure()
    
    # Add traces for each keyword
    for column in data.columns:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data[column],
            name=column,
            mode='lines',
            line=dict(width=2)
        ))
    
    # Update layout
    fig.update_layout(
        title='AI & ML Trends',
        xaxis_title='Date',
        yaxis_title='Interest Over Time',
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
