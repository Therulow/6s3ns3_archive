import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
import requests
from scipy.stats import norm
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from Components.package_imports import *
from shared.default_pagelayout import get_default_layout
from shared.myear_dropdown import myear_dropdown
from datetime import datetime

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
deployment_url = 'https://sixs3ns3-backend-test.onrender.com/' #for deployment

# Link to local server
api_url = 'http://127.0.0.1:5000/'


# ---------------------
# DATA FETCHING AND MODEL GENERATING FUNCTIONS 
# ---------------------

def generate_model_figure_and_forecast(api_endpoint, model_label, year, month):
    response = requests.post(
        f"{deployment_url}/{api_endpoint}", 
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
   "Model 1": 0.811495,
   "Model 2": 0.719911,
   "Model 3": 0.65465,
   "Model 4": 0.616918,
   "Model 5": 0.661384
}


mae_values = {
   "Model 1": 0.52913,
   "Model 2": 0.505932,
   "Model 3": 0.462518,
   "Model 4": 0.443277,
   "Model 5": 0.470836
}


da_values = {
   "Model 1": 0.92,
   "Model 2": 0.92,
   "Model 3": 0.94,
   "Model 4": 0.94,
   "Model 5": 0.96
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
   html.H1("Compare NowCast Models", style={'text-align': 'center', 'color':'white', 'fontWeight':'600'}),
   html.Br(),
   html.H4("Select a Month and Year to forecast next Quarter GDP Growth Rate", style={'text-align': 'center', 'color':'white'}),

   html.Div([myear_dropdown()], style={
        'width': '25%',          
        'margin': '0 auto',       
        'margin-bottom': '20px',
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center'
    }),

    html.Div( children = [
        dbc.Toast(
            id='error6',
            header="Error",
            is_open=False,
            duration=4000,  
            dismissable=True,
            style={
                "zIndex": 1000,
                "backgroundColor": "rgba(255, 0, 0, 0.8)",
                "color": "white"
            }
        ),
    ]
    , style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center'
    }),

    html.Br(),

    html.Div([
        # Dropdown and Graph for Model 1
        html.Div([
            dcc.Dropdown(
                id="model_title1",
                options=model_labels,
                value="Model 1",
                placeholder="Select Model 1",
                className="comparemodels-dropdown",
                clearable=False
            ),
            html.Br(),
            html.H4("GDP Forecast Next Quarter:", style={'color': 'white'}),
            html.Div(id='forecast_output_1', style={"fontWeight": "bold", "fontSize": "24px"}),
            dcc.Graph(id='graph_1'),
        ], style={'display': 'inline-block', 'width': '45%'}),
        
        # Dropdown and Graph for Model 2
        html.Div([
            dcc.Dropdown(
                id="model_title2",
                options=model_labels,
                value="Model 2",
                placeholder="Select Model 2",
                className="comparemodels-dropdown",
                clearable=False
            ),
            html.Br(),
            html.H4("GDP Forecast Next Quarter:", style={'color': 'white'}),
            html.Div(id='forecast_output_2', style={"fontWeight": "bold", "fontSize": "24px"}),
            dcc.Graph(id='graph_2'),
        ], style={'display': 'inline-block', 'width': '45%', 'marginLeft': '5%'})
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center'
    }),

    html.Br(),

   # Evaluation Section
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
           value = "rmse",
           placeholder='Select Evaluation Metric',
           className="comparemodels-dropdown",
           clearable = False
       )
   ], style={'width': '50%', 'marginBottom': '20px'}),
  
  html.Div([
    # Display Evaluation Metric for Model 1
   html.Div(id="evaluation_metric1", style={'display': 'inline-block','fontSize': '20px', 'width': '50%', 'color':'white'}),
  
   # Display Evaluation Metric for Model 2
   html.Div(id="evaluation_metric2", style={'display': 'inline-block','fontSize': '20px', 'width': '50%', 'color':'white'})
   ]),

   html.Br(),

   #Display DM Test Values
   html.Div(id="dm_test_results", style={'display': 'inline-block','fontSize': '20px', 'text-align':'center', 'width':'100%', 'color':'white'}),
],
style={
       'height': '100vh',
       'overflowY': 'scroll',  # Enable scrolling
       'paddingTop': "25px", #Leave space on top for nav bar 
       'paddingBottom': '200px', #bottom padding
       'marginLeft': '50px',
        'marginRight': '50px'
   })

# Wrap the entire page content in a loading indicator
loading_content = html.Div(
    dcc.Loading(
        id="page-loading",
        type="circle",  
        children=comparemodels_content, 
        style={
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
            "height": "100vh" 
        }

    )
)

layout = get_default_layout(main_content= loading_content)

# ---------------------
# CALLBACKS
# ---------------------

# Callback for Model 1: Update graph and forecast with date filtering
@dash.callback(
   [Output('graph_1', 'figure'),
    Output('forecast_output_1', 'children'),
    Output('error6', 'children'),
    Output('error6', 'is_open')],
   [Input('model_title1', 'value'),
    Input('year-dropdown', 'value'),
    Input('month-dropdown', 'value')]
)
def update_graph_and_forecast_1(model_name, year, month):
    current = datetime.now()
    current_year = current.year
    current_month_abbr = current.strftime("%b")
    
    # Convert selected values from dropdown
    selected_year_int = int(year)
    selected_month_int = datetime.strptime(month, "%b").month
    current_month_int = datetime.strptime(current_month_abbr, "%b").month

     # If selected date is in the future
    if selected_year_int > current_year or (selected_year_int == current_year and selected_month_int > current_month_int):
        error_toast_msg = f"⚠ Please select a date on or before {current_month_abbr} {current_year}."
        return (dash.no_update, dash.no_update, error_toast_msg, True)

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
        return fig, forecast_text, "", False
    return (
        dash.no_update,            
        forecast_text,
        "",           
        False                     
    )


