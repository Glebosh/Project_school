import dash
import dash_core_components as dcc
import dash_html_components as html
import functions as func
from dash.dependencies import Input, Output

import pandas as pd

data = pd.read_html('Отчет об успеваемости и посещаемости ученика.xls')

df = data[1]

app = dash.Dash(__name__)

fig_one = func.plot_marks(df)

all_subj = func.get_subjects(df)
options = [{'label': i, 'value': i} for i in all_subj]

dropdown = dcc.Dropdown(
        id='dropdown',
        options=options,
        value=all_subj[0]
    )

div = [dcc.Graph(id='graph_subject'), dropdown]

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
            children=div 
        ),  
])

@app.callback(
    Output('graph_subject', 'figure'),
    Input('dropdown', 'value')
)
def update_figure(value):
    fig_two = func.plot_subject(df, value)
    return fig_two

if __name__ == '__main__':
    app.run_server(debug=True)
