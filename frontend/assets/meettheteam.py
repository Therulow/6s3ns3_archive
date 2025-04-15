import dash_bootstrap_components as dbc
from dash import html

# Define your 6 team members
team_members = [
    {"name": "Jason Low", "title": "Front-End", "img": "./assets/pictures/jason.JPG"},
    {"name": "Shani Hiew", "title": "Front-End", "img": "/assets/pictures/shani.jpg"},
    {"name": "Steffi Lum", "title": "Front-End", "img": "/assets/pictures/steffi.JPG"},
    {"name": "Josiah Lee", "title": "Back-End", "img": "/assets/pictures/josiah.jpeg"},
    {"name": "Quek Hong Rui", "title": "Back-End", "img": "/assets/pictures/member5.jpg"},
    {"name": "Riley Teo", "title": "Back-End", "img": "/assets/pictures/riley.jpg"},
]

# Create the layout
def create_team_layout(team_members, cols_per_row=3):
    rows = []
    # Loop over team members in chunks of 'cols_per_row'
    for i in range(0, len(team_members), cols_per_row):
        row_members = team_members[i:i+cols_per_row]
        row = dbc.Row(
            [   
                dbc.Col(
                    html.Div(
                        [
                            html.Img(
                                src=member["img"],
                                style={
                                    "borderRadius": "50%",
                                    "width": "150px",
                                    "height": "150px",
                                    "objectFit": "cover",
                                    "marginBottom": "10px"
                                }
                            ),
                            html.H4(member["name"], style={"color": "white", "marginBottom": "0px", "fontFamily": "Montserrat"}),
                            html.P(member["title"], style={"color": "lightgrey", "fontFamily": "Montserrat"})
                        ],
                        style={"textAlign": "center"}
                    ),
                    width={"size": 12 // cols_per_row}  # This will be 4 when cols_per_row is 3
                )
                for member in row_members
            ],
            justify="center"
        )
        rows.append(row)
    return html.Div(rows, style={"marginTop": "30px"})


