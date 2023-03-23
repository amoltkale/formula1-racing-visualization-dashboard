from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import configparser

# Reading the configuration
parse = configparser.ConfigParser()
config = parse.read("config.ini")
mapbox_token = parse.get("mapbox", "secret_token")

# app = Dash(__name__)
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)
# app = Dash(__name__, suppress_callback_exceptions=True)


app.layout = html.Div(
    [
        html.H1("FORMULA 1 RACING DASHBOARD"),
        dcc.Tabs(
            id="tabs-example-graph",
            value="tab-1-example-graph",
            children=[
                dcc.Tab(label="Speed Trend", value="tab-1-example-graph"),
                dcc.Tab(
                    label="Grid - Position Correlation", value="tab-2-example-graph"
                ),
                dcc.Tab(label="Race Status Trend", value="tab-3-example-graph"),
                dcc.Tab(label="Geo Scatter", value="tab-4-example-graph"),
            ],
        ),
        html.Div(id="tabs-content-example-graph"),
    ],
    style={
        "marginTop": 30,
        "marginBottom": 20,
        "width": "55%",
        "display": "inline-block",
    },
)


@app.callback(Output("line-graph", "figure"), [Input("my-range-slider", "value")])
def update_line_chart(value):
    df = pd.read_csv("speed_per_circuit.csv")
    # mask = df["count"] >= value[0] & df["count"] <= value[1]
    df = df[df["count"] >= value[0]]
    df = df[df["count"] <= value[1]]
    fig = px.line(
        df,
        x="year",
        y="fastestLapSpeed",
        color="grand_prix",
        hover_name="name_y",
        labels={
            "fastestLapSpeed": "Fastest Lap Speed",
            "year": "Year",
        },
    )
    # fig.update_layout( height=600)
    return fig


@app.callback(
    Output("slider-value", "children"),
    Input("my-range-slider", "value"),
)
def update_slider_value(value):
    # return 'You have selected Option to show circuits with more than **'+str(value)+'** races'
    return (
        "You have selected Grand Prixs with races in range of **"
        + str(value[0])
        + "** to **"
        + str(value[1])
        + "** races"
    )


@app.callback(Output("heatmap-graph", "figure"), Input("pos_radio_buttons", "value"))
def filter_heatmap(positions):
    # df = px.data.medals_wide(indexed=True) # replace with your own data source
    results = pd.read_csv("gridVsPos.csv")
    mask_grid = results["grid"] <= positions
    mask_pos = results["position"] <= positions
    results = results[mask_grid & mask_pos]
    hm_df = pd.pivot_table(
        results, values="freq", index=["grid"], columns=["position"], fill_value=0
    )
    fig = px.imshow(
        hm_df,
        text_auto=True,
        height=600,
        color_continuous_scale="YlOrBr",
        labels={
            "grid": "Grid Position",
            "position": "Final Position",
        },
    )
    return fig


