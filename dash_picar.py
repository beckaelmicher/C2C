
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

df = pd.read_csv("messergebnisse.csv")

#print(df.info())

#print(df["Distance"].mean())

# Definition eines dbc Element für die spätere Verwenung im Layout
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

card_total_driving_length = dbc.Card(
    [
        #dbc.CardImg(src="/static/images/squirrel.png", top=True),
        dbc.CardBody(
            [
                html.H4("Gesamtfahrstrecke", className="card-title"),
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
        #dbc.CardImg(src="/static/images/squirrel.png", top=True),
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

app.layout = html.Div(
    children=[
        dbc.Row([
            dbc.Col([card_max_speed], width=2),
            dbc.Col([card_min_speed], width=2),
            dbc.Col([card_avg_speed], width=2),
        ], align='center'),
         dbc.Row([
            dbc.Col([card_total_driving_length], width=2),
            dbc.Col([card_total_test_time], width=2)
        ], align='center'),
        html.H2(id='titel',
                children='Messsignale'),
        html.Div(children='Wählen Sie ein anzuzeigendes Signal aus.'),
        dcc.Dropdown(id='dropdown',
                     options=[
                         {'label': 'Speed', 'value': 'Speed'},
                         {'label': 'Direction', 'value': 'Direction'},
                         {'label': 'Distance', 'value': 'Distance'},
                         {'label': 'Steering angle', 'value': 'SteeringAngle'},
                     ],
                     value='SteeringAngle'),
        dcc.Graph(id='line_plot'),
        html.Br(),
        
    ]
)


# Callback für den Plot als Ausgabe (siehe 'line_plot') und den Wert des Dropdown Menüs als Eingabe
@app.callback(Output(component_id='line_plot', component_property='figure'),
              [Input(component_id='dropdown', component_property='value')])
def graph_update(value_of_input_component):
    print(value_of_input_component)
    fig = px.line(df, x=df['Time'], y=df[value_of_input_component])
    return fig


if __name__ == '__main__':
    try:
        with open("config.json", "r") as f:
            data = json.load(f)
            raspberry_ip = data["raspberry_ip"]
            app.run_server(host = raspberry_ip, port=8080, debug=True)
    except:
        print("Keine geeignete Datei config.json gefunden!")
        app.run_server(debug=True)


