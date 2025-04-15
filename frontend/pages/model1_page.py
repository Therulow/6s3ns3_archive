import dash
from dash import html, dcc, Input, Output, State, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from shared.default_pagelayout import get_default_layout 
from shared.myear_dropdown import myear_dropdown
import requests
import json
import certifi
import os
import plotly.graph_objects as go
from datetime import datetime
os.environ['SSL_CERT_FILE'] = certifi.where()

# Register the Model 1 page
dash.register_page(__name__, path="/Mean", name="Mean")

# Sample data for the graph
# years = [f"{year}Q{q}" for year in range(1950, 2026) for q in range(1, 5)]
# values = [1000 * (1.03 ** (int(year.split('Q')[0]) - 1950)) for year in years]  # Simulated Real GDP growth

# df = pd.DataFrame({"Year": years, "Real GDP": values})

# Content for Model 1 page
model1_content = html.Div(
    id="main-content",
    style={
        "height": "100vh",           # Full height of the viewport    
        "overflowY": "scroll",          # Enable vertical scrolling
        "paddingTop": "25px",         # some space at the top
        "paddingBottom": "200px"        # some space at the bottom
    },     
    children=[
        # Header "Model 1"
        html.H1("Prevailing Mean Benchmark Model", style={"text-align": "center","color": "white", "marginBottom": "20px", "fontWeight": "600"}),

        # Graph Centered
        dcc.Graph(id='model1-graph', style={"text-align": "center", "width": "80%", "margin": "0 auto", "height": "500px"}),

        html.Br(), 

        # Container showing forecast value
        html.Div( children = [
           html.H1(
                    id = 'model1-forecast-title',
                    children = ["GDP Forecast for: "],
                    style={
                    "color": "rgba(206, 203, 203)",
                    "fontWeight": "600",
                    "fontSize": "22px",
                    "fontFamily": "Montserrat, sans-serif",
                    "textAlign": "center"}
            ), 
            html.H2(
                    id = 'model1-forecast', children="", 
                    style={
                    "color": "white",
                    "fontWeight": "600",
                    "fontSize": "18px",
                    "fontFamily": "Montserrat, sans-serif",
                    "textAlign": "center"
                }

            )
        ], 
         style={
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",    
            "justifyContent": "center",  
            "width": "100%",
        }
        ),
        
        html.Br(),

        # Dropdowns for year and month
        html.Div([
            myear_dropdown()
        ], style={"display": "flex", "justifyContent": "center", "alignItems": "center"}),

        # Add notification for invalid date
        html.Div( children = [
            dbc.Toast(
            id='error1',
            header="Error",
            is_open=False,
            duration=4000,  
            dismissable=True,
            style={
                "position": "relative",
                "zIndex": 1000,
                "backgroundColor": "rgba(255, 0, 0, 0.8)",
                "color": "white"
            }
        )
        ], 
        style={
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
            "width": "100%",
            "paddingTop": "20px",
        }
        ),
        
        html.Br(),

        # Model Description
        html.H2("Model Description", style={"text-align": "center", "color": "white", "marginTop": "30px", 
                                            "fontWeight": '600'}),

        html.P("This model takes the prevailing arithmetic mean of GDP for all past quarters and that would be the prediction for GDP in the next quarter. \
               We can see that the predictions tend to fall above the real values in evaluation test data, likely due to the fact GDP growth figures are greater \
               in periods of growth during the industrial revolution as compared to more steady growth in the 2000s. One main con of this model would be the inability to predict recessions as they are few and far between.",
        style={"color": "lightgrey", "width": "80%", "margin": "0 auto"}
        )
    ]
)

# Wrap the entire page content in a loading indicator
loading_content = html.Div(
    dcc.Loading(
        id="page-loading",
        type="circle",  
        children=model1_content, 
        style={
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
            "height": "100vh" 
        }

    )
)


# Plug that content into your default layout
layout = get_default_layout(main_content=loading_content)
api_url = 'http://127.0.0.1:5000/'
deployment_url2 = 'https://sixs3ns3-backend-test.onrender.com/' 

# Callback to update the graph
@dash.callback(
    Output('model1-graph', 'figure'),
    Output('model1-forecast', 'children'),
    Output('model1-forecast', 'style'),
    Output('model1-forecast-title', 'children'),
    Output('error1', 'children'),
    Output('error1', 'is_open'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)

def update_graph(year, month):
    # Get current date
    current = datetime.now()
    current_year = current.year
    current_month_abbr = current.strftime("%b")

    # Convert selected values from dropdown
    selected_year_int = int(year)
    selected_month_int = datetime.strptime(month, "%b").month
    current_month_int = datetime.strptime(current_month_abbr, "%b").month

    base_style = {
        "color": "grey",
        "fontWeight": "600",
        "fontSize": "28px",
        "fontFamily": "Montserrat, sans-serif"
    }

    # If selected date is in the future
    if selected_year_int > current_year or (selected_year_int == current_year and selected_month_int > current_month_int):
        error_toast_msg = f"⚠ Please select a date on or before {current_month_abbr} {current_year}."
        forecast_title = "Forecast Unavailable"
        # Return exactly 6 outputs:
        # (graph figure, forecast children, forecast style, forecast title, error message, error is_open)
        return (
            dash.no_update,     # graph figure (or could be an empty figure)
            "-",                # forecast children
            base_style,         # forecast style
            forecast_title,     # forecast title
            error_toast_msg,    # error toast children
            True                # error toast is_open
        )

    # If valid date, fetch data from backend
    response = requests.post(
        f"{deployment_url2}/mean_model_prediction",
        headers={'Content-Type': 'application/json'},
        data=json.dumps({"year": year, "month": month})
    )
    data = response.json()
    data = pd.DataFrame.from_dict(data).reset_index().rename(columns={"index": "Quarter"})
    data = data[data["Quarter"].str[:4].astype(int) >= 2000]

    value = round(data["Predicted GDP"].iloc[-1], 3)
    if value < 0:
        forecast_style = {**base_style, "color": "red"}
    elif value > 0:
        forecast_style = {**base_style, "color": "rgb(0, 200, 83)"}
    else:
        forecast_style = {**base_style, "color": "white"}
    
    forecast_value = f"{value:.3f}%"

    fig = px.line(data, x="Quarter", y="Predicted GDP",
                  title="Forecast GDP Growth Rate",
                  labels={"Predicted GDP": "GDP Growth Rate (%)", "Quarter": "Year"},
                  template="plotly_dark")
    fig.data[0].name = "Predicted GDP"
    fig.data[0].showlegend = True

    fig.add_trace(go.Scatter(
        x=data["Quarter"],
        y=data["Actual GDP"],
        mode="lines",
        name="Actual GDP",
        line=dict(color="orange")
    ))

    fig.update_layout(
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=50, b=50),
        title={
            "text": f"GDP Growth Rate up till {month} {year}",
            "font": {"color": "grey", "family": "Montserrat, sans-serif"}
        }
    )

    forecast_title = f"Forecast for {data['Quarter'].iloc[-1]}"

    # Return exactly 6 outputs in the valid branch:
    return (
        fig,             # model1-graph.figure
        forecast_value,  # model1-forecast.children
        forecast_style,  # model1-forecast.style
        forecast_title,  # model1-forecast-title.children
        "",              # error1.children (no error)
        False            # error1.is_open (closed)
    )


