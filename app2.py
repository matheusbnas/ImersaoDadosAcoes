
#lib central
import dash

#Elementos do dash
from dash import dcc
from dash import html
#import dash_core_components as dcc #Isso já está em depreciado. Correto seria "from dash import dcc"
#import dash_html_components as html #Isso já está depreciado. Correto seria "from dash import html"
import dash_bootstrap_components as dbc 
from dash.dependencies import Input, Output

#Pacotes de visualização
import plotly.graph_objs as go
import pandas as pd
import yfinance as yf


yf.pdr_override() #Para fazer o carregamento

# Especificar o símbolo da ação e o período de tempo desejado
Simbolo = 'BTC-USD'
Fim = '2021-12-31'
Periodo = '6mo'

# Coletando os dados
Dados = yf.download(Simbolo, period=Periodo)
Dados['Media_Movel'] = Dados['Close'].rolling(window=5).mean()

# Função para atualizar os dados com base no período selecionado
def atualizar_dados(periodo_selecionado):
    global Periodo, Dados
    if periodo_selecionado == '1y':
        Periodo = '1y'
    elif periodo_selecionado == '3mo':
        Periodo = '3mo'
    elif periodo_selecionado == '6mo':
        Periodo = '6mo'

    Dados = yf.download(Simbolo, period=Periodo)
    Dados['Media_Movel'] = Dados['Close'].rolling(window=5).mean()

# Layout do aplicativo. Faz a conexão com o aplicativo dash e os layouts prontos
app = dash.Dash(
    __name__,
    title='Evento Dashboard',
    #Definir os estilos
    #Link dos estilos = https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/
    external_stylesheets=[
        dbc.themes.DARKLY,
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css',
        'https://fonts.googleapis.com/css2?family=Joan&family=Roboto:ital,wght@0,100;1,300&family=Source+Sans+Pro:ital,wght@0,400;1,300&display=swap'
    ]
)

# Gráfico Candlestick
Grafico_Candlestick = go.Figure(
    data=[
        go.Candlestick(
            x=Dados.index,
            open=Dados['Open'],
            high=Dados['High'],
            low=Dados['Low'],
            close=Dados['Close'],
            increasing_line_color='red',
            decreasing_line_color='green'
        )
    ]
)

Grafico_Candlestick.update_layout(
    xaxis_rangeslider_visible=False,
    title='Análise Fechamento',
    xaxis_title='Período',
    yaxis_title='Preço de Fechamento'
)

Grafico_Candlestick.update_layout(
    template="plotly_dark",
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
)

# Gráfico de Linhas
Grafico_Linhas = go.Figure()

Grafico_Linhas.add_trace(go.Scatter(
    x=Dados.index,
    y=Dados['Media_Movel'],
    mode='lines',
    name='Média Móvel',
    line=dict(color='rgb(158, 58, 171)')
))

Grafico_Linhas.add_trace(go.Scatter(
    x=Dados.index,
    y=Dados['Close'],
    mode='lines',
    name='Fechamento',
    line=dict(color='green')
))

Grafico_Linhas.update_layout(
    title='Análise Média Móvel e Fechamento',
    xaxis_title='Período',
    yaxis_title='Preço',
    template='plotly_dark',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1,
        font=dict(size=9)
    )
)

# Layout do aplicativo (FRONT-END)
app.layout = html.Div(
    #Reproduz todos os elementos da página
    children=[
        #Barra superior (NAVBAR)
        html.Div(
            className='navbar navbar-expand-lg bg-primary',
            style={
                'height': 'fit-content',
                #'background': '#111111',
                'display': 'flex',
                'flex-direction': 'row',
                'align-items': 'center',
                'justify-content': 'space-between',
                'border-bottom': '1px solid #4b5460',
                'padding': '1rem 5rem',
                'width': '100%',
            },
            children=[
                html.Div(
                    className='banner-title',
                    children=[
                        html.H5(
                            ['Dashboard'],
                            style={
                                'font-family': 'open sans semi bold, sans-serif',
                                'font-weight': '500'
                            }
                        ),
                        html.H6('Análise BITCOIN')
                    ]
                ),
                html.Div(
                    className='banner-logo',
                    children=[
                        html.Img(src=app.get_asset_url('icone_bitcoin.png'), height='60px', alt='logo')
                    ]
                )
            ]
        ),
        html.Div(
            className="container",
            children=[
                html.Div(
                    [
                        html.Label("Selecione o período", style={'color': 'white'}),
                        dcc.Dropdown(
                            id='periodo-dropdown',
                            options=[
                                {'label': '1 Ano', 'value': '1y'},
                                {'label': '3 Meses', 'value': '3mo'},
                                {'label': '6 Meses', 'value': '6mo'}
                            ],
                            value='6mo',
                            clearable=False,
                            style={ 'color': 'black'},
                            className='custom-dropdown'
                        ),
                    
                    ],
                    className="my-4"
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id='candlestick-chart',
                            figure=Grafico_Candlestick
                        )
                    ],
                    className="my-4"
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id='graph2',
                            figure=Grafico_Linhas
                        )
                    ],
                    className="my-4"
                ),
            ]
        )
    ]
)


@app.callback(
    Output('candlestick-chart', 'figure'),
    Output('graph2', 'figure'),
    Input('periodo-dropdown', 'value')
)
def atualizar_graficos(periodo_selecionado):
    atualizar_dados(periodo_selecionado)

    Grafico_Candlestick = go.Figure(
        data=[
            go.Candlestick(
                x=Dados.index,
                open=Dados['Open'],
                high=Dados['High'],
                low=Dados['Low'],
                close=Dados['Close'],
                increasing_line_color='red',
                decreasing_line_color='green'
            )
        ]
    )

    Grafico_Candlestick.update_layout(
        xaxis_rangeslider_visible=False,
        title='Análise Fechamento',
        xaxis_title='Período',
        yaxis_title='Preço de Fechamento'
    )

    Grafico_Candlestick.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
    )

    Grafico_Linhas = go.Figure()
    Grafico_Linhas.add_trace(go.Scatter(
        x=Dados.index,
        y=Dados['Media_Movel'],
        mode='lines',
        name='Média Móvel',
        line=dict(color='rgb(158, 58, 171)')
    ))

    Grafico_Linhas.add_trace(go.Scatter(
        x=Dados.index,
        y=Dados['Close'],
        mode='lines',
        name='Fechamento',
        line=dict(color='green')
    ))

    Grafico_Linhas.update_layout(
        title='Análise Média Móvel e Fechamento',
        xaxis_title='Período',
        yaxis_title='Preço',
        template='plotly_dark',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(size=9)
        )
    )

    return Grafico_Candlestick, Grafico_Linhas

#Rodar a aplicação
if __name__ == '__main__':
    app.run_server(debug=True)