import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:@localhost/titanic?host=localhost?port=3306')
conn = engine.connect()


results = conn.execute("SELECT * from titanic").fetchall()
df_titanic = pd.DataFrame(data=results, columns = results[0].keys())


results = conn.execute("SELECT * from titanicoutcalc").fetchall()
df_out = pd.DataFrame(data=results, columns = results[0].keys())



app = dash.Dash(__name__)

app.title = 'Ujian Titanic Dashboard'

app.layout = html.Div(children=[
        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(label='Ujian Titanic Database', value='tab-1',children=[
                html.Div([
                html.Div(children=[
                    html.Div([
                        html.P('Table :')
                    ], className='col-1'),
                    html.Div([
                        dcc.Dropdown(
                            id='jenisdf',
                            options=[{'label': i.capitalize(), 'value': i} for i in ['Titanic', 'Titanic Outlier Calculation']],
                            value='Titanic'
                        )
                    ],className='col-3')
                ],className='row'),
                html.H1(
                    id='namaTab1',
                    className='h1',
                    style={'textAlign':'center'}
                    ),
                html.P(
                    id='jmlrow',
                ),
                dcc.Graph(
                id='tableData',
                )
                ])
            ]),
            dcc.Tab(label='Categorical Plot', value='tab-2',children=[
            html.Div([
                html.H1('Categorical Plot Ujian Titanic', 
                className='h1',
                style={'textAlign':'center'}
                ),
                html.Div(children=[
                    html.Div([
                        html.P('Jenis :'),
                        dcc.Dropdown(
                            id='jenisPlot',
                            options=[{'label': i.capitalize(), 'value': i} for i in ['bar','box','violin']],
                            value='bar'
                        )
                    ],className='col-6'),
                    html.Div([
                        html.P('X Axis :'),
                        dcc.Dropdown(
                            id='xaxis',
                            options=[{'label': i.capitalize(), 'value': i} for i in ['survived','sex','ticket class', 'embark town', 'who', 'outlier']],
                            value='survived'
                        )
                    ],className='col-6')
                ],className='row'),
                dcc.Graph(
                    id='categoricalPlot'
                )
            ])
        ])

])
        ])



children='Titanic Database', 


@app.callback(
    Output('namaTab1', 'children'),
    [Input('jenisdf','value')]
)
def updateNama(df):
    dfNama={
        'Titanic' : "Table Titanic",
        'Titanic Outlier Calculation' : "Table Titanic Outlier Calc"
     }
    return dfNama[df]



@app.callback(
    Output('jmlrow', 'children'),
    [Input('jenisdf','value')]
)
def updateRow(df):
    dfNama={
        'Titanic' : len(df_titanic['sex']),
        'Titanic Outlier Calculation' : len(df_out['id'])
     }
    return "Total Row = " + str(dfNama[df])

@app.callback(
    Output('tableData', 'figure'),
    [Input('jenisdf','value')]
)
def updateTable(df) :
    dfNama={
        'Titanic' : df_titanic,
        'Titanic Outlier Calculation' : df_out

    }
    return {
        'data':[
                go.Table(
                    header=dict(values=list(dfNama[df].columns),
                            fill = dict(color='#C2D4FF'),
                            align = ['left'] * 5),
                    cells=dict(values=[dfNama[df][i] for i in dfNama[df].columns],
                            fill = dict(color='#F5F8FF'),
                            align = ['left'] * 5))
                ]
    }



@app.callback(
    Output(component_id='categoricalPlot', component_property='figure'),
    [Input(component_id='jenisPlot', component_property='value'),
    Input('xaxis', 'value')]
)
def update_graph_categorical(jenisPlot, xaxis):
    listGOFunc = {
    "bar": go.Bar,
    "violin": go.Violin,
    "box": go.Box
    }

    xax = {
    'survived': 'survived',
    'sex': 'sex',
    'ticket class': 'class',
    'embark town': 'embark_town',
    'who': 'who',
    'outlier': 'outlier'

    }

    return {
        'data': [listGOFunc[jenisPlot](
                x=df_titanic[xax[xaxis]],
                y=df_titanic['fare'],
                text=df_titanic[xax[xaxis]],
                opacity=0.7,
                name='Fare'
            ),
            listGOFunc[jenisPlot](
                x=df_titanic[xax[xaxis]],
                y=df_titanic['age'],
                text=df_titanic[xax[xaxis]],
                opacity=0.7,
                name='Age'
            )],
        'layout': go.Layout(
                    xaxis={'title': xaxis.capitalize()},
                    yaxis={'title': 'Fare (US$), Age (Year)'},
                    margin=dict(l=40,b=40,t=10,r=10),
                    hovermode='closest',
                    boxmode='group',violinmode='group'
                )
    }


if __name__ == '__main__':
    app.run_server(debug=True,port=1997)

