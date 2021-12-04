# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import functions as func

import pandas as pd

data = pd.read_html('Отчет об успеваемости и посещаемости ученика.xls')

df = data[1]

app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
#df = pd.DataFrame({
#    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#    "Amount": [4, 1, 2, 2, 4, 5],
#    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
#})

fig_one = func.plot_marks(df)
fig_two = func.plot_subject(df, 'Алгебра')
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
                id='graph_months',
                figure=fig_one)
        ),
        html.Div(
            className="column",
            children=dcc.Graph(
                id='graph_subject',
                figure=fig_two)
        ),   
])

if __name__ == '__main__':
    app.run_server(debug=True)
