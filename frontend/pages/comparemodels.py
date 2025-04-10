import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
import requests
from scipy.stats import norm
from Components.package_imports import *
from shared.default_pagelayout import get_default_layout
from shared.myear_dropdown import myear_dropdown

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
# current_dir is /path/to/MyProject/frontend/pages
# The project root is two levels up: 
project_root = os.path.join(current_dir, '..', '..')
# Now build the path to test.csv inside Components/Predictions:
test_csv_path = os.path.join(project_root, 'Components', 'Predictions', 'test.csv')

#link page to homepage
dash.register_page(__name__, path="/comparemodels", name="Compare Models")

#Link to backend server
api_url = "http://127.0.0.1:5000"

# ---------------------
# DATA FETCHING AND MODEL GENERATING FUNCTIONS 
# ---------------------

def generate_model_figure_and_forecast(api_endpoint, model_label, year, month):
    response = requests.post(
        f"{api_url}/{api_endpoint}", 
        headers={'Content-Type': 'application/json'},
        data=json.dumps({"year": year, "month": month})
    )
    data = response.json()
    data = pd.DataFrame.from_dict(data)
    data = data.reset_index().rename(columns={"index": "Quarter"})
    data = data[data["Quarter"].str[:4].astype(int) >= 2000]

    base_style = {
        "fontSize": "28px",
        "fontFamily": "Montserrat, sans-serif"
    }
    try:
        value = data["Predicted GDP"].iloc[-1]
    except (IndexError, KeyError):
        value = 0
    value = round(value, 3)
    print(f"For {model_label}: Predicted GDP value is {value}", flush=True)

    # Determine the color based on value
    if value < 0:
        color = "red"
    elif value > 0:
        color = "rgb(0,200,83)"
    else:
        color = "white"

    # Format forecast text with color styling
    forecast_display = html.Span(f"{value:.3f}%", style={"color": color})

    fig = px.line(
        data, 
        x="Quarter", 
        y="Predicted GDP", 
        title=f"{model_label}: GDP Forecast",
        labels={"Predicted GDP": "GDP Growth Rate (%)", "Quarter": "Year"}, 
        template="plotly_dark"
    )
    fig.data[0].name = "Predicted GDP"
    fig.data[0].showlegend = True           
    
    if "Actual GDP" in data.columns:
        fig.add_trace(go.Scatter(
            x=data["Quarter"],
            y=data["Actual GDP"],
            mode="lines",
            name="Actual GDP",
            line=dict(color="orange", dash="dot")
        ))
    
    fig = apply_transparent_background(fig)
    
    return fig, forecast_display


def update_model1(year, month):
    return generate_model_figure_and_forecast("mean_model_prediction", "Model 1", year, month)

def update_model2(year, month):
    return generate_model_figure_and_forecast("arft04_model_prediction", "Model 2", year, month)

def update_model3(year, month):
    return generate_model_figure_and_forecast("midas_model_prediction", "Model 3", year, month)

def update_model4(year, month):
    return generate_model_figure_and_forecast("bridge_model_prediction", "Model 4", year, month)

def update_model5(year, month):
    return generate_model_figure_and_forecast("rf_model_prediction", "Model 5", year, month)



# Evaluation Metrics Fixed Values (Based on Test Data)
rmse_values = {
   "Model 1": 2.2,
   "Model 2": 1.8,
   "Model 3": 5.0,
   "Model 4": 6.7,
   "Model 5": 3.2
}


mae_values = {
   "Model 1": 3.4,
   "Model 2": 1.1,
   "Model 3": 0.9,
   "Model 4": 2.5
}


da_values = {
   "Model 1": 8.7,
   "Model 2": 2.4,
   "Model 3": 0.02,
   "Model 4": 10.7
}

model_labels = {
    "Model 1": "Prevailing Mean Benchmark Model",
    "Model 2": "ARFT04 Benchmark Model",
    "Model 3": "Mixed Data Sampling (MIDAS) Model",
    "Model 4": "Bridge Model",
    "Model 5": "Random Forest (RF)"
}


# ---------------------
# HELPER FUNCTIONS FOR STYLING
# ---------------------

def get_dropdown_style():
    return {
        "backgroundColor": "transparent",  # clear background
        "fontWeight": "bold",                # bold text inside the input
        "color": "white",                   # white text color
        "padding": "5px"
    }

def apply_transparent_background(fig):
   fig.update_layout(
       paper_bgcolor='rgba(0,0,0,0)',  # Transparent outer background
       plot_bgcolor='rgba(0,0,0,0)',   # Transparent plotting area
       margin=dict(l=0, r=0, t=50, b=50),
       font={'color': 'white'}
   )
   return fig

def format_forecast(forecast):
   color = "green" if forecast > 0 else "red" if forecast < 0 else "black"
   sign = "+" if forecast > 0 else "-" if forecast < 0 else ""
   return html.Span(f"{sign}{abs(forecast)}%", style={"color": color})

