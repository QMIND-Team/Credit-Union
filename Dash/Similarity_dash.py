import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import pickle

KLD = pickle.load(open('KLD_similarity.pkl','rb'))
COS = pickle.load(open('Cosine_similarity.pkl','rb'))
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
            html.P('QMIND Credit Union Team', 
                   style={'color' : colors['text'], 'textAlign' : 'center',
                          'marginBottom' : 0}),
            # Line break
            dcc.Markdown('___'),
            
            # Label and checkboxes
            html.Div([
                    # Label
                    html.Div([
                            html.Label('Enter a Credit Union Identification Number', 
                                       style = {'color' : colors['text']}),
                                       
                            dcc.Input(id = 'input', 
                                      value = 1, 
                                      type='number'),
            
                            ], className='six columns'),
                     
                    # Checkboxes
                    html.Div([
                            html.Label('Similarity Metric:',
                                       style = {'color' : colors['text']}),
                            dcc.Checklist(
                                    options=[
                                            {'label': 'Kullback Lieber Divergence', 
                                             'value': 'kldiv'},
                                            {'label': 'Cosine Similarity', 
                                             'value': 'cossim'}
                                            ],
                                    values=['kldiv', 'cossim'],
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
    df = pd.DataFrame()
    # Getting all of the most similar CUs by KLD
    ID = [KLD[input_value][i][1] for i in range(len(KLD[input_value]))]    
    
    # Collecting the cosine similarity and the KLD similarity
    cos_sim = [COS[input_value][i] for i in range(len(COS[input_value]))]
    kld_sim = [KLD[input_value][i] for i in range(len(KLD[input_value]))]
    
    # ordering the cosine similarity list to have the same order as KLD
    order = {key: i for i, key in enumerate(ID)}
    cos_sim = sorted(cos_sim, key = lambda d: order[d[1]])
    
    #extracting just the values from the similarity metric
    cos_sim_values = ['{0:.2f}'.format(cos_sim[i][0]) for i in range(len(cos_sim))]
    kld_sim_values = ['{0:.2f}'.format(kld_sim[i][0]) for i in range(len(kld_sim))]

    # filling the data frame to use as the table on dash
    df['Credit Union ID'] = ID
    df['Kullback Lieber Divergence'] = kld_sim_values
    df['Cosine Similarity'] = cos_sim_values
    
    # Build table data
    trace = go.Table(
            header = dict(values = list(['Credit Union ID',
                                         'Kullback Lieber Divergence',
                                         'Cosine Similarity']),
                          align = ['left']*5),
            
            cells = dict(values = [df['Credit Union ID'], 
                                   df['Kullback Lieber Divergence'], 
                                   df['Cosine Similarity'],],
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
    