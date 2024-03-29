import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from sklearn import datasets

iris = datasets.load_iris()
breast_cancer = datasets.load_breast_cancer()
dataset_chosen = 'iris'


def load_data(dataset):
    if dataset == 'iris':
        df = pd.DataFrame(iris.data, columns=iris.feature_names)
        df['target'] = iris.target
        targets = list(df['target'].unique())
        target_names = iris.target_names
    else:
        df = pd.DataFrame(breast_cancer.data, columns=breast_cancer.feature_names)
        df['target'] = breast_cancer.target
        targets = list(df['target'].unique())
        target_names = breast_cancer.target_names
    return df, targets, target_names


df, targets, target_names = load_data(dataset_chosen)
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.SOLAR]
                )

body = dbc.Container(
    [html.Div([
        html.Div(
            [
                html.H2("Scatter Plots"),
                html.Br(),
                html.H4('Choose dataset'),
                dcc.Dropdown(
                    id='choose-dataset',
                    options=[{'label': i, 'value': i} for i in ['iris', 'breast cancer']],
                    value='iris'
                ),
                html.Br(),

            ],

        ),

        html.Div([
            html.H4('Select columns to be chosen for X axis and Y axis'), ]),

        html.Div([

            html.Div(
                [html.H6("X: axis")]
            ),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in df.columns[:-1]],
                value=df.columns[0]
            ),
            html.Div(
                [html.Br()]
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            ),
            html.Div(
                [html.Br()]
            ),
        ],
            style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Div(
                [html.H6("Y: axis")]
            ),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in df.columns[:-1]],
                value=df.columns[1]
            ),
            html.Div(
                [html.Br()]
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            ),
            html.Div(
                [html.Br()]
            ),
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

        dbc.Card(
            [dbc.CardHeader("Dynamic scatter plot"),
             dbc.CardBody([dcc.Graph(id='a-scatter-plot')]),
             ]
        ),

        html.Div(
            [html.Br()]
        ),

        dbc.Row(
            [dbc.Col(
                dbc.Card(
                    [dbc.CardHeader("Boxplot of x axis column"),
                     dbc.CardBody([dcc.Graph(id='x-column-box')]),
                     ],
                style={'width': '30rem'},
                ),
                     width="auto"),

             dbc.Col(
                 dbc.Card(
                     [dbc.CardHeader("Boxplot of y axis column"),
                      dbc.CardBody([dcc.Graph(id='y-column-box')]),
                      ],
                style={'width': '30rem', 'float': 'right'},
                 ),
                     width="auto")]
        ),


        dbc.Card(
            [dbc.CardHeader("Histogram of x axis column"),
             dbc.CardBody([dcc.Graph(id='x-column-hist')]),
             ]
        ),

        html.Div(
            [html.Br()]
        ),

        dbc.Card(
            [
                dbc.CardHeader("Histogram of y axis column"),
                dbc.CardBody([dcc.Graph(id='y-column-hist')]),
            ]
        ),
    ]
)

app.layout = html.Div([
    body
], className="mt-4", )


@app.callback(
    Output('xaxis-column', 'options'),
    [Input('choose-dataset', 'value')])
def set_xaxis_column_options(the_dataset):
    global dataset_chosen, df, targets, target_names
    if dataset_chosen != the_dataset:
        dataset_chosen = the_dataset
        df, targets, target_names = load_data(dataset_chosen)
    return [{'label': i, 'value': i} for i in df.columns[:-1]]


@app.callback(
    Output('xaxis-column', 'value'),
    [Input('xaxis-column', 'options')])
def set_xaxis_column_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('yaxis-column', 'options'),
    [Input('xaxis-column', 'value')])
def set_xaxis_column_options(the_dataset):
    return [{'label': i, 'value': i} for i in df.columns[:-1]]


@app.callback(
    Output('yaxis-column', 'value'),
    [Input('yaxis-column', 'options')])
def set_yaxis_column_value(available_options):
    return available_options[1]['value']


@app.callback(
    Output('a-scatter-plot', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),
     Input('choose-dataset', 'value'),
     ])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 choose_dataset,
                 ):
    return {
        'data': [go.Scatter(
            x=df.loc[df['target'] == target, xaxis_column_name],
            y=df.loc[df['target'] == target, yaxis_column_name],
            mode='markers',
            name=target_names[target],
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ) for target in targets],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


@app.callback(
    Output('x-column-hist', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('choose-dataset', 'value'),
     ])
def update_graph_x_hist(xaxis_column_name,
                        choose_dataset,
                        ):
    return {
        'data': [go.Histogram(
            x=df.loc[df['target'] == target, xaxis_column_name],
            name=target_names[target],
        ) for target in targets],
        'layout': go.Layout(
            title=go.layout.Title(
                text=xaxis_column_name),
            hovermode='closest'
        )
    }


@app.callback(
    Output('y-column-hist', 'figure'),
    [Input('yaxis-column', 'value'),
     Input('choose-dataset', 'value'),
     ])
def update_graph_y_hist(yaxis_column_name,
                        choose_dataset,
                        ):
    return {
        'data': [go.Histogram(
            x=df.loc[df['target'] == target, yaxis_column_name],
            name=target_names[target],
        ) for target in targets],
        'layout': go.Layout(
            title=go.layout.Title(
                text=yaxis_column_name),
            hovermode='closest'
        )
    }

@app.callback(
    Output('x-column-box', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('choose-dataset', 'value'),
     ])
def update_graph_x_box(xaxis_column_name,
                        choose_dataset,
                        ):
    return {
        'data': [go.Box(
            y=df.loc[df['target'] == target, xaxis_column_name],
            name=target_names[target],
        ) for target in targets],
        'layout': go.Layout(
            title=go.layout.Title(
                text=xaxis_column_name),
            hovermode='closest'
        )
    }


@app.callback(
    Output('y-column-box', 'figure'),
    [Input('yaxis-column', 'value'),
     Input('choose-dataset', 'value'),
     ])
def update_graph_y_box(yaxis_column_name,
                        choose_dataset,
                        ):
    return {
        'data': [go.Box(
            y=df.loc[df['target'] == target, yaxis_column_name],
            name=target_names[target],
        ) for target in targets],
        'layout': go.Layout(
            title=go.layout.Title(
                text=yaxis_column_name),
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
