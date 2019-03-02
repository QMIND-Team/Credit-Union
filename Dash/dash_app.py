import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

# Import dataframe data
df = pd.read_pickle('CU_locations.p')

# Html Stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Intialize app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Text and background color selection
colors = {
    'background': '#273746',
    'text': '#7FDBFF'
}


# Define app layout   
app.layout = html.Div(children=[
        # Header
        html.H3('Credit Union Analysis Tool', 
                style={'color' : colors['text'], 'textAlign' : 'center',
                       'marginBottom' : 0}),
        # Description
        html.Div([
            html.P('''A web application for evaluation and 
                   comparison of Canadian credit unions.''',
                   style={'color' : colors['text'], 
                          'fontSize' : 15, 'textAlign' : 'center'}),
            # Author 
            html.P('Developed by: QMIND Credit Union Analysis Team', 
                   style={'color' : colors['text'], 'textAlign' : 'center',
                          'marginBottom' : 0}),
            # Line break
            dcc.Markdown('___'),
            
            # Label and checkboxes
            html.Div([
                    # Label
                    html.Div([
                            html.Label('Enter a Credit Union Routing Number:', 
                                       style = {'color' : colors['text']}),
                                       
                            dcc.Input(id = 'input', 
                                      value = 80900140, 
                                      type='number'),
            
                            ], className='six columns'),
                     
                    # Checkboxes
                    html.Div([
                            html.Label('Select Categories that you wish to consider:',
                                       style = {'color' : colors['text']}),
                            dcc.Checklist(
                                    options=[
                                            {'label': 'Financials', 
                                             'value': 'fin'},
                                            {'label': u'Demographics', 
                                             'value': 'demo'},
                                            {'label': 'Location', 
                                             'value': 'loc'},
                                            {'label': 'Size',
                                             'value': 'size'}
                                            ],
                                    values=['loc', 'size'],
                                    style = {'color' : colors['text']}),
                            ], className='six columns'),
                    ], className = 'row'
            ),
            
            # Description
            html.Label('''The following credit unions most closely 
                    match your criterion:''',
                    style = {'color' : colors['text'], 'marginTop' : 10}),   
            
            # Table 
            dcc.Graph(id = 'interactive_table')
            
        ])
], style = {'backgroundColor' : colors['background'], 'marginBottom': 0, 'marginTop': 0})

# CSS style sheet for rows and columns
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})    

# Callback functions for interactive capabilites 
@app.callback(
        dash.dependencies.Output(component_id = 'interactive_table', 
                                 component_property = 'figure'),
                                 
        [dash.dependencies.Input(component_id = 'input', 
                                 component_property = 'value')])

# Figure update based on callback
def update_figure(input_value):
    # New data frame ordering
    filtered_df = df.loc[(df['RN'] - input_value).abs().argsort()]  
    
    # Build table data
    trace = go.Table(
            header = dict(values = list(['Routing Number',
                                    'Electronic Paper',
                                    'Postal Address',
                                    'Postal Code',
                                    'Credit Union Name']),
                          align = ['left']*5),
            
            cells = dict(values = [filtered_df.RN[:10], 
                                   filtered_df.EP[:10], 
                                   filtered_df.PA[:10], 
                                   filtered_df.PC[:10], 
                                   filtered_df.CU[:10]],
                         align = ['left']*5)
    )
    
    # Return the table data and the desired layout
    return {'data' : [trace],
            'layout' : go.Layout(
                    margin = {'l' : 0, 'b' : 0, 't' : 25, 'r' : 0}),
                    }

 
# Run the app!!   
if __name__ =='__main__':
    app.run_server(debug = False)
    