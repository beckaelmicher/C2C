from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from flask import Flask, Response
import time
import plotly.express as px
from basisklassen_cam import Camera
import cv2
import numpy as np
import image_processing as ip
from camcar import CamCar
from threading import Thread
from multiprocessing import Process
import os

external_stylesheets = [dbc.themes.BOOTSTRAP]
server = Flask(__name__)

app = Dash(__name__, external_stylesheets=external_stylesheets, server=server)
car = CamCar(config="config.json")
car.stop()

car.path = os.getcwd() + "/images/" # "/home/pi/Desktop/"
print(car.path)

@server.route("/video_feed")
def video_feed():
   result = car.stream() 
   return Response(result, mimetype='multipart/x-mixed-replace; boundary=frame')


# Layout: Reine Optik

app.layout = html.Div(children=[
    dbc.Row([html.H1("Verarbeitungsschritte", style={"textAlign": "center"}),
             html.Div(id="hidden-div", style={"display":"none"}),
             html.Div(id="hidden-div-2", style={"display":"none"}),
             html.Div(id="hidden-div-3", style={"display":"none"}),
             html.Div(id="hidden-div-4", style={"display":"none"}),
             html.Div(id="hidden-div-5", style={"display":"none"}),
             ]
            ), 
    dbc.Row([
        dbc.Col([
            html.Div([
            html.Img(src="/video_feed", id="videofeed", style={'height':'100%'})
            ]),
            
        ], width=3),
        dbc.Col([
                html.Div(id='dd-output-container', children="Auswahl des dargestellten Bilds"),
                dcc.Dropdown(['Original', 'ROI', 'Filtered', "Points"], 'Original', id='image-dropdown'),
                html.Br(),
                html.Br(),
                html.H1(id="angle")
                
        ], align="center", width=2),
        dbc.Col([
            html.H3("Anpassen HSV Filter"),
            html.Div([
                html.Div(id='slider-output-container-h', children="H lower and upper bounds"),
                dcc.RangeSlider(0, 179, 1, value=[0, 50], id='h-range-slider', marks={
                                0: "0", 179: "179"}, tooltip={'always_visible': True, 'placement': 'bottom'}),
                ]),
            html.Div([
                html.Div(id='slider-output-container-s', children="S lower and upper bounds"),
                dcc.RangeSlider(0, 255, 1, value=[0, 255], id='s-range-slider', marks={
                                0: "0", 255: "100"}, tooltip={'always_visible': True, 'placement': 'bottom'}),
                ]),
            html.Div([
                html.Div(id='slider-output-container-v', children="V lower and upper bounds"),
                dcc.RangeSlider(0, 255, 1, value=[0, 255], id='v-range-slider', marks={
                                0: "0", 255: "100"}, tooltip={'always_visible': True, 'placement': 'bottom'}),
                ]),
            ], width=3),

        dbc.Col([
            html.H3("Region of Interest"),
            html.Div([
                html.Div(id='slider-output-container-upper', children="Upper Crop"),
                dcc.Slider(0, 0.7, value=0.4, id='upper-crop-slider'),
                ]),
                html.Div([
                html.Div(id='slider-output-container-lower', children="Lower Crop"),
                dcc.Slider(0.0, 0.5, value=0.2, id='lower-crop-slider'),
                ]),
                html.Div([
                html.Div(id='slider-output-container-resize', children="Resize"),
                dcc.Slider(0, 1, 1, value=1, id='resize-slider', marks={
                                0: "0", 1: "1"}, tooltip={'always_visible': True, 'placement': 'bottom'}),
                ]),

        ], width=3)
    ]), 
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H1("Fahrt", style={"textAlign": "center"}),
            html.Br(),
            dbc.Row([
                dbc.Col(),
                dbc.Col(html.Button("START", id="start", n_clicks=0, style={"background-color": "green", "padding": "15px 30px"})),
                dbc.Col(html.Button('STOP', id='stop', n_clicks=0, style={"background-color": "red", "padding": "15px 30px"})),
                dbc.Col()
            ])
        ], width=4),
        dbc.Col([
            html.H1("Autoeinstellungen", style={"textAlign": "center"}),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Div(id='dd-angle', children="Auswahl der Lenkmethode"),
                    dcc.Dropdown(['cv2', 'NN'], 'cv2', id='steering-dropdown'),
                    html.Div(id='div-save', children="Speichern des Bildes"),
                    dcc.RadioItems(options = ['Ja', 'Nein'], value='Nein', id='ri-save'),
                ], width=2),
                dbc.Col([
                    html.Div(id='dd-speed', children="Auswahl der Geschwindigkeit"),
                    dcc.Slider(0, 100, value=30, id='speed-slider'),
                ], width=4)
            ])
        ])
    ])

])


# Callbacks: Funktionalität
@app.callback(Output(component_id="angle",component_property="children"),
              [
               Input(component_id="image-dropdown", component_property="value"),
               Input(component_id="upper-crop-slider", component_property="value"),
               Input(component_id="lower-crop-slider", component_property="value"),
               Input(component_id="h-range-slider", component_property="value"),
               Input(component_id="s-range-slider", component_property="value"),
               Input(component_id="v-range-slider", component_property="value"),
               ]
              )
def start_streaming(image, roi_upper, roi_lower, h, s, v):
        car.hsv_lower = np.array([h[0], s[0], v[0]])
        car.hsv_upper = np.array([h[1], s[1], v[1]])
        car.streaming_image = image
        car.roi_upper = roi_upper
        car.roi_lower = roi_lower
        # stream_thread = Thread(target=car.stream)
        # stream_thread.start()

@app.callback(Output(component_id="hidden-div", component_property="children"),
              #Output("ri-save", "value"), 
              Input(component_id="stop", component_property="n_clicks")
              )
def stop_driving(n):
    car.saving = False
    car.stop()
    #return "Nein"

@app.callback(Output(component_id="hidden-div-2", component_property="children"),
              Input(component_id="start", component_property="n_clicks")
              )
def start_driving(n):
    car.drive(30)


@app.callback(Output(component_id="hidden-div-3", component_property="children"),
              Input(component_id="speed-slider", component_property="value")
              )
def start_driving(speed):
    car.speed = int(speed)


@app.callback(Output(component_id="hidden-div-4", component_property="children"),
              Input(component_id="steering-dropdown", component_property="value")
              )
def start_driving(steering):
    car.steering_method = steering

@app.callback(Output(component_id="hidden-div-5", component_property="children"),
              Input(component_id="ri-save", component_property="value")
              )
def start_saving(saving):
    if saving == "Ja":
        car.saving = True
    else:
        car.saving = False


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050)