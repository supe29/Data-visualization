import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import pycountry_convert as pc
from dash.dependencies import Output, Input

app = dash.Dash(__name__)

summer = pd.read_csv("summer.csv")
dictionary = pd.read_csv("dictionary.csv")
summer = summer.merge(dictionary, left_on='Country', right_on='Code', how='left')
# summer['Population'] = summer.fillna(0)
summer = summer.dropna(subset=['GDP per Capita'])


def convert(row):
    cn_code = pc.country_name_to_country_alpha2(row.Country_y, cn_name_format="default")
    conti_code = pc.country_alpha2_to_continent_code(cn_code)
    return conti_code


summer['continent'] = summer.apply(convert, axis=1)

conti_names = {
    "AS": "Asia",
    "SA": "South America",
    "AS": "Asia",
    "OC": " Oceana",
    "EU": "Europe",
    "NA": "North America",
    "AF": "Africa"
}

summer['continent'] = summer['continent'].map(conti_names)

app.layout = html.Div(children=[
    html.H1(
        children='Medal analysis',
        style={
            'textAlign': 'center'
        }
    ),

    html.Div(children='Dash: The Great Olympians data', style={
        'textAlign': 'center'
    }),

    dcc.Dropdown(id='d', value=[], multi=True,
                 options=[{'label': x, 'value': x} for x in
                          summer.Medal.unique()]),
    html.Div([
        dcc.Graph(id='graph1', figure={}, className='six columns')

    ]),

    dcc.Dropdown(id='b', value=[], multi=True,
                 options=[{'label': x, 'value': x} for x in
                          summer.Country_y.unique()]),
    html.Div([
        dcc.Graph(id='graph2', figure={}, className='six columns')

    ]),

    dcc.Slider(
        summer['Year'].min(),
        summer['Year'].max(),
        step=None,
        value=summer['Year'].min(),
        marks={str(year): str(year) for year in summer['Year'].unique()},
        id='year-slider'
    ),
    html.Div([
        dcc.Graph(id='graph-with-slider', figure={}, className='six columns')
    ]),
dcc.Dropdown(id='c', value=[], multi=True,
                 options=[{'label': x, 'value': x} for x in
                          summer.Year.unique()]),
    html.Div([
        dcc.Graph(id='graph4', figure={}, className='six columns')

    ]),

])


@app.callback(
    [Output(component_id='graph1', component_property='figure'),
     Output(component_id='graph2', component_property='figure'),
     Output(component_id='graph-with-slider', component_property='figure'),
     Output(component_id='graph4', component_property='figure')],
    [Input(component_id='d', component_property='value'),
     Input(component_id='b', component_property='value'),
     Input(component_id='year-slider', component_property='value'),
     Input(component_id='c', component_property='value')]
)
def update_side_graph(opt_select, ctry_select, selected_year, ember):
    dff = summer.copy()

    dff = dff[dff.Medal.isin(opt_select)]
    dff1 = dff[dff.Country_y.isin(ctry_select)]
    filtered_df = dff[dff.Year == selected_year]
    dff2 = dff[dff.Year.isin(ember)]

    # plotly
    fig1 = px.bar(dff, x="Medal", color="Gender", barmode="group",
                  title="Bar Chart to check total no. of Gold, Silver and Bronze medals won gender wise")

    fig2 = px.histogram(dff1, x="Country_y", title='Histogram to check which countries have won the most medals')

    fig = px.scatter(filtered_df, x="GDP per Capita", y="Year",
                     size="GDP per Capita", color="continent",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    fig4 = px.line(dff2, x='Year', color='Gender', title="Line chart to analyze participation each year based on gender")

    return fig1, fig2, fig, fig4


if __name__ == '__main__':
    app.run_server(debug=True)
