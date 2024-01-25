
"""Die Datei "dash_picarp.py" öffnet eine HTML-Seite, um per Dash die aufgezeichneten Fahrdaten zu visualisieren.

Funktionalität:
    - Anzeige der Werte Minimal-, Durchschnitts- und Höchstgeschwindigkeit Sowie Gesamtstrecke und -testzeit in KAcheln

    - Mittels einer weiteren Dropdown-Liste kann aus der Messdatei ein Messsignal zum Darstellen in einem Graphen verwendet werden.

"""
import dash
from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import json

# Verwendung von externen Stylesheets 
app = dash.Dash(external_stylesheets=[dbc.themes.LUMEN])
# Einlesen der CSV-Datei mit den Messergebnissen in ein Panda Dataframe
df = pd.read_csv("messergebnisse.csv")

# Definition "Kartenelements zur Anzeige der max. Geschwindigkeit"
card_max_speed = dbc.Card(
    [
        dbc.CardImg(src="/static/images/max.jpg", style={'height':150, 'width':150}, top=True),
        dbc.CardBody(
            [
                html.H4("Max Speed", className="card-title"),
                html.P(
                    str(max(df["Speed"])) + " cm/s",
                    className="card-text",
                ),
            ]
        ),
    ],
    style={"width": "18rem"},
)

# Definition "Kartenelements zur Anzeige der min. Geschwindigkeit"
card_min_speed = dbc.Card(
    [
        dbc.CardImg(src="/static/images/low.jpg", style={'height':150, 'width':150}, top=True),
        dbc.CardBody(
            [
                html.H4("Min Speed", className="card-title"),
                html.P(
                    str(min(df["Speed"])) + " cm/s",
                    className="card-text",
                ),
            ]
        ),
    ],
    style={"width": "18rem"},
)

# Definition "Kartenelements zur Anzeige der durchschnittlichen Geschwindigkeit"
card_avg_speed = dbc.Card(
    [
        dbc.CardImg(src="/static/images/mid.jpg", style={'height':150, 'width':150}, top=True),
        dbc.CardBody(
            [
                html.H4("Avg Speed", className="card-title"),
                html.P(
                    str(round(df["Speed"].mean(),2)) + " cm/s",
                    className="card-text",
                ),
            ]
        ),
    ],
    style={"width": "18rem"},
)

# Definition "Kartenelements zur Anzeige der Gesamtfahrstrecke
card_total_driving_length = dbc.Card(
    [
        dbc.CardImg(src="/static/images/track.png", style={'height':150, 'width':150}, top=True),
        dbc.CardBody(
            [
                html.H4("Gesamtstrecke", className="card-title"),
                html.P(
                    str(round(df["Speed"].mean() * (max(df["Time"])-min(df["Time"])), 2)) + " cm",
                    className="card-text",
                ),
            ]
        ),
    ],
    style={"width": "18rem"},
)

card_total_test_time = dbc.Card(
    [
        dbc.CardImg(src="/static/images/time.png", style={'height':150, 'width':150}, top=True),
        dbc.CardBody(
            [
                html.H4("Gesamttestzeit", className="card-title"),
                html.P(
                    str(round(max(df["Time"])-min(df["Time"]),2)) + " s",
                    className="card-text",
                ),
            ]
        ),
    ],
    style={"width": "18rem"},
)

# Platzierung und Gestaltung des HTML-Layouts
app.layout = html.Div(
    children=[
        html.H1(id='titel', children='PiCar Dashboard'),
        html.Br(),
        # Anordnung der Kacheln in einer Reihe
        dbc.Row([
            dbc.Col([card_min_speed], width=2),
            dbc.Col([card_avg_speed], width=2),
            dbc.Col([card_max_speed], width=2),
            dbc.Col([card_total_driving_length], width=2),
            dbc.Col([card_total_test_time], width=2)
        ], align='center'),
        html.Br(),
        # Titel für die graphische Anzeige der Messsignale
        html.H2(id='titel1', children='Messsignale'),
        html.Br(),
        html.Div(children='Wählen Sie ein anzuzeigendes Signal aus.'),
        # Drop-Down Liste zur Auswahl des anzuzeigenden Mess-Signals
        dcc.Dropdown(id='dropdown',
                     options=[
                         {'label': 'Speed', 'value': 'Speed'},
                         {'label': 'Direction', 'value': 'Direction'},
                         {'label': 'Distance', 'value': 'Distance'},
                         {'label': 'Steering angle', 'value': 'SteeringAngle'},
                     ],
                     value='SteeringAngle'),
        # Erstellung des Graphen mit der ID: line_plot
        dcc.Graph(id='line_plot'),
        html.Br(),
        
    ], style={
        "backgroundColor": "#DDDDDD",
        "maxWidth": "1100px",
        "padding":"20px 30px 40px",
        }
)

# Darstellung des ausgewählten Mess-Signals aus der Drop-Down Liste
@app.callback(Output(component_id='line_plot', component_property='figure'),
              [Input(component_id='dropdown', component_property='value')])
def graph_update(value_of_input_component):
    print(value_of_input_component)
    fig = px.line(df, x=df['Time'], y=df[value_of_input_component])
    return fig

# Main zum direkten Aufruf und Anzeigen des Dashboards im Webbrowser
if __name__ == '__main__':
    #Prüfung, ob eine IP-Adresse für den Pi in der config.json hinterlegt ist, 
    # falls nicht, wird das Dashboard lokal im Webbrowser angezeigt
    try:
        with open("config.json", "r") as f:
            data = json.load(f)
            raspberry_ip = data["raspberry_ip"]
            app.run_server(host = raspberry_ip, port=8080, debug=True)
    except:
        print("Keine geeignete Datei config.json gefunden!")
        app.run_server(debug=True)