# Callback for Model 2: Update graph and forecast with date filtering
@dash.callback(
   [Output('graph_2', 'figure'),
    Output('forecast_output_2', 'children')],
   [Input('model_title2', 'value'),
    Input('year-dropdown', 'value'),
    Input('month-dropdown', 'value')]
)
def update_graph_and_forecast_2(model_name, year, month):
    current = datetime.now()
    current_year = current.year
    current_month_abbr = current.strftime("%b")
    
    # Convert selected values from dropdown
    selected_year_int = int(year)
    selected_month_int = datetime.strptime(month, "%b").month
    current_month_int = datetime.strptime(current_month_abbr, "%b").month

     # If selected date is in the future
    if selected_year_int > current_year or (selected_year_int == current_year and selected_month_int > current_month_int):
        return (dash.no_update, dash.no_update)

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
       html.Div(f'{eval_metric}', style={"fontSize": "36px", "fontWeight": "bold"}),
       html.Div(f'{metric.upper()} for {model_labels.get(model, model)}', style={"fontSize": "18px", "fontWeight": "normal", "whiteSpace": "nowrap"}),
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
       html.Div(f'{eval_metric}', style={"fontSize": "36px", "fontWeight": "bold"}),
       html.Div(f'{metric.upper()} for {model_labels.get(model, model)}', style={"fontSize": "18px", "fontWeight": "normal","whiteSpace": "nowrap"}),
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
        
        # Determine colors based on values
        dm_color = "rgb(255, 153, 51)" if stat > 0 else "rgb(255,204,51)" 
        p_color = "rgb(255,182,193)" if p < 0.1 else "rgb(33, 158, 188)" 

        # Build the text for the DM Test Results
        dm_result_components = [
        html.H2("Diebold-Mariano (DM) Test Results", style={"color": "white"}),
        html.Div([
            "DM Stat: ",
            html.Span(f"{stat:.2f}", style={"color": dm_color})
        ], style={"fontSize": "20px", "color": "white"}),
        html.Div([
            "p-value: ",
            html.Span(f"{p:.3f}", style={"color": p_color})
        ], style={"fontSize": "20px", "color": "white"}),
        html.Div([
            "HAC SE: ",
            html.Span(f"{se:.3f}", style={"color": "white"})
        ], style={"fontSize": "20px", "color": "white"}),
        html.Div([
            "Mean Loss Differential: ",
            html.Span(f"{mean:.3f}", style={"color": "white"})
        ], style={"fontSize": "20px", "color": "white"})]

    # Determine the DM test result conclusion based on stat and p
    if stat > 0:
        # For stat > 0, model2 is better than model1.
        model1_display = html.Span(model_labels.get(model1_name, model1_name), style={"color": "white"})
        model2_display = html.Span(f'{model_labels.get(model2_name, model2_name)} is better', style={"color": dm_color})
        
        # Set the significance text and color based on p
        if p < 0.1:
            significance_text = html.Span("is with", style={"color": "rgb(255,182,193)"})
            conclusion_text = html.Div(
            [
                model2_display,
                " than ",
                model1_display,
                ".",
                " This ",
                significance_text,
                " statistical significance."
            ], style={"color": "white", "fontSize": "20px", "fontWeight": "bold"})
        else:
            significance_text = html.Span("may not be with", style={"color": "rgb(33, 158, 188)"})
            conclusion_text = html.Div(
            [
                model2_display,
                " than ",
                model1_display,
                ".",
                " However, this ",
                significance_text,
                " statistical significance."
            ], style={"color": "white", "fontSize": "20px", "fontWeight": "bold"})

    elif stat < 0:
        # For stat < 0, model1 is better than model2.
        model1_display = html.Span(f'{model_labels.get(model1_name, model1_name)} is better', style={"color": dm_color})
        model2_display = html.Span(model_labels.get(model2_name, model2_name), style={"color": "white"})
        
        if p < 0.1:
            significance_text = html.Span("is with", style={"color": "rgb(255,182,193)"})
            conclusion_text = html.Div(
            [
                model1_display,
                " than ",
                model2_display,
                ".",
                " This ",
                significance_text,
                " statistical significance."
            ], style={"color": "white", "fontSize": "20px", "fontWeight": "bold"})
        else:
            significance_text = html.Span("may not be with", style={"color": "rgb(33, 158, 188)"})
            conclusion_text = html.Div(
            [
                model1_display,
                " than ",
                model2_display,
                ".",
                " However, this ",
                significance_text,
                " statistical significance."
            ], style={"color": "white", "fontSize": "20px", "fontWeight": "bold"})
            
    else:
        conclusion_text = html.Div("No significant difference between models.", 
                                style={"color": "white", "fontSize": "20px", "fontWeight": "bold"})

    # Finally, append the conclusion text to your DM test result components
    dm_result_components.append(html.Br())
    dm_result_components.append(conclusion_text)

    return dm_result_components
