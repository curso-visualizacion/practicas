# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import dash_table
from pywaffle import Waffle
import plotly.tools as tools
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud, STOPWORDS
from io import BytesIO
import base64
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def fig_to_uri(in_fig, close_all=True, **save_args):
    # type: (plt.Figure) -> str
    """
    Save a figure as a URI
    :param in_fig:
    :return:
    """
    out_img = BytesIO()
    in_fig.savefig(out_img, format='png', **save_args)
    if close_all:
        in_fig.clf()
        plt.close('all')
    out_img.seek(0)  # rewind file
    encoded = base64.b64encode(out_img.read()).decode(
        "ascii").replace("\n", "")
    return "data:image/png;base64,{}".format(encoded)


def create_wordcloud():
    text = open('./alice_novel.txt').read()
    stopwords = set(STOPWORDS)
    wc = WordCloud(background_color="white", max_words=2000,
                   stopwords=stopwords, contour_width=3, contour_color='steelblue')
    wc.generate(text)
    fig = plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    return fig_to_uri(fig)


def create_waffle():
    data = {'Category 1': 48, 'Category 2': 46, 'Category 3': 3}
    fig = plt.figure(
        FigureClass=Waffle,
        rows=5,
        values=data,
        colors=("#983D3D", "#232066", "#DCB732"),
        title={'label': 'Example of Waffle Chart', 'loc': 'left'},
        labels=["{0} ({1}%)".format(k, v) for k, v in data.items()],
        legend={'loc': 'lower left', 'bbox_to_anchor': (
            0, -0.4), 'ncol': len(data), 'framealpha': 0},
        figsize=(9, 6)
    )
    return fig_to_uri(fig)


def create_heatmap():
    fig = go.Figure(data=go.Heatmap(
        z=[[1, 20, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, -10, 20]],
        x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        y=['Morning', 'Afternoon', 'Evening']))
    return fig


def create_matplotlib():
    np.random.seed(19680801)
    N = 50
    x = np.random.rand(N)
    y = np.random.rand(N)
    colors = np.random.rand(N)
    area = (30 * np.random.rand(N))**2
    fig = plt.figure(figsize=(10,5))
    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    return tools.mpl_to_plotly(fig)


tips = px.data.tips()
def create_datatable():
    return dash_table.DataTable(
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
        style_table={'display': 'inline-block', 'align': 'center'}
    )


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1("Demo: Matplotlib and Plotly in Dash",
                style={'textAlign': 'center'}),
        html.H3("Waffle Chart", style={'textAlign': 'center'}),
        html.Div([html.Img(id='waffle', src=create_waffle())],
                 id='waffle_div', style={'textAlign': 'center'}),
        html.H3("WordCloud", style={'textAlign': 'center'}),
        html.Div([html.Img(id='wordcloud', src=create_wordcloud())],
                 id='wordcloud_div', style={'textAlign': 'center'}),
        html.H3("Heatmap", style={'textAlign': 'center'}),
        html.Div([dcc.Graph(figure=create_heatmap(), style={'width': '50%', 'display': 'inline-block'})], style={
                 'textAlign': 'center'}),
        html.H3("Alternative way for matplotlib plots",
                style={'textAlign': 'center'}),
        html.Div([dcc.Graph(figure=create_matplotlib(), style={'width': '50%', 'display': 'inline-block'})], style={
                 'textAlign': 'center'}),
        html.H3("Data Table", style={'textAlign': 'center'}),
        html.Div([create_datatable()], style={'width': '100%'})

    ],
)


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
