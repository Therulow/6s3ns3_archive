from dash import html, dcc
from datetime import datetime
import calendar

def myear_dropdown(): 
    return html.Div(
            style={ 
                "display": "flex",
                "flexDirection": "row",
                "gap": "10px",   
                "alignItems": "center"
        },
            children=[
                
                dcc.Dropdown(
                    id='month-dropdown',
                    options=[{'label': m, 'value': m} for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                                                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']],
                    value= calendar.month_abbr[datetime.now().month],
                    clearable = False,
                    className="myear-dropdown"
                ),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': str(year), 'value': str(year)} for year in range(datetime.now().year, 1999, -1)],
                    value=str(datetime.now().year),
                    clearable = False,
                    className="myear-dropdown"
                ),
    ]
)