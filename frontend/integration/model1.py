import sys
import os

# Add the parent directory of 'Components' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Now you can import benchmark1_prediction
from Components.benchmark1_prediction import benchmark1_prediction


import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime




def get_forecast(selected_date="Mar 2022"): 

    date = datetime.strptime(selected_date, "%b %Y").strftime("%Y-%m-%d")
    

    forecast_df = benchmark1_prediction(date)

    # get forecast from last one in dataframe
    forecast = forecast_df["pct_chg"].iloc[-1]

    return round(forecast,3)


# print(get_forecast("Jan2023"))

def get_forecast_graph(selected_date="Mar 2022"):
    date = datetime.strptime(selected_date, "%b %Y")

    forecast_df = benchmark1_prediction(date)
    # Cast index column as str
    forecast_df.index = forecast_df.index.astype(str)

    # Display only from 2000 onwards
    forecast_df_filtered = forecast_df.loc[forecast_df.index >= "2000"]
    

    # Create a line plot
    fig = px.line(
        forecast_df_filtered,
        x = 'quarters',
        y='pct_chg',
        title=f"Forecast GDP Growth Rate",
        labels={"pct_chg": "GDP Growth Rate (%)", "quarters": "Year"},
        template='plotly_dark'
    )

   # Add vertical line at selected date (datetime format)
    # fig.add_vline(x=date, line_dash="dash", line_color="red")


    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent outer background
        plot_bgcolor='rgba(0,0,0,0)',   # Transparent plotting area
        margin=dict(l=0, r=0, t=50, b=50),
        title = {
            "text": f"GDP Growth Rate up till {selected_date}",
            "font": {
                "color": "grey",
                "family": "Montserrat, sans-serif"
            }
        }, 
        height=280
    )

    return fig

def get_quarter(selected_date="Mar 2022"):
    date = datetime.strptime(selected_date, "%b %Y")
    forecast_df = benchmark1_prediction(date)

    # Get the last index from the DataFrame — assumes it's in 'YYYYQX' format
    last_quarter = forecast_df["quarters"].iloc[-1]

    return last_quarter

print(get_quarter())



def monthyear():
    # Define the start date (January 2000)
    start_date = pd.to_datetime("2000-01-01")
    # Get today's date
    today = datetime.today()
    # Create a PeriodIndex with monthly frequency from start_date to today
    months = pd.period_range(start=start_date, end=today, freq='M')
    # Format the periods as "Jan2000", "Feb2000", etc.
    month_list = months.strftime("%b %Y").tolist()
    # Return the list directly (not as a DataFrame)
    return month_list



# print(benchmark1_prediction())
# print(get_forecast_graph("Jan2023"))

# print(monthyear())
# print(get_forecast())
# print(benchmark1_prediction("2022-03-01"))
# print(type(benchmark1_prediction().index))