import panel as pan
import pandas as pd
import plotly.graph_objects as go
from jinja2 import Environment, FileSystemLoader
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pywaffle import Waffle

pan.extension("plotly")

data_url = "https://python-graph-gallery.com/wp-content/uploads/gapminderData.csv"
df = pd.read_csv(data_url)
df2 = df[df.continent == "Americas"]

fig = go.Figure(data=go.Heatmap(z=df2.lifeExp, x=df2.year, y=df2.country))

heatmap = pan.panel(fig)

data = df.groupby("continent")["pop"].sum()
data = round((data / data.sum() * 100), 2)
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=data,
    legend={
        "labels": [
            f"{country} ({percent})" for (country, percent) in data.to_dict().items()
        ],
        "loc": "lower left",
        "bbox_to_anchor": (0, -0.8),
        "framealpha": 0,
        # "ncol": len(data),
        "fontsize": 12,
    },
    # icons="thumbs-up",
    figsize=(10, 5),
)
waffle = pan.panel(fig)


env = Environment(loader=FileSystemLoader("."))
jinja_template = env.get_template("custom_template.html")

tmpl = pan.Template(jinja_template)

tmpl.add_panel("A", heatmap)
tmpl.add_panel("B", waffle)
tmpl.servable()