# ---------------------
# PAGE LAYOUT 
# ---------------------
comparemodels_content = html.Div(id="main-content",children=[
   html.H1("Compare NowCast Models", style={'text-align': 'center', 'color':'white'}),
   html.Br(),
   html.H4("Select a Month and Year to forecast next Quarter GDP Growth Rate", style={'text-align': 'center', 'color':'white'}),

   html.Div([myear_dropdown()], style={
        'width': '23%',          # set a width less than 100%
        'margin': '0 auto',       # center the element horizontally
        'margin-bottom': '20px'
    }),

   # Dropdown and Graph for Model 1
   html.Div([
       dcc.Dropdown(
           id="model_title1",
           options= model_labels,
           value = "Model 1",
           placeholder="Select Model 1",
           style=get_dropdown_style(),
           className="comparemodels-dropdown"
       ),
       html.H4("GDP Forecast Next Quarter:", style={'color':'white'}),
       html.Div(id='forecast_output_1', style={"fontWeight": "bold", "fontSize": "24px"}),
       dcc.Graph(id='graph_1'),
   ], style={'display': 'inline-block', 'width': '48%'}),


   # Dropdown and Graph for Model 2
   html.Div([
       dcc.Dropdown(
           id="model_title2",
           options= model_labels,
           value = "Model 2",
           placeholder="Select Model 2",
           style=get_dropdown_style(),
           className="comparemodels-dropdown"
       ),
       html.H4("GDP Forecast Next Quarter:", style={'color':'white'}),
       html.Div(id='forecast_output_2', style={"fontWeight": "bold", "fontSize": "24px"}),
       dcc.Graph(id='graph_2'),
   ], style={'display': 'inline-block', 'width': '48%', 'marginLeft': '2%'}),


   # Evaluation Section
   html.Br(),
    html.Div([
        html.H1("Evaluation", style={'color':'white', 'margin-right': '10px'}),
        html.H6("*based on test data", style={'color':'grey', 'fontStyle':'italic'})
    ], style={'display': 'flex', 'alignItems': 'center'}),
   html.Div(style={'borderTop': '2px solid white', 'margin': '20px 0'}),
  
   # Dropdown for Evaluation Metric
   html.Div([
       dcc.Dropdown(
           id="evaluation_metric",
           options=[
               {'label': 'Root Mean Squared Error (RMSE)', 'value': 'rmse'},
               {'label': 'Mean Absolute Error (MAE)', 'value': 'mae'},
               {'label': 'Directional Accuracy (DA)', 'value': 'da'}
           ],
           value = "mae",
           placeholder='Select Evaluation Metric',
           style=get_dropdown_style(),
           className="comparemodels-dropdown"
       )
   ], style={'width': '50%', 'marginBottom': '20px'}),
  
   # Display Evaluation Metric for Model 1
   html.Div(id="evaluation_metric1", style={'display': 'inline-block','fontSize': '20px', 'width': '50%', 'color':'white'}),
  
   # Display Evaluation Metric for Model 2
   html.Div(id="evaluation_metric2", style={'display': 'inline-block','fontSize': '20px', 'width': '50%', 'color':'white'}),

   #Display DM Test Values
   html.Div(id="dm_test_results", style={'display': 'inline-block','fontSize': '20px', 'text-align':'center', 'width':'100%', 'color':'white'}),
],
style={
       'height': '100vh',
       'overflowY': 'scroll',  # Enable scrolling
       'paddingTop': "25px", #Leave space on top for nav bar 
       'paddingBottom': '200px' #bottom padding
   })

# Plug that content into your default layout
layout = get_default_layout(main_content= comparemodels_content)

# ---------------------
# CALLBACKS
# ---------------------

# Callback for Model 1: Update graph and forecast with date filtering
@dash.callback(
   [Output('graph_1', 'figure'),
    Output('forecast_output_1', 'children')],
   [Input('model_title1', 'value'),
    Input('year-dropdown', 'value'),
    Input('month-dropdown', 'value')]
)
def update_graph_and_forecast_1(model_name, year, month):
    if model_name and year and month:
        # Choose which model function to call based on model_name
        if model_name == "Model 1":
            fig, forecast_text = update_model1(year, month)
        elif model_name == "Model 2":
            fig, forecast_text = update_model2(year, month)
        elif model_name == "Model 3":
            fig, forecast_text = update_model3(year, month)
        elif model_name == "Model 4":
            fig, forecast_text = update_model4(year, month)
        elif model_name == "Model 5":
            fig, forecast_text = update_model5(year, month)
        else:
            fig = go.Figure()
            forecast_text = ""
        return fig, forecast_text
    return {}, ""


