import pandas as pd
import plotly.graph_objects as go

def get_marks(month):
    marks = {'2': 0, '3': 0, '4': 0, '5': 0}
    for subj in month.index:
        row = month.iloc[subj]
        row = pd.to_numeric(row, errors='coerce')
        row = row.dropna()

        for mark in row.values:
            marks[str(int(mark))] += 1

    return marks


def get_marks_for_subject(df, subject):
    marks = {'2': 0, '3': 0, '4': 0, '5': 0}

    for data in df.iloc:
        if data[0] == subject:
            data = pd.to_numeric(data, errors="coerce")
            data = data.dropna()
            data = data.values[:-1]

            for mark in data:
                marks[str(int(mark))] += 1
    return marks


def get_figure(data: list):
    fig = go.Figure(data=data)

    fig.update_layout(
        title='Отметки за год',
        xaxis=dict(
            title='отметки',
            titlefont_size=16,
            tickfont_size=14,
        ),
        yaxis=dict(
            title='количество отметок',
            titlefont_size=16,
            tickfont_size=14,
        ),
        barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
    )

    return fig


def get_marks_bar(marks: dict, m: str):
    data = go.Bar(
        x=list(marks.keys()),
        y=list(marks.values()),
        name=m
    )
    return data


def plot_marks(df):
    months = set([item[0] for item in df.columns[1:-1]])
    bars = list()
    for m in months:
        marks = get_marks(df[m])
        bar = get_marks_bar(marks, m)
        bars.append(bar)
        
    return get_figure(bars)


def plot_subject(df, subject):
    marks = get_marks_for_subject(df, subject)
    bar = get_marks_bar(marks, subject)
    fig = get_figure([bar])
    fig.update_layout(title=f'Отметки за год по предмету: "{subject}"')
    return fig


def get_subjects(df):
    subjects = list()
    for idx in range(len(df)):
        subjects.append(df.iloc[idx][0])

    return sorted(subjects)


def calculate_average_mark(df, month, subject):
    marks = {'2': 0, '3': 0, '4': 0, '5': 0}
    
    subjects = list()
    for idx in range(len(df)):
        subjects.append(df.iloc[idx][0])

    for subj_idx, s in enumerate(subjects):
        if s == subject:
            break

    row = df[month].iloc[subj_idx]
    row = pd.to_numeric(row, errors='coerce')
    row = row.dropna()

    for mark in row.values:
        marks[str(int(mark))] += 1
    
    total = 0

    for mark, count in marks.items():
        total += int(mark) * count
    avg = total / sum(marks.values())
    return avg


def get_months(df):
    months = [0]
    for col in df.columns[1:-1]:
        if months[-1] != col[0]:
            months.append(col[0])
    months = months[1:]
    return months