@app.callback(
    Output("tabs-content-example-graph", "children"),
    Input("tabs-example-graph", "value"),
)
def render_content(tab):
    if tab == "tab-1-example-graph":
        return html.Div(
            [
                html.H4(
                    "Fastest Lap Speed For different Race circuits over the years."
                ),
                dcc.Graph(id="line-graph"),
                dcc.RangeSlider(0, 20, 1, value=[5, 15], id="my-range-slider"),
                html.Div(id="output-container-range-slider"),
                dcc.Markdown(id="slider-value"),
            ],
            style={"marginTop": 30},
        )
    elif tab == "tab-2-example-graph":
        return html.Div(
            [
                html.H4("Correlation Between Grid Position and Final Position"),
                dcc.Graph(id="heatmap-graph"),
                html.H6("Number of race positions:"),
                dcc.RadioItems(
                    id="pos_radio_buttons",
                    options=[
                        {"label": "10 Positions", "value": 10},
                        {"label": "15 Positions", "value": 15},
                        {"label": "20 Positions", "value": 20},
                        {"label": "30 Positions", "value": 30},
                    ],
                    value=10,
                    inline=True,
                ),
            ]
        )
    elif tab == "tab-3-example-graph":
        status_df = pd.read_csv("race_final_status_distro.csv")
        return html.Div(
            [
                html.H4("Final Result Status Trend Over Years"),
                html.Div(
                    [html.H6("Select Country:")],
                    style={
                        "width": "10%",
                        "marginBottom": 20,
                        "display": "inline-block",
                    },
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            options=[
                                "All Circuits",
                                "Australia",
                                "Malaysia",
                                "Bahrain",
                                "Spain",
                                "Turkey",
                                "Monaco",
                                "Canada",
                                "France",
                                "UK",
                                "Germany",
                                "Hungary",
                                "Belgium",
                                "Italy",
                                "Singapore",
                                "Japan",
                                "China",
                                "Brazil",
                                "USA",
                                "Austria",
                                "Argentina",
                                "Portugal",
                                "South Africa",
                                "Mexico",
                                "Netherlands",
                                "Sweden",
                                "UAE",
                                "Morocco",
                                "Switzerland",
                                "Korea",
                                "India",
                                "Russia",
                                "Azerbaijan",
                                "Qatar",
                                "Saudi Arabia",
                            ],
                            value=["Monaco"],
                            id="memory-countries",
                            multi=True,
                        )
                    ],
                    style={
                        "width": "90%",
                        "marginBottom": 20,
                        "float": "right",
                        "display": "inline-block",
                    },
                ),
                dcc.Graph(
                    id="stacked-bar-graph",
                ),
            ]
        )
    elif tab == "tab-4-example-graph":
        df = pd.read_csv("circuit_stats.csv")
        df["color"] = df["num_races"].fillna(0).replace(np.inf, 0)
        df["size"] = df["num_races"].apply(lambda x: np.log(x) * 3).replace(np.NINF, 0)
        fig = px.scatter_mapbox(
            df,
            lat="lat",
            lon="lng",
            hover_name="name",
            hover_data={
                "lat": False,
                "lng": False,
                "location": True,
                "size": False,
                "color": False,
            },
            color_discrete_sequence=px.colors.qualitative.Bold,
            color="color",
            # zoom=1,
            height=600,
            size="size",
        )
        fig.update_layout(
            # title = 'F1 Circuits',
            mapbox=dict(
                # style="satellite-streets",
                style="light",
                accesstoken="pk.eyJ1IjoiYW1vbHRrYWxlIiwiYSI6ImNsZmowYjdsNzAxMWg0Mm13MGlwZTR0eDYifQ.oPCEnpIi6t4zHB51yCc1pA",  #
                center=go.layout.mapbox.Center(lat=29, lon=0),
                zoom=1,
            ),
            height=600,
        )
        return html.Div(
            [
                html.H3("Formula 1 Circuits"),
                dcc.RadioItems(
                    id="radio-button-continent",
                    options=[
                        {"label": "World", "value": "World"},
                        {"label": "Europe", "value": "Europe"},
                        {"label": "Asia", "value": "Asia"},
                        {"label": "North America", "value": "North America"},
                        {"label": "South America", "value": "South America"},
                    ],
                    value="World",
                    inline=True,
                ),
                dcc.Graph(
                    id="geo-scatter",
                    # figure=fig,
                ),
            ]
        )


@app.callback(Output("stacked-bar-graph", "figure"), Input("memory-countries", "value"))
def create_stacked_bars(value):
    # df = px.data.medals_wide(indexed=True) # replace with your own data source
    df = pd.read_csv("race_final_status_country.csv")
    # if value!=['All Circuits']:
    if not any("All Circuits" in s for s in value):
        mask = df["country"].isin(value)
        df = df[mask]
    df = df[["resultId", "year", "status"]]
    df = df.groupby(["year", "status"])["resultId"].count().to_frame()
    df.reset_index(inplace=True)
    fig = px.bar(
        df,
        x="year",
        y="resultId",
        color="status",
        # color_discrete_sequence=px.colors.qualitative.G10,
        color_discrete_sequence=px.colors.qualitative.Bold,
        labels={
            "resultId": "Count of Results",
            "year": "Year",
        },
    )
    return fig


@app.callback(Output("geo-scatter", "figure"), Input("radio-button-continent", "value"))
def create_geo_scatter(value):
    if value == "Europe":
        center = go.layout.mapbox.Center(lat=46, lon=3)
        zoom = 3
    elif value == "Asia":
        center = go.layout.mapbox.Center(lat=28, lon=77)
        zoom = 2.8
    elif value == "North America":
        center = go.layout.mapbox.Center(lat=35, lon=-97)
        zoom = 3
    elif value == "South America":
        center = go.layout.mapbox.Center(lat=-35, lon=-58)
        zoom = 3
    else:
        center = go.layout.mapbox.Center(lat=29, lon=0)
        zoom = 1
    df = pd.read_csv("circuit_stats.csv")
    df["color"] = df["num_races"].fillna(0).replace(np.inf, 0)
    df["size"] = df["num_races"].apply(lambda x: np.log(x) * 3).replace(np.NINF, 0)
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lng",
        hover_name="name",
        hover_data={
            "lat": False,
            "lng": False,
            "location": True,
            "size": False,
            "color": False,
        },
        color_discrete_sequence=px.colors.qualitative.Bold,
        color="color",
        # zoom=1,
        # height=600,
        size="size",
    )
    fig.update_layout(
        # title = 'F1 Circuits',
        mapbox=dict(
            # style="satellite-streets",
            style="light",
            accesstoken=mapbox_token,
            center=center,
            zoom=zoom,
        ),
        height=600,
    )
    return fig


app.run_server(debug=True)
