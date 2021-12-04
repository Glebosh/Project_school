# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import pandas as pd

app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig_one = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
fig_two = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group", color_discrete_sequence=px.colors.sequential.Viridis)

# <div class="row">
#   <div class="column"></div>
#   <div class="column"></div>
# </div>

app.layout = html.Div(
    className="row",
    children=[
        html.Div(
            className="column",
            children=dcc.Graph(
                id='example-graph-one',
                figure=fig_one)
        ),
        html.Div(
            className="column",
            children=dcc.Graph(
                id='example-graph-two',
                figure=fig_two)
        ),   
])

if __name__ == '__main__':
    app.run_server(debug=True)
