
import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.express as px
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import json

# Verwendung von externen Stylesheets 
app = dash.Dash(external_stylesheets=[dbc.themes.LUMEN])
# Einlesen der CSV-Datei mit den Messergebnissen in ein Panda Dataframe
df = pd.read_csv("messergebnisse.csv")



# Platzierung und Gestaltung des HTML-Layouts
app.layout = html.Div(
    # Ausrichtung der KAcheln in zwei Reihen mit Reihe 1 zu 3 Spalten und Reihe 2 zu 2 Spalten
    children=[
        html.H1(id='titel',
                    children='PiCar App'),
        dbc.Row([
            dbc.Col([
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
            ], align='center'),
            
            dbc.Col([
                html.Button('Start', id='start_val', n_clicks=0),
                html.Br(),
                html.Br(),
                html.Button('Stop', id='stop_val', n_clicks=0),
            ]),
        ], align='center'),
        
        html.Div(children='Wählen Sie ein anzuzeigendes Signal aus.'),
        # Drop-Down Liste zur Auswahl des anzuzeigenden Mess-Signals
        # dcc.Dropdown(id='dropdown2',
        #               options=[
        #                 {'label': 'Speed', 'value': 'Speed'},
        #                 {'label': 'Direction', 'value': 'Direction'},
        #                 {'label': 'Distance', 'value': 'Distance'},
        #                 {'label': 'Steering angle', 'value': 'SteeringAngle'},
        #              ],
        #              value='SteeringAngle'),
        # Erstellung des Graphen mit der ID: line_plot
        # dcc.Graph(id='line_plot'),
        html.Br(),
        html.Div(id="log", children='ABC'),
    ]
)
@app.callback(
    Output('log', 'children'),
    [Input('start_val', 'n_clicks')], 
    [State('dropdown', 'value')],
    prevent_initial_call=True
)
def start_fahrparcours(n_clicks, value):
    if n_clicks > 0:
        if value == "Speed":
            # Rufe Methode x auf
            return "Reaktion für Speed"
        elif value == "Direction":
            # Rufe Methode x auf 
            return "Reaktion für Direction"
        elif value == "Distance":
            # Rufe Methode x auf 
            return "Reaktion für Distance"
        elif value == "Steering Angle": 
            # Rufe Methode x auf
            return "Reaktion für Steering Angle"
        


#  Reaktion in der App, sofern sich am Input Value etwas ändert
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



