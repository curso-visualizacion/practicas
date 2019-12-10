# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import dash_table

# Define dataset
tips = px.data.tips()

#Define options for dropdown selects
col_options = [dict(label=x, value=x) for x in tips.columns]
dimensions = ["x", "y", "color", "facet_col", "facet_row", "size"]

# Define external stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Crete application object
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Create application layout with a DIV containing all other elements
app.layout = html.Div(
    [
        # Header or Title
        html.H1("Demo: Plotly Express in Dash with Tips Dataset"),
        # Div containing dropdown selects
        html.Div(
            [
                html.P([d + ":", dcc.Dropdown(id=d, options=col_options)])
                for d in dimensions
            ],
            style={"width": "25%", "float": "left"}, # style of this div
        ),

        # Graph object is created empty and plot is drawn with a callback
        dcc.Graph(id="graph", style={
                  "width": "75%", "display": "inline-block"}),

        # Subtitle
        html.H3("Explore data"),

        # Datatable
        dash_table.DataTable(
            id="datatable",
            columns=[
                {"name": i, "id": i} for i in sorted(tips.columns)
            ],
            page_current=0,
            page_size=5,
            page_action='custom',
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
        )
    ]
)

"""
This callback populates the graph object defined in the layout. 
In Output(id, comp) we define the id of the graph object in the html and a component inside 
the graph to 'insert' the scatter plotly object, in this case it is a 'figure'.

In Input(object, value) we define what are the input arguments for the make_figure function.
"""
@app.callback(Output("graph", "figure"), [Input(d, "value") for d in dimensions])
def make_figure(x, y, color, facet_col, facet_row, size):
    scatter = px.scatter(
        tips,
        x=x,
        y=y,
        color=color,
        facet_col=facet_col,
        facet_row=facet_row,
        height=700,
        size=size
    )
    return scatter


@app.callback(
    Output('datatable', 'data'),
    [Input('datatable', "page_current"),
     Input('datatable', "page_size")])
def update_table(page_current, page_size):
    return tips.iloc[
        page_current*page_size:(page_current + 1)*page_size
    ].to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
