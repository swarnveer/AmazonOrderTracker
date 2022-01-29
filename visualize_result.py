import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

def show_graph(df, df2):
    total = df2['Order Value'].sum()
    total = "₹"+str(total)
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    colors = {
        'background': '#F0F8FF',
        'text': '#00008B'
    }
    fig = px.scatter(df, x="Order Date", y='Order Value', color='Order Type', hover_name='Order Name',
           size='Order Value', size_max=60, height=600, width=1000, template='simple_white',
          color_discrete_sequence=px.colors.qualitative.G10, title='Amazon Orders')
    fig2 = px.pie(df2, names="Order Year", values='Order Value', color='Order Value',height=600, width=1000,
                 template='simple_white', color_discrete_sequence=px.colors.qualitative.G10, title='Yearly Orders')
    markdown_text = '''
    ### Amazon Orders summary
    Creator: Swarnveer Singh, [LinkedIn](https://www.linkedin.com/in/swarnveer/), [github](https://github.com/swarnveer)
    '''
    app.layout = html.Div([
        dcc.Markdown(children=markdown_text,
            style={
                'backgroundColor': colors['background'],
                'textAlign': 'center',
                'color': colors['text']
            }),

        dcc.Graph(
            id='orders',
            figure=fig
        ),
        dcc.Graph(
            id='yearly-orders',
            figure=fig2
        ),
        dcc.Textarea(
        id='textarea-example',
        value=f'Total order sum: {total}',
        style={'width': '100%', 'height': 50},
        )
    ])
    app.run_server(debug=True)
