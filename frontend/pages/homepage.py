import dash 
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import os
import sys 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from pages.news import df_articles, generate_card_scroll
from shared.default_pagelayout import get_default_layout 
# from integration.model1 import get_forecast, get_forecast_graph, monthyear, get_quarter
from shared.myear_dropdown import myear_dropdown
import json
import requests
from Components.package_imports import *
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set working directory to current file location
os.chdir(os.path.dirname(os.path.abspath(__file__)))


dash.register_page(__name__, path="/", name="Home") # Register the homepage

 # Main content for homepage
homepage_content = html.Div(
    id="main-content",
    style={
        "position": "absolute",
        "top": "60px",
        "left": "65px",
        "width": "300px",
        "height": "600px",
        "zIndex": "1", 
        "paddingBottom": "100px"
    },
    children=[
        # Header "Top Stories this Week"
        html.H1(
            "Top Stories this Week",
            style={
                "color": "white",
                "fontWeight": "600",
                "fontSize": "22px",
                "marginBottom": "20px",
                "fontFamily": "Montserrat, sans-serif"
            }
        ),
        # Container for the articles
        html.Div(
            children=[
                generate_card_scroll(df_articles)
            ],
            style={
                "position": "absolute",
                "left": "-55px",
                "display": "block",
                "overflowY": "auto",
                "overflowX": "hidden"
            }
        ),
        html.Label(
            "Select a Month and Year to forecast next Quarter GDP Growth Rate",
            style={
                "color": "rgba(206, 203, 203)",
                "fontWeight": "600",
                "fontSize": "20px",
                "marginBottom": "20px",
                "fontFamily": "Montserrat, sans-serif", 
                "position": "absolute",
                "left": "350px", 
                "top": "400px",
                "width": "900px"
            }
        ),
       
       
        # Container for Forecast label and value
        html.Div(
            children = [
                html.H1(
                    id = 'gdp-forecast-title',
                    children = ["GDP Forecast for: "],
                    style={
                        "color": "rgba(206, 203, 203)",
                        "fontWeight": "600",
                        "fontSize": "22px",
                        "fontFamily": "Montserrat, sans-serif"
                    }
                ),
                html.H2(
                    id = 'gdp-forecast', children="",
                    style={
                        "color": "white",
                        "fontWeight": "600",
                        "fontSize": "28px",
                        "fontFamily": "Montserrat, sans-serif"
                    }
                ),

                ], style={"position": "absolute",
                        "height": "5px",
                        "width": "500px", 
                        "left": "360px",
                        "top": "-2px"}
        ), 
        # Container for displaying forecast graph
        html.Div( 
            children =[
            dcc.Graph(
                id = 'gdp-forecast-graph',
                figure = go.Figure(),
                config = {"displayModeBar": False},
                style={
                    "position": "absolute",
                    "left": "316px",
                    "top": "70px",
                    "width": "900px",
                    "height": "280px",
                    "backgroundColor": 'transparent'
                }
            )
            ]

        ), 
        # Add button to go explore the model
      html.Div(
            children=[
                dcc.Link(
                    dbc.Button(
                        "Explore Model",
                        id="explore-button",
                        size="sm",
                        style={
                            "backgroundColor": "grey",
                            "color": "white",
                            "border": "none",
                            "padding": "4px 8px",
                            "fontSize": "14px",
                            "display": "flex",
                            "justifyContent": "center",  
                            "alignItems": "center",      
                            "textAlign": "center",      
                            "width": "120px",
                            "borderRadius": "8px"
                        }
                    ),
                    href="/Bridge",  
                    style={
                        "position": "absolute",
                        "top": "70px",
                        "left": "650px",
                        "zIndex": "1000",
                        "textDecoration": "none"
                    }
                )
            ]
        ),
        html.Div(
                id="myear-display",
                style={
                    "color": "grey",
                    "fontSize": "16px",
                    "marginBottom": "10px",
                    "fontFamily": "Montserrat, sans-serif",
                    "textAlign": "center", 
                    "position": "absolute",
                    "left": "189px",
                    "top": "430px",
                    "width": "500px"
        }
),
         # Dropdown for selecting the month/year
        html.Div( 
            style={"position": "absolute",
                    "left": "347px",
                    "top": "470px"}, 
            children=[
                myear_dropdown()
    ]
), 
    # Add notification toast for invalid date selection
        dbc.Toast(
            id='home-error',
            header="Error",
            is_open=False,
            duration=4000,  
            dismissable=True,
            style={
                "position": "absolute",
                "top": "470px",
                "left": "700px",
                "zIndex": 1000,
                "backgroundColor": "rgba(255, 0, 0, 0.8)",
                "color": "white"
            }
        )
    ]
)

# Wrap the entire page content in a loading indicator
loading_content = html.Div(
    dcc.Loading(
        id="page-loading",
        type="circle",  
        children=homepage_content, 
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
deployment_url2 = 'https://sixs3ns3-backend-test.onrender.com/' # For deployment

@dash.callback(
    Output('myear-display', 'children'),
    Output('gdp-forecast', 'children'),
    Output('gdp-forecast', 'style'),
    Output('gdp-forecast-graph', 'figure'),
    Output('gdp-forecast-title', 'children'),
    Output('home-error', 'children'),
    Output('home-error', 'is_open'),
    Input('year-dropdown', 'value'),
    Input('month-dropdown', 'value')
)


def update_all(selected_year, selected_month):

    # Get current date
    current = datetime.now()
    current_year = current.year
    current_month_abbr = current.strftime("%b")

    # Convert selected values from dropdown
    selected_year_int = int(selected_year)
    selected_month_int = datetime.strptime(selected_month, "%b").month
    current_month_int = datetime.strptime(current_month_abbr, "%b").month

    # Default Display text 
    selected_date = f"{selected_month} {selected_year}"
    display_text = html.Span([
        html.Span("Selected Time: ", style={"color": "grey"}),
        html.Span(selected_date, style={"color": "white", "fontWeight": "700"})
    ])

    base_style = {
        "color": "grey",
        "fontWeight": "600",
        "fontSize": "28px",
        "fontFamily": "Montserrat, sans-serif"
    }

    # If selected date is in the future
    if selected_year_int > current_year or (selected_year_int == current_year and selected_month_int > current_month_int):
        error_toast_msg = f"⚠ Please select a date on or before {current_month_abbr} {current_year}."
        forecast_title = f"Forecast Unavailable"
        return (
            display_text,
            "-",
            base_style,
            dash.no_update,
            forecast_title,
            error_toast_msg,  
            True             
        )

    # ---- If valid date, fetch data from backend ----
    response = requests.post(
        f"{deployment_url2}/bridge_model_prediction",
        headers={'Content-Type': 'application/json'},
        data=json.dumps({"year": selected_year, "month": selected_month})
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
            "text": f"GDP Growth Rate up till {selected_date}",
            "font": {"color": "grey", "family": "Montserrat, sans-serif"}
        }
    )

    forecast_title = f"Forecast for {data['Quarter'].iloc[-1]}"

    return display_text, forecast_value, forecast_style, fig, forecast_title, "", False
