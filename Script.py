import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import pandas as pd
from PIL import Image
# import time
# import plotly.express as px
# from skimage import io

# Loopoing over each image
df = pd.read_csv('Data_Base/detection_results.csv')
n_frame = df['n_frame'].values

images = []
for i in range(1, max(df['n_frame'])):
    path_name = 'Data_Base/in5_{}.png'.format(i) 
    img = Image.open(path_name)
    images.append(img)

# Global parameter for image number that is shown
ind = 0

fig = go.Figure(go.Image(z=images[ind]))
fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
fig.update_layout(margin=dict(l=5, r=5, b=10,t=10))


color_mapping = {
                'blue':'#1F77B4',
                'orange':'#FF7F0E',
                'yellow':'#EECA3B'
}

colors = {
    'text': '#000000',
    'background': '#ffffff'
}


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

                html.Div([

                    html.H1(
                        children='Perception',
                        style={
                            'textAlign': 'center',
                            'color': colors['text']
                        }
                    ),

                    html.Br(),

                    html.Div([
                            html.Div([
                                dcc.RadioItems(
                                    id='Left_Image_type',
                                    options=[
                                        {'label': 'Camera Image', 'value': 'camera'},
                                        {'label': 'Deapth Image', 'value': 'depth'},
                                        {'label': 'Lidar Image', 'value': 'Lidar'}],
                                    value='camera',
                                    # style={'width': '100%'},
                                    # style={"padding": "10px", "max-width": "800px", "margin": "auto"},
                                    labelStyle={'display': 'inline-block'}
                            )], style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                            
                            dcc.Graph(
                                    id='Left_perception_graph',
                                    figure=fig
                            ),

                            html.Div([html.H6('Image Display:')],style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                            
                            html.Div([
                                
                                dcc.Checklist(
                                            id='Left_img_display',
                                            options=[
                                                {'label': 'Bounding Boxes   ', 'value': 'bb'},
                                                {'label': 'XYZ   ', 'value': 'XYZ'}],
                                            labelStyle={'display': 'inline-block'}
                                            
                                )],style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                            
                            
                    ],style={'width': '50%', 'float': 'left', 'display': 'inline-block',}),

                    html.Div([
                        
                            html.Div([
                                dcc.RadioItems(
                                    id='Right_Image_type',
                                    options=[
                                        {'label': 'Camera Image', 'value': 'camera'},
                                        {'label': 'Deapth Image', 'value': 'depth'},
                                        {'label': 'Lidar Image', 'value': 'Lidar'}],
                                    value='camera',
                                   
                                    labelStyle={'display': 'inline-block'}
                            )], style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                
                            dcc.Graph(
                                    id='Right_perception_graph',
                                    figure=fig
                            ),
                            
                            html.Div([html.H6('Image Display:')],style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                            
                            html.Div([
                                
                                dcc.Checklist(
                                            id='Right_img_display',
                                            options=[
                                                {'label': 'Bounding Boxes   ', 'value': 'bb'},
                                                {'label': 'XYZ   ', 'value': 'XYZ'}],
                                            labelStyle={'display': 'inline-block'}
                                           
                                )],style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                            
                           
                    ],style={'width': '50%', 'float': 'right', 'display': 'inline-block',}),

                    html.Div([
                            
                            html.Div([
                                
                                html.Button(id='next_button', children='NEXT FRAME', n_clicks=0),
                                
                                dcc.Input(
                                    id='frame_input',
                                    placeholder='Enter frame number...',
                                    type='text',
                                    value=''
                                ),
                                
                                html.Button(id='submit_button', children='SUBMIT'),
                             ], style = {
                                        'width': '100%',
                                        'display': 'flex',
                                        'align-items': 'center',
                                        'justify-content': 'center',
                                        "padding": "20px", "max-width": "800px", "margin": "auto"
                                        }),
                            html.Div(
                                    id='Current_frame_state',
                                    children=html.H6('Current frame number is: 1'),
                                    style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),

                            html.Label('FPS'),
                            dcc.Slider(
                                min=0,
                                max=30,
                                step=None,
                                marks={
                                        0: '0',
                                        5: '0.5',
                                        10: '1',
                                        15: '2',
                                        20: '5',
                                        25: '15',
                                        30: '30'
                                },
                                value=0
                            ), 

                            html.Hr()

                    ])
                    
                ]),

                html.Div([
                    html.H1(
                        children='State Estimation',
                        style={
                            'textAlign': 'center',
                            'color': colors['text']
                        }
                    ),
                ])               
])


def drawRect(fig, df, i):
    fig.add_shape(
                # unfilled Rectangle
                type="rect",
                x0=df['u'][i],
                y0=df['v'][i],
                x1=df['u'][i] + df['w'][i],
                y1=df['v'][i] + df['h'][i],
                line=dict(
                    color=color_mapping[df['type'][i]],
                ),
            )
    return fig

def addId(fig, df, i):
    fig.add_annotation(
                x=df['u'][i] + round(df['w'][i]/2),
                y=df['v'][i],
                text=f"ID:{i}",
                bgcolor=colors['background'],
                bordercolor=colors['text'],
                opacity=0.8,
                ax=1,
                ay=-df['h'][i]/2,
                align="center",
                arrowsize=1,
                arrowwidth=2,
                arrowcolor=colors['text']    
            )
    return fig

def addXYZ(fig, df, i):
    fig.add_annotation(
                x=df['u'][i] + round(df['w'][i]/2),
                y=df['v'][i],
                text=f"X:{df['X'][i]}, Y:{df['Y'][i]}",
                bgcolor='#ffffff',
                bordercolor='#000000',
                opacity=0.8,
                ax=1,
                ay=-df['h'][i]/2,
                align="center",
                arrowsize=1,
                arrowwidth=2,
                arrowcolor=colors['text'] 
                    
            )

def addIdAndXYZ(fig, df, i):
    fig.add_annotation(
                x=df['u'][i] + round(df['w'][i]/2),
                y=df['v'][i],
                text=f"ID:{i}, X:{df['X'][i]}, Y:{df['Y'][i]}",
                bgcolor='#ffffff',
                bordercolor=colors['text'],
                opacity=0.8,
                ax=1,
                ay=-df['h'][i]/2,
                align="center",
                arrowsize=1,
                arrowwidth=2,
                arrowcolor=colors['text'] 
                    
            )

# Perception Left Image Display and Frame Controller - State input does not fire the callback
@app.callback(
            [Output('Left_perception_graph', 'figure'),
            Output('Right_perception_graph', 'figure'),
            Output('Current_frame_state', 'children')],
            [Input('next_button', 'n_clicks'),
            Input('submit_button', 'n_clicks'),
            Input('Left_img_display', 'value'),
            Input('Right_img_display', 'value')],
            [State('frame_input', 'value')])

def update_figure(next_btn, submit_btn, L_selected_display, R_selected_display, submit_num):
    
    global ind

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'next_button' in changed_id:
        ind = ind + 1
    elif 'submit_button' in changed_id:
        ind = int(submit_num) - 1
   

    R_fig = go.Figure(go.Image(z=images[ind]))
    R_fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
    R_fig.update_layout(margin=dict(l=5, r=5, b=10,t=10))

    L_fig = go.Figure(go.Image(z=images[ind]))
    L_fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
    L_fig.update_layout(margin=dict(l=5, r=5, b=10,t=10))

    indices = (n_frame == ind + 1)
    df_tmp = df[indices]
    indexes = df_tmp.index

    # Right Image Editing
    if R_selected_display == ['bb']:
        # Display image with bounding boxes
        for i in indexes:
            drawRect(R_fig, df_tmp, i)
            addId(R_fig, df_tmp, i)   

    elif R_selected_display == ['XYZ']:
        
        # Display image with 3D (x,y) cordinate
        for i in indexes:
            addXYZ(R_fig, df_tmp, i)  

    elif R_selected_display == ['bb', 'XYZ']:
        
        # Display image with bounding boxes and 3D (x,y) cordinate
        for i in indexes:
            drawRect(R_fig, df_tmp, i)
            addIdAndXYZ(R_fig, df_tmp, i)

    elif R_selected_display == ['XYZ', 'bb']:
        
        # Display image with bounding boxes and 3D (x,y) cordinate
        for i in indexes:
            drawRect(R_fig, df_tmp, i)
            addIdAndXYZ(R_fig, df_tmp, i)

    # Left Image Editing
    if L_selected_display == ['bb']:
        # Display image with bounding boxes
        for i in indexes:
            drawRect(L_fig, df_tmp, i)
            addId(L_fig, df_tmp, i)   

    elif L_selected_display == ['XYZ']:
        
        # Display image with 3D (x,y) cordinate
        for i in indexes:
            addXYZ(L_fig, df_tmp, i)  

    elif L_selected_display == ['bb', 'XYZ']:
        
        # Display image with bounding boxes and 3D (x,y) cordinate 
        for i in indexes:
            drawRect(L_fig, df_tmp, i)
            addIdAndXYZ(L_fig, df_tmp, i)

    elif L_selected_display == ['XYZ', 'bb']:
        
        # Display image with bounding boxes and 3D (x,y) cordinate
        for i in indexes:
            drawRect(L_fig, df_tmp, i)
            addIdAndXYZ(L_fig, df_tmp, i)
    
    return L_fig, R_fig, html.H6('Current frame number is: {}'.format(ind + 1))

# # Perception Left Image Display and Frame Controller - State input does not fire the callback
# @app.callback(
#             [Output('Left_perception_graph', 'figure'),
#             Output('Current_frame_state', 'children')],
#             [Input('next_button', 'n_clicks'),
#             Input('submit_button', 'n_clicks'),
#             Input('Left_img_display', 'value')],
#             [State('frame_input', 'value')])

# def update_figure(next_btn, submit_btn, selected_display, submit_num):
    
#     global ind

#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     if 'next_button' in changed_id:
#         ind = ind + 1
#     elif 'submit_button' in changed_id:
#         ind = int(submit_num) - 1
   

#     fig = go.Figure(go.Image(z=images[ind]))
#     fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
#     fig.update_layout(margin=dict(l=5, r=5, b=10,t=10))

#     indices = (n_frame == ind + 1)
#     df_tmp = df[indices]
#     indexes = df_tmp.index

#     if selected_display == ['bb']:
#         # Display image with bounding boxes
#         for i in indexes:
#             drawRect(fig, df_tmp, i)
#             addId(fig, df_tmp, i)   

#     elif selected_display == ['XYZ']:
        
#         # Display image with 3D (x,y) cordinate
#         for i in indexes:
#             addXYZ(fig, df_tmp, i)  

#     elif selected_display == ['bb', 'XYZ']:
        
#         # Display image with bounding boxes and 3D (x,y) cordinate
#         for i in indexes:
#             drawRect(fig, df_tmp, i)
#             addIdAndXYZ(fig, df_tmp, i)

#     elif selected_display == ['XYZ', 'bb']:
        
#         # Display image with bounding boxes and 3D (x,y) cordinate
#         for i in indexes:
#             drawRect(fig, df_tmp, i)
#             addIdAndXYZ(fig, df_tmp, i)
    
#     return fig, html.H6('Current frame number is: {}'.format(ind + 1))


# # Perception Right Image Display and Frame Controller - State input does not fire the callback
# @app.callback(
#             Output('Right_perception_graph', 'figure'),
#             [Input('next_button', 'n_clicks'),
#             Input('submit_button', 'n_clicks'),
#             Input('Right_img_display', 'value')],
#             [State('frame_input', 'value')])

# def update_figure(next_btn, submit_btn, selected_display, submit_num):
    
#     global ind

#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     if 'next_button' in changed_id:
#         ind = ind + 1
#     elif 'submit_button' in changed_id:
#         ind = int(submit_num) - 1
   

#     fig = go.Figure(go.Image(z=images[ind]))
#     fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
#     fig.update_layout(margin=dict(l=5, r=5, b=10,t=10))

#     indices = (n_frame == ind + 1)
#     df_tmp = df[indices]
#     indexes = df_tmp.index

#     if selected_display == ['bb']:
#         # Display image with bounding boxes
#         for i in indexes:
#             drawRect(fig, df_tmp, i)
#             addId(fig, df_tmp, i)   

#     elif selected_display == ['XYZ']:
        
#         # Display image with 3D (x,y) cordinate
#         for i in indexes:
#             addXYZ(fig, df_tmp, i)  

#     elif selected_display == ['bb', 'XYZ']:
        
#         # Display image with bounding boxes and 3D (x,y) cordinate
#         for i in indexes:
#             drawRect(fig, df_tmp, i)
#             addIdAndXYZ(fig, df_tmp, i)

#     elif selected_display == ['XYZ', 'bb']:
        
#         # Display image with bounding boxes and 3D (x,y) cordinate
#         for i in indexes:
#             drawRect(fig, df_tmp, i)
#             addIdAndXYZ(fig, df_tmp, i)
    
#     return fig

# @app.callback(Output('Right perception_graph', 'figure'),
#             [Input('Right img_display', 'value')])

# def update_figure(selected_display):
#     global ind

#     if selected_display == ['bb']:
#         # Display image with bounding boxes
#         fig = go.Figure(go.Image(z=images[ind]))
#         indices = (n_frame == ind + 1)
#         df_tmp = df[indices]

#         for i in range(len(df_tmp['u'])):
#             fig.add_shape(
#                 # unfilled Rectangle
#                 type="rect",
#                 x0=df_tmp['u'][i],
#                 y0=df_tmp['v'][i],
#                 x1=df_tmp['u'][i] + df_tmp['w'][i],
#                 y1=df_tmp['v'][i] + df_tmp['h'][i],
#                 line=dict(
#                     color=color_mapping[df_tmp['type'][i]],
#                 ),
#             )
#             fig.add_annotation(
#                 x=df_tmp['u'][i] + round(df_tmp['w'][i]/2),
#                 y=df_tmp['v'][i],
#                 text=f"ID:{i}",
#                 bgcolor=colors['background'],
#                 bordercolor=colors['text'],
#                 opacity=0.8,
#                 ax=1,
#                 ay=-df_tmp['h'][i]/2,
#                 align="center",
#                 arrowsize=1,
#                 arrowwidth=2,
#                 arrowcolor=colors['text']    
#             )
            
#         fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
#         fig.update_layout(margin=dict(l=5, r=5, b=10,t=10))
   
#     elif selected_display == ['XYZ']:
#         # Display image with 3D (x,y) cordinate
#         fig = go.Figure(go.Image(z=images[ind]))
#         indices = (n_frame == ind + 1)
#         df_tmp = df[indices]

#         for i in range(len(df_tmp['u'])):
           
#             fig.add_annotation(
#                 x=df_tmp['u'][i] + round(df_tmp['w'][i]/2),
#                 y=df_tmp['v'][i],
#                 text=f"X:{df_tmp['X'][i]}, Y:{df_tmp['Y'][i]}",
#                 bgcolor='#ffffff',
#                 bordercolor='#000000',
#                 opacity=0.8,
#                 ax=1,
#                 ay=-df_tmp['h'][i]/2,
#                 align="center",
#                 arrowsize=1,
#                 arrowwidth=2,
#                 arrowcolor=colors['text'] 
                    
#             )
            
    
#         fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
#         fig.update_layout(margin=dict(l=5, r=5, b=10,t=10))

#     elif selected_display == ['bb', 'XYZ']:
#         # Display image with bounding boxes and 3D (x,y) cordinate
#         fig = go.Figure(go.Image(z=images[ind]))
#         indices = (n_frame == ind + 1)
#         df_tmp = df[indices]

#         for i in range(len(df_tmp['u'])):
#             fig.add_shape(
#                 # unfilled Rectangle
#                 type="rect",
#                 x0=df_tmp['u'][i],
#                 y0=df_tmp['v'][i],
#                 x1=df_tmp['u'][i] + df_tmp['w'][i],
#                 y1=df_tmp['v'][i] + df_tmp['h'][i],
#                 line=dict(
#                     color=color_mapping[df_tmp['type'][i]],
#                 ),
#             )
#             fig.add_annotation(
#                 x=df_tmp['u'][i] + round(df_tmp['w'][i]/2),
#                 y=df_tmp['v'][i],
#                 text=f"ID:{i}, X:{df_tmp['X'][i]}, Y:{df_tmp['Y'][i]}",
#                 bgcolor='#ffffff',
#                 bordercolor=colors['text'],
#                 opacity=0.8,
#                 ax=1,
#                 ay=-df_tmp['h'][i]/2,
#                 align="center",
#                 arrowsize=1,
#                 arrowwidth=2,
#                 arrowcolor=colors['text'] 
                    
#             )
            
    
#         fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
#         fig.update_layout(margin=dict(l=5, r=5, b=10,t=10))

#     elif selected_display == ['XYZ', 'bb']:
#         # Display image with bounding boxes and 3D (x,y) cordinate
#         fig = go.Figure(go.Image(z=images[ind]))
#         indices = (n_frame == ind + 1)
#         df_tmp = df[indices]

#         for i in range(len(df_tmp['u'])):
#             fig.add_shape(
#                 # unfilled Rectangle
#                 type="rect",
#                 x0=df_tmp['u'][i],
#                 y0=df_tmp['v'][i],
#                 x1=df_tmp['u'][i] + df_tmp['w'][i],
#                 y1=df_tmp['v'][i] + df_tmp['h'][i],
#                 line=dict(
#                     color=color_mapping[df_tmp['type'][i]],
#                 ),
#             )
#             fig.add_annotation(
#                 x=df_tmp['u'][i] + round(df_tmp['w'][i]/2),
#                 y=df_tmp['v'][i],
#                 text=f"ID:{i}, X:{df_tmp['X'][i]}, Y:{df_tmp['Y'][i]}",
#                 bgcolor='#ffffff',
#                 bordercolor=colors['text'],
#                 opacity=0.8,
#                 ax=1,
#                 ay=-df_tmp['h'][i]/2,
#                 align="center",
#                 arrowsize=1,
#                 arrowwidth=2,
#                 arrowcolor=colors['text'] 
                    
#             )
            
    
#         fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
#         fig.update_layout(margin=dict(l=5, r=5, b=10,t=10))

#     else:

#         fig = go.Figure(go.Image(z=images[ind]))
#         fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
#         fig.update_layout(margin=dict(l=5, r=5, b=10,t=10))

#     return fig


# # Perception Next frame Controller
# @app.callback(
#             [Output('Left perception_graph', 'figure'),
#             Output('Right perception_graph', 'figure'),
#             Output('Current frame state', 'children')],
#             [Input('next_button', 'children')])

# def update_output():
#     Ind = ind + 1
#     fig = go.Figure(go.Image(z=images[ind]))

#     return fig, fig, html.H6('Current frame number is: {}'.format(ind + 1)) 

# # Perception Frame jump Controller - State input does not fire the callback
# @app.callback(
#             [Output('Left perception_graph', 'figure'),
#             Output('Right perception_graph', 'figure'),
#             Output('Current frame state', 'children')],
#             Input('next_button'),
#             State('input-1-state', 'value'))

# def update_output(n_clicks, input1, input2):
#     return u'''
#         The Button has been pressed {} times,
#         Input 1 is "{}",
#         and Input 2 is "{}"
#     '''.format(n_clicks, input1, input2)



# @app.callback(Output('container-button-timestamp', 'children'),
#               [Input('btn-nclicks-1', 'n_clicks'),
#                Input('btn-nclicks-2', 'n_clicks'),
#                Input('btn-nclicks-3', 'n_clicks')])
# def displayClick(btn1, btn2, btn3):
#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     if 'btn-nclicks-1' in changed_id:
#         msg = 'Button 1 was most recently clicked'
#     elif 'btn-nclicks-2' in changed_id:
#         msg = 'Button 2 was most recently clicked'
#     elif 'btn-nclicks-3' in changed_id:
#         msg = 'Button 3 was most recently clicked'
#     else:
#         msg = 'None of the buttons have been clicked yet'
#     return html.Div(msg)

if __name__ == '__main__':
    app.run_server(debug=True)
