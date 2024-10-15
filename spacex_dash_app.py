# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                  dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS SLC 40', 'value': 'CCAFS SLC'},
                                                    {'label': 'CCAFS LC 40', 'value': 'CCAFS LC'},
                                                    {'label': 'KSC LC 39A', 'value': 'KSC'},
                                                    {'label': 'VAFB SLC 4E', 'value': 'VAFB'}
                                                ],
                                                value='ALL',
                                                placeholder="Select Launch site",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site

                                        
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    10000: '10000'},
                                                value=[1000, 6000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total success launches by site')
        return fig
    else:
        data = filtered_df
        if entered_site == 'CCAFS SLC':
            data = data[data['Launch Site'] == 'CCAFS SLC-40']['class'].value_counts()
            fig = px.pie(data, values=data.values,
            names=data.index,  
            title='Success launches by CCAFS SLC-40')
            return fig
        elif entered_site == 'CCAFS LC':
            data = data[data['Launch Site'] == 'CCAFS LC-40']['class'].value_counts()
            fig = px.pie(data, values=data.values,
            names=data.index, 
            title='Success launches by CCAFS LC-40')
            return fig
        elif entered_site == 'KSC':
            data = data[data['Launch Site'] == 'KSC LC-39A']['class'].value_counts()
            fig = px.pie(data, values=data.values,
            names=data.index,  
            title='Success launches by KSC LC-39A')
            return fig
        else:
            data = data[data['Launch Site'] == 'VAFB SLC-4E']['class'].value_counts()
            fig = px.pie(data, values=data.values,
            names=data.index, 
            title='Success launches by VAFB SLC-4E')
            return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_range):
    data = spacex_df
    low, high = payload_range
    mask = (data['Payload Mass (kg)'] > low) & (data['Payload Mass (kg)'] < high)
    if entered_site == 'ALL':
        fig = px.scatter(data[mask], x='Payload Mass (kg)', 
        y='class', color="Booster Version Category",
        title='Correlation between Payload and Success for all sites')
        return fig
    else:
        if entered_site == 'CCAFS SLC':
            data = data[data['Launch Site'] == 'CCAFS SLC-40']
            fig = px.scatter(data[mask], x='Payload Mass (kg)', 
            y='class', color="Booster Version Category",
            title='Correlation between Payload and Success for CCAFS SLC-40')
            return fig
        elif entered_site == 'CCAFS LC':
            data = data[data['Launch Site'] == 'CCAFS LC-40']
            fig = px.scatter(data[mask], x='Payload Mass (kg)', 
            y='class', color="Booster Version Category",
            title='Correlation between Payload and Success for CCAFS LC-40')
            return fig
        elif entered_site == 'KSC':
            data = data[data['Launch Site'] == 'KSC LC-39A']
            fig = px.scatter(data[mask], x='Payload Mass (kg)', 
            y='class', color="Booster Version Category",
            title='Correlation between Payload and Success for KSC LC-39A')
            return fig
        else:
            data = data[data['Launch Site'] == 'VAFB SLC-4E']
            fig = px.scatter(data[mask], x='Payload Mass (kg)', 
            y='class', color="Booster Version Category",
            title='Correlation between Payload and Success for VAFB SLC-4E')
            return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