# Callback for Model 2: Update graph and forecast with date filtering
@dash.callback(
   [Output('graph_2', 'figure'),
    Output('forecast_output_2', 'children')],
   [Input('model_title2', 'value'),
    Input('year-dropdown', 'value'),
    Input('month-dropdown', 'value')]
)
def update_graph_and_forecast_2(model_name, year, month):
    if model_name and year and month:
        # Choose which model function to call based on model_name
        if model_name == "Model 1":
            fig, forecast_text = update_model1(year, month)
        elif model_name == "Model 2":
            fig, forecast_text = update_model2(year, month)
        elif model_name == "Model 3":
            fig, forecast_text = update_model3(year, month)
        elif model_name == "Model 4":
            fig, forecast_text = update_model4(year, month)
        elif model_name == "Model 5":
            fig, forecast_text = update_model5(year, month)
        else:
            fig = go.Figure()
            forecast_text = ""
        return fig, forecast_text
    return {}, ""


# Callback for evaluation metric 1
@dash.callback(
   Output('evaluation_metric1', 'children'),
   [Input('model_title1', 'value'),
    Input('evaluation_metric', 'value')]
)
def update_eval_metric_1(model, metric):
   if model and metric:
       # Fetch the appropriate evaluation metric value based on selection
       if metric == 'rmse':
           eval_metric = rmse_values.get(model, "Not Available")
       elif metric == 'mae':
           eval_metric = mae_values.get(model, "Not Available")
       elif metric == 'da':
           eval_metric = da_values.get(model, "Not Available")


       # Return the metric and model name on separate lines with different styles
       return html.Div([
       html.Div(f'{eval_metric}%', style={"fontSize": "36px", "fontWeight": "bold"}),
       html.Div(f'{metric.upper()} for {model_labels.get(model, model)}', style={"fontSize": "18px", "fontWeight": "normal"}),
       ], style={'width': '50%', 'text-align':'center', 'margin': '0 auto'}) 

   return "Select a model and metric to display the evaluation result."


# Callback for evaluation metric 2
@dash.callback(
   Output('evaluation_metric2', 'children'),
   [Input('model_title2', 'value'),
    Input('evaluation_metric', 'value')]
)
def update_eval_metric_2(model, metric):
   if model and metric:
       # Fetch the appropriate evaluation metric value based on selection
       if metric == 'rmse':
           eval_metric = rmse_values.get(model, "Not Available")
       elif metric == 'mae':
           eval_metric = mae_values.get(model, "Not Available")
       elif metric == 'da':
           eval_metric = da_values.get(model, "Not Available")


       # Return the metric and model name on separate lines with different styles
       return html.Div([
       html.Div(f'{eval_metric}%', style={"fontSize": "36px", "fontWeight": "bold"}),
       html.Div(f'{metric.upper()} for {model_labels.get(model, model)}', style={"fontSize": "18px", "fontWeight": "normal"}),
       ], style={'width': '50%', 'text-align':'center', 'margin': '0 auto'}) 


   return "Select a model and metric to display the evaluation result."


# Callback to perform the Diebold-Mariano test based on selected models
@dash.callback(
   Output('dm_test_results', 'children'),
   [Input('model_title1', 'value'),
    Input('model_title2', 'value')]
)
def compute_dm_test(model1_name, model2_name):
    if model1_name and model2_name:
        model_to_pred = {
        "Model 1": os.path.join(project_root, "Components", "Predictions", "benchmark1.csv"),
        "Model 2": os.path.join(project_root, "Components", "Predictions", "arft04.csv"),
        "Model 3": os.path.join(project_root, "Components", "Predictions", "midas.csv"),
        "Model 4": os.path.join(project_root, "Components", "Predictions", "bridge.csv"),
        "Model 5": os.path.join(project_root, "Components", "Predictions", "rf_bridge.csv")
        }

        # Read the test data, which might be used as the true values
        try:
            test = pd.read_csv(test_csv_path, index_col=0)
        except Exception as e:
            return f"Error reading test data: {e}"
        
        # Get file paths for the selected models
        pred1_file = model_to_pred.get(model1_name)
        pred2_file = model_to_pred.get(model2_name)
        if pred1_file is None or pred2_file is None:
            return "Selected model does not have an associated predictions file."
        
        try:
            pred1 = pd.read_csv(pred1_file, index_col=0)
            pred2 = pd.read_csv(pred2_file, index_col=0)
        except Exception as e:
            return f"Error reading prediction data: {e}"
        stat, p, se, mean = dm_test(test, pred1, pred2)
        
        # Create a list of HTML elements to display the results.
        dm_text = [
            html.H2("Diebold-Mariano (DM) Test Results", style={"color": "white"}),
            html.Div(f"DM Stat: {stat:.2f}", style={"color": "white", "fontSize": "20px"}),
            html.Div(f"p-value: {p:.3f}", style={"color": "white", "fontSize": "20px"}),
            html.Div(f"HAC SE: {se:.3f}", style={"color": "white", "fontSize": "20px"}),
            html.Div(f"Mean Loss Differential: {mean:.3f}", style={"color": "white", "fontSize": "20px"})
        ]
        return dm_text
    return "Please select both models to compare."
