from dash import Dash, dcc, html, Input, Output, dash_table
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
        html.Div([html.P("FORMULA 1 RACING DASHBOARD")], style = {"fontSize": "32px","fontWeight": 700,"color": "#dc0f0f", "marginBottom":20}),
        dcc.Tabs(
            id="tabs-example-graph",
            value="tab-1-example-graph",
            children=[
                dcc.Tab(label="Circuits Geo-Scatter", value="tab-1-example-graph"),
                dcc.Tab(label="Speed Trend", value="tab-4-example-graph"),
                dcc.Tab(
                    label="Grid - Position Correlation", value="tab-2-example-graph"
                ),
                dcc.Tab(label="Race Status Trend", value="tab-3-example-graph"),
            ],
        ),
        html.Div(id="tabs-content-example-graph"),
    ],
    style={
        "marginTop": 30,
        "marginBottom": 20,
        "width": "70%",
        "display": "inline-block",
        "padding": "20px",
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
    if tab == "tab-4-example-graph":
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
                html.H6("Country:"),
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
                ),
                dcc.Graph(
                    id="stacked-bar-graph",
                ),
            ]
        )
    elif tab == "tab-1-example-graph":
        return html.Div(
            [
                html.H4("Formula 1 Circuits"),
                dcc.RadioItems(
                    id="radio-button-continent",
                    options=[
                        {"label": "World", "value": "World"},
                        {"label": "Europe", "value": "Europe"},
                        {"label": "Asia", "value": "Asia"},
                        {"label": "North America", "value": "North America"},
                        {"label": "South America", "value": "South America"},
                        {"label": "Australia", "value": "Australia"},
                    ],
                    value="World",
                    inline=True,
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="geo-scatter",
                            hoverData={
                                "points": [{"customdata": ["Circuit de Monaco"]}]
                            }
                            # figure=fig,
                        )
                    ],
                    style={"width": "69%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        # dcc.Graph(
                        #     id="track-facts",
                        #     # figure=fig,
                        # ),
                        html.Div(id="track-facts"),
                    ],
                    style={"width": "29%", "float": "right", "display": "inline-block"},
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
    elif value == "Australia":
        center = go.layout.mapbox.Center(lat=-27, lon=133)
        zoom = 3
    else:
        center = go.layout.mapbox.Center(lat=29, lon=0)
        zoom = 1
    df = pd.read_csv("circuit_stats_v2.csv")
    df["color"] = df["num_races"].fillna(0).replace(np.inf, 0)
    df["size"] = df["num_races"].apply(lambda x: np.log(x) * 3).replace(np.NINF, 0)
    df["races"] = df["num_races"]
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lng",
        hover_name="name",
        hover_data={
            "name": True,
            "location": True,
            "country": False,
            "races": True,
            "size": False,
            "lat": False,
            "lng": False,
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


@app.callback(
    Output("track-facts", "children"),
    Input("geo-scatter", "hoverData"),
)
def check_hover(hoverData):
    hover_part = hoverData["points"][0]["customdata"]
    grand_prix = hover_part[0]

    df = pd.read_csv("circuit_stats_v2.csv")
    df = df.drop(["circuitId", "circuitRef", "alt", "url"], axis=1)
    df = df.rename(
        columns={
            # "name": "Circuit",
            "location": "City",
            "country": "Country",
            "num_races": "Events",
            "driver_name": "Most Successfull Driver",
            "wins": "Sucessful Driver Wins",
            "num_drivers": "Total Drivers Participated",
            "num_constructors": "Total Constructors Participated",
            "winners": "Total Winners",
            "pole_sitters": "Pole Sitters",
        }
    )
    dft = pd.DataFrame()
    dft[["Stat", "Value"]] = df[df["name"] == grand_prix].T.reset_index()
    table_data = dft.to_dict("records")

    #print(f"Hover on Circuit: {hoverData}")
    # figure1 = go.Figure()
    test_html = html.Div(
        [
            html.H4(grand_prix),
            dash_table.DataTable(
                id="memory-table",
                # columns=[
                #     {"name": "Stat", "id": "Stat"},
                #     {"name": "Value", "id": "Value"},
                # ],
                data=table_data,
                style_cell={"textAlign": "left", "padding": "6px"},
                style_as_list_view=False,
                style_header={
                    "backgroundColor": "rgb(232, 232, 232)",
                    "color": "black",
                    "fontSize": "18px",
                    "border": "1px solid grey",
                },
                style_data={
                    "color": "black",
                    "fontSize": "15px",
                    "border": "1px solid grey",
                },
            ),
            # dcc.Graph(id="example-graph", figure=fig),
        ],
        style={
            "marginTop": 55,
        },
    )
    return test_html


app.run_server(debug=True)
