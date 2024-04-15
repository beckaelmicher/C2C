"""Die Datei "dash_app.py" öffnet eine HTML-Seite, um per Dash das Steuern des Raspberry-Cars zu können.

Funktionalität:
    - Auswahl des gewünschten Fahrparcours aus Dropdown-Liste mit Möglichkeit zum Starten dieser mittels Start-Button.
    
    - Das PiCar kann mittels des Stop-Buttons jederzeit angehalten werden.
    
    - Mittels einer weiteren Dropdown-Liste kann nach dem Fahren aus der erzeugten Messdatei ein Messsignal zum Darstellen in einem Graphen verwendet werden.

"""
import dash
from dash import dcc, html, Input, Output, State, ctx
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import json
import plotly.express as px
import fahrparcours_dash as fpd


# Verwendung von externen Stylesheets 
app = dash.Dash(external_stylesheets=[dbc.themes.LUMEN])

# Platzierung und Gestaltung des HTML-Layouts
app.layout = html.Div(
    children=[
        html.H1(id='titel', children='PiCar App'),
        html.Br(),
        html.H3(id='titel1', children='Auswahl der Fahrfunktionen'),
        dbc.Row([
            dbc.Col([
                html.Div(children='Wählen Sie den gewünschten Fahrparcours aus:'),
                html.Br(),
                 # Drop-Down Liste zur Auswahl des Fahrparcours
                dcc.Dropdown(id='dropdown',
                     options=[
                         {'label': 'Fahrparcours 1 - Vorwärts und Rückwärts', 'value': '1'},
                         {'label': 'Fahrparcours 2 - Kreisfahrt mit maximalem Lenkwinkel', 'value': '2'},
                         {'label': 'Fahrparcours 3 - Vorwärtsfahrt bis Hindernis', 'value': '3'},
                         {'label': 'Fahrparcours 4 - Erkundungstour', 'value': '4'},
                         {'label': 'Fahrparcours 5 - Linienverfolgung', 'value': '5'},
                     ],
                     value='1'),
            ], align='center'),
            # Start-/ Stop-Button für Ausführen und Stoppen des Fahrparcours eingefügt
            dbc.Col([
                html.Button('Start', id='start_button', n_clicks=0),
                html.Br(),
                html.Br(),
                html.Button('Stop', id='stop_button', n_clicks=0),
            ]),
        ], align='center'),

        html.Br(),
        html.Div(id="log", children=''),
        html.Br(),
        html.H3(id='titel2', children='Anzeige des Loggings'),
        html.Div(children='Wählen Sie ein anzuzeigendes Signal aus:'),
        # Drop-Down Liste zur Auswahl des anzuzeigenden Mess-Signals
        dcc.Dropdown(id='dropdown2',
                      options=[
                        {'label': 'Geschwindigkeit', 'value': 'Speed'},
                        {'label': 'Fahrtrichtung', 'value': 'Direction'},
                        {'label': 'Abstand', 'value': 'Distance'},
                        {'label': 'Lenkwinkel', 'value': 'SteeringAngle'},
                     ],
                     value='SteeringAngle'),
        # Erstellung des Graphen mit der ID: line_plot
        dcc.Graph(id='line_plot'),
    ], style={
        "backgroundColor": "#DDDDDD",
        "maxWidth": "1000px",
        "padding":"20px 30px 40px",
        }
)

# Callback für Start-/Stop-Button
# Methode zum Starten des gewählten Fahrparcours und der Stop-Methode
# ctx Bibliothek zum Prüfen des gedrückten Buttons verwendet
@app.callback(
    Output('log', 'children'),
    [Input('start_button', 'n_clicks')], 
    [Input('stop_button', 'n_clicks')], 
    [State('dropdown', 'value')],
    prevent_initial_call=True
)
def start_fahrparcours(start_button, stop_button, value):
    button_id = ctx.triggered_id if not None else 'No clicks yet'
    if button_id == "start_button":
        if value == "1":
            fpd.fahrparcours_1()
            return "Fahrparcours 1 beendet"
        elif value == "2":
            fpd.fahrparcours_2()
            return "Fahrparcours 2 beendet"
        elif value == "3":
            fpd.fahrparcours_3()
            return "Fahrparcours 3 beendet"
        elif value == "4": 
            fpd.fahrparcours_4()
            return "Fahrparcours 4 beendet"
        elif value == "5": 
            fpd.fahrparcours_5()
            return "Fahrparcours 5 beendet"
    elif button_id == "stop_button":
        fpd.stop()
        return "Programm abgebrochen!"

# Darstellung des ausgewählten Mess-Signals aus der Drop-Down Liste
@app.callback(
    Output(component_id='line_plot', component_property='figure'),
    [Input(component_id='dropdown2', component_property='value')],
    prevent_initial_call=True
)
def graph_update(value_of_input_component):
    # Einlesen der CSV-Datei mit den Messergebnissen in ein Pandas Dataframe
    df = pd.read_csv("messergebnisse.csv")
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
