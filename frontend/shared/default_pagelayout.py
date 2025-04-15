import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import os

# Set working directory to current file location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Reusable style for nav links and buttons (without inline color)
_nav_link_style = {
    "backgroundColor": "transparent",
    "border": "none",
    "fontFamily": "Montserrat, sans-serif",
    "fontSize": "22px",
    "cursor": "pointer",
    "textDecoration": "none"
}

# Default layout function
def get_default_layout(main_content=None):
    if main_content is None:
        main_content = html.Div(id="main-content")

    return html.Div(
        style={
            "minHeight": "100vh",
            "overflowY": "auto",
            "overflowX": "hidden",
            "background": "radial-gradient(circle at top left, #3e1f47 0%, #000000 25%)",
            "boxShadow": "0 0 100px #ff6a00",
            "margin": "0px",
            "padding": "0px",
            "position": "relative"
        },
        children=[
            # NAVBAR
            html.Nav(
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "padding": "30px 60px",
                    "fontFamily": "Montserrat, sans-serif",
                    "fontWeight": "400",
                    "fontSize": "22px",
                    "width": "100%"
                },
                children=[
                    html.Div([
                        dcc.Link("6S3NS3", href='/', className="logo-clickable", style={
                            "fontWeight": "800",
                            "fontSize": "32px",
                            "textDecoration": "none",
                            "marginRight": "20px", 
                            'marginLeft': '6px'
                        }),
                        dcc.Link("About", href="/about", className="fade-button-dropdown", style={
                            **_nav_link_style,
                            "marginLeft": "60px"
                        }),
                        html.Button("Models", id="model-fade-button", n_clicks=0,
                                    className="fade-button-dropdown", style=_nav_link_style),
                        html.Button("Latest US Economic Data", id="indicator-fade-button", n_clicks=0,
                                    className="fade-button-dropdown", style=_nav_link_style),
                    ], style={
                        "display": "flex",
                        "gap": "140px",
                        "alignItems": "center"
                    })
                ]
            ),

            # DROPDOWNS
            dbc.Fade(
                id="model-fade",
                is_in=False,
                appear=True,
                children=html.Div(
                    className="mega-dropdown",
                    children=[
                        html.Div("Explore Models", className="dropdown-item-normal"),
                        dcc.Link("Prevailing Mean Benchmark Model", href="/Mean", className="dropdown-item-bold"),
                        dcc.Link("ARFT04 Benchmark Model", href="/ARFT04", className="dropdown-item-bold"),
                        dcc.Link("MIDAS Model", href="/MIDAS", className="dropdown-item-bold"),
                        dcc.Link("Bridge Model", href="/Bridge", className="dropdown-item-bold"),
                        dcc.Link("RF Model", href="/RF", className="dropdown-item-bold"),
                        dcc.Link("Compare Models", href="/comparemodels", className="dropdown-item-bold")
                    ]
                )
            ),
            dbc.Fade(
                id="indicator-fade",
                is_in=False,
                appear=True,
                children=html.Div(
                    className="mega-dropdown",
                    children=[
                        html.Div("Explore Indicators", className="dropdown-item-normal"),
                        dcc.Link("CPI", href="/cpi", className="dropdown-item-bold"),
                        dcc.Link("Housing Starts", href="/housing_starts", className="dropdown-item-bold"),
                        dcc.Link("Industrial Production", href="/industrial_production", className="dropdown-item-bold"), 
                        dcc.Link("Unemployment Rate", href="/unemployment", className="dropdown-item-bold"),
                    ]
                )
            ),

            main_content
        ]
    )
