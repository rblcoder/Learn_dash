import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
from sklearn import datasets

iris = datasets.load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target
# 'sepal length (cm)', 'sepal width (cm)', 'petal length (cm)',
#        'petal width (cm)', 'target'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background': '#222222',
    'text': '#7777BF'
}


def generate_table(dataframe):
    return html.Table(
        # Header
        [html.Tr( [html.Th('statistics')] +  [html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr( [html.Td(dataframe.index[i])] + [
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(len(dataframe))], style={
            'justify': 'center',
            'color': colors['text'],
            'width': 'auto'
        }
    )


app.layout = html.Div(children=[

    html.H1(
        children='Iris Data EDA',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Box plots', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'y': df['sepal length (cm)'], 'x': df['target'], 'type': 'box', 'name': 'sepal length (cm)'},
                {'y': df['sepal width (cm)'], 'x': df['target'], 'type': 'box', 'name': 'sepal width (cm)'},
                {'y': df['petal length (cm)'], 'x': df['target'], 'type': 'box', 'name': 'petal length (cm)'},
                {'y': df['petal width (cm)'], 'x': df['target'], 'type': 'box', 'name': 'petal width (cm)'},
            ],
            'layout': {
                # ' plot_bgcolor': colors['background'],
                # 'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                },
                'title': 'Visualize species-vise box plots of features', 'boxmode': 'group'

            }
        }
    ),
    html.Div(children=['Describe', generate_table(df.describe())],
             style={
        'width':'auto',
        'align': 'center',
        'color': colors['text'],
    }),
])
if __name__ == '__main__':
    app.run_server(debug=True)
