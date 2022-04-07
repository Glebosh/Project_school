import io
import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
import functions as func
from dash.dependencies import Input, Output, State

import pandas as pd

data = pd.read_html('report.xls')
df = data[1]

app = dash.Dash(__name__)
server = app.server

fig_one = func.plot_marks(df)
all_subj = func.get_subjects(df)
options = [{'label': i, 'value': i} for i in all_subj]

dropdown = dcc.Dropdown(
        id='dropdown',
        options=options,
        value=all_subj[0]
    )

div = [dropdown, html.P('', id='mark_text'), dcc.Graph(id='graph_subject'), dcc.Graph(id='graph_trend')]
figures_html = html.Div(
    id='figures_row_div',
    className="invisible",
    children=[
        html.Div(
            className="five columns",
            children=dcc.Graph(
                id='graph_months',
                figure=fig_one),
            style={'margin-left': '8.66666666667%'}
        ),
        html.Div(
            className="five columns",
            children=div,
            style={'margin-right': '8.66666666667%'}
        ),  
    ],
    style={
        'margin-top': '50px'
    }
)

text = 'Загрузите свой файл с оценками с сайта sgo.'

file_upload_html = html.Div(className='section', children=[
    html.Div(className='section-heading', children=html.H5(
        id='output-data-upload',
        children=text,
        )),

    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload File', className='button button-primary'),
        # Allow multiple files to be uploaded
        multiple=True
    ),
 ])

app.layout = html.Div(children=[file_upload_html, figures_html])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        data_upload = io.BytesIO(decoded)
        with open("uploud_report.xls", "wb") as f:
            f.write(data_upload.getbuffer())
        data = pd.read_html('uploud_report.xls')
        df = data[1]
        return html.Div(['Upload finished']), df
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])


@app.callback(
    Output('graph_subject', 'figure'),
    Output('mark_text', component_property='children'),
    Output('graph_trend', 'figure'),
    Input('dropdown', 'value'))
def update_figure(value):
    fig_two = func.plot_subject(df, subject=value)

    marks = func.get_marks_for_subject(df, value)
    total = 0
    for mark, count in marks.items():   
        total += int(mark) * count
    mean = total / sum(marks.values())
    emoji = u'\U0001f643' if mean >= 4.5 else u'\U0001f612'
    if mean <= 3.5:
        emoji =  u'\U0001f614'
    mean_str = f'Средний балл по предмету "{value}" за весь год: {mean:.2f} ' + emoji

    fig_three = func.plot_trend(df, value)

    return fig_two, mean_str, fig_three


@app.callback(Output('output-data-upload', 'children'),
              Output('graph_months', 'figure'),
              Output('dropdown', 'options'),
              Output('dropdown', 'value'),
              Output('figures_row_div', 'className'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              Input('output-data-upload', 'children'),
              Input('figures_row_div', 'className'))
def update_output(list_of_contents, list_of_names, list_of_dates, output_div, figures_row_classname):

    if list_of_contents is not None:
        global df
        output_div, df = parse_contents(list_of_contents[-1], list_of_names[-1], list_of_dates[-1])
        output_div = html.Div([''])
        figures_row_classname = 'row'


    all_subj = func.get_subjects(df)
    options = [{'label': i, 'value': i} for i in all_subj]
    fig_months = func.plot_marks(df)

    return output_div, fig_months, options, all_subj[0], figures_row_classname

if __name__ == '__main__':
    app.run_server(debug=True)
