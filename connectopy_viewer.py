#!/usr/bin/env python
# coding: utf-8

# In[9]:


from jupyter_dash import JupyterDash
import dash_bootstrap_components as dbc

import dash
from dash import dcc, html, no_update

import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import shutil


# In[11]:


JupyterDash.infer_jupyter_proxy_config()


# In[15]:


#load data
df_z2 = pd.read_csv(r"input/df_z2.csv")
df_z4 = pd.read_csv(r"input/df_z4.csv")


# In[16]:


# convert column of diagnosis to int
df_z2 = df_z2.astype({'group':'str'})
df_z4 = df_z4.astype({'group':'str'})


# In[17]:


def returnSlice(df):
    return df[(df['vine_scores'] != 777) & (df['vine_scores'] != 999) & (df['vine_scores'] != 0)]


# In[18]:


#len(returnSlice(df_z2).sbj_id.values)


# In[1]:


# for sbj_id in returnSlice(df_z2).sbj_id.values:
#     print(sbj_id)
#     shutil.copy("P:\\3022036.01\\congrads\\hariri_wave1\\" + str(int(sbj_id))+ "\\hariri_inverted_L_NO_GR1.png",
#                "C:\\Users\\chrisa\\Desktop\\CODE\\conviewer\\input\\figures\\" + str(int(sbj_id)) + "_hariri_inverted_L_NO_GR1.png")


# In[2]:


# #test for one subject
# sbj_id = 104324981539
# shutil.copy("P:\\3022036.01\\congrads\\hariri_wave1\\" + str(sbj_id)+ "\\hariri_inverted_L_NO_GR1.png",
#                "C:\\Users\\chrisa\\Desktop\\CODE\\conviewer\\input\\figures\\" + str(sbj_id) + "_hariri_inverted_L_NO_GR1.png")


# TODO   
# (1) change the value of 1 and 2 in diagnostic group, perhaps in sex as well (maybe check all columns)   
# (2) age should be in years  

# In[19]:


df_z2_slice = returnSlice(df_z2).reset_index(drop=True)
df_z4_slice = returnSlice(df_z4).reset_index(drop=True)


# In[20]:


df_z2_slice['group'] = df_z2_slice['group'].replace({"1.0":"TD", "2.0":"ASD"})
df_z4_slice['group'] = df_z4_slice['group'].replace({"1.0":"TD", "2.0":"ASD"})


# In[4]:


# df_z2_slice


# In[21]:


def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


# In[23]:


#https://stackoverflow.com/questions/70050831/plotly-dash-scatter-plot-pointnumber-is-assigned-to-multiple-points-in-hover-da
import base64
app = JupyterDash(external_stylesheets=[dbc.themes.BOOTSTRAP])

fig = px.scatter(df_z2_slice, x="vine_scores", y="coef_values", color='group', color_discrete_sequence=['royalblue', 'darkkhaki'],
                 labels={'vine_scores':'Vineland-II Daily Living Scores', 'group':'Diagnostic Group',
                        'coef_values':"TSM Coefficient"},
                 custom_data=['age','sbj_id'])

# fig.update_traddces(
#     hovertemplate="<br>".join([
#         "vine_scores: %{x}",
#         "Coef_values: %{y}",
#         "Age: %{customdata[0]}",
#         "ID: %{customdata[1]}"
#     ])
# )

fig.update_traces(hoverinfo="none", hovertemplate=None)

app.layout = dbc.Container([
    html.H1(children='Connectopy Viewer'),
    dcc.Dropdown(["TSM Coefficient z^2","TSM Coefficient z^4"], "TSM Coefficient z^2" , 
                 id='coef-dropdown'),
#     html.H3(children=["TSM Coefficient z",html.Sup(2)]),
    dcc.Graph(
        id='graph',
        figure=fig,
        clear_on_unhover=True,
    ),
    dcc.Tooltip(id='graph-tooltip'),
    html.Div(id='img-id',style={"width": "100%"})
])

# @app.callback(
#     Output("graph-tooltip","show"),
#     Output("graph-tooltip", "bbox"),
#     Output("graph-tooltip", "children"),
#     Input("graph", "hoverData")
# )

# def display_hover(hoverData):
#     if hoverData is None:
#         return False, no_update, no_update

#     pt = hoverData["points"][0]
#     bbox = pt["bbox"]
#     num = pt["pointNumber"]
#     sbj_id = pt["customdata"][1]

#     df_row = df_z2_slice.iloc[num]
    
#     name = str(int(df_row['sbj_id']))

#     img_src = "C:\\Users\\chrisa\\Desktop\\CODE\\conviewer\\input\\figures\\" + name + "_hariri_inverted_L_NO_GR1.png"

#     children = [
#         html.Div([
#             html.Img(src=b64_image(img_src), style={"width": "100%"}),
#             html.H2(f"{name}", style={"color": "black"}),
#             #html.P(f"{form}"),
#         ], style={'width':'900px', 'white-space': 'normal', 'overflow': 'left'})
#     ]
#     #print(img_src)
#     #img = b64_image(img_src)
#     return True, bbox, children

@app.callback(
    Output("img-id","children"),
    Input("graph", "hoverData")
)
def update_img(hoverData):
    if hoverData is None:
        return no_update

    pt = hoverData["points"][0]
    bbox = pt["bbox"]
    num = pt["pointNumber"]
    sbj_id = pt["customdata"][1]

    df_row = df_z2_slice.iloc[num]
    
    name = str(int(df_row['sbj_id']))

    img_src = "input/figures/" + name + "_hariri_inverted_L_NO_GR1.png"
    children = [
        html.Div([
            html.H2(f"{name}", style={"color": "black"}),
            html.Img(src=b64_image(img_src), style={"width": "100%",'background-color':'#cccccc'}),
        ], style={'width':'900px', 'white-space': 'normal'})
    ]
    return children

@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('coef-dropdown', 'value')])
def update_output(value):
    if value == "TSM Coefficient z^2":
        fig = px.scatter(df_z2_slice, x="vine_scores", y="coef_values", color='group', color_discrete_sequence=['royalblue', 'darkkhaki'],
                 labels={'vine_scores':'Vineland-II Daily Living Scores', 'group':'Diagnostic Group',
                        'coef_values':"TSM Coefficient"},
                 custom_data=['age','sbj_id'])
    elif value == "TSM Coefficient z^4":
        fig = px.scatter(df_z4_slice, x="vine_scores", y="coef_values", color='group', color_discrete_sequence=['royalblue', 'darkkhaki'],
                 labels={'vine_scores':'Vineland-II Daily Living Scores', 'group':'Diagnostic Group',
                        'coef_values':"TSM Coefficient"},
                 custom_data=['age','sbj_id'])
    return fig

if __name__ == "__main__":
    app.run_server(debug=True, mode='inline')


# In[5]:


# df_z2_slice


# In[6]:


# {'points': [{'curveNumber': 1, 'pointNumber': 55, 'pointIndex': 55, 'x': 42, 'y': -0.00830255, 'bbox': {'x0': 203.54000000000002, 'x1': 209.54000000000002, 'y0': 359.89, 'y1': 365.89}, 'customdata': [10670, 631415270075]}]}


# In[19]:


# df_z2_test = df_z2.astype({'group':'int'})


# In[7]:


# returnSlice(df_z2).head()


# In[48]:


# app = JupyterDash(__name__)
# app.layout = html.Div([
#     html.H1("Connectopy Viewer"),
#     dcc.Graph(id='graph'),
#     html.Label([
#         "colorscale",
#         dcc.Dropdown(
#             id='colorscale-dropdown', clearable=False, value='plasma'
# #             value='plasma', options=[
# #                 {'label': c, 'value': c}
# #                 for c in px.colors.named_colorscales()
#              )
#     ]),
# ])# Define callback to update graph
# @app.callback(
#     Output('graph', 'figure'),
#     [Input("colorscale-dropdown", "value")]
# )
# def update_figure(colorscale):
#     return px.scatter(
#         df_z2_slice, x="vine_scores", y="coef_values", color="group",
# #         color_discrete_sequence=px.colors.qualitative.G10,
#         render_mode="webgl", title='TSM Coefficient z^2'
#     )# Run app and display result inline in the notebook
# app.run_server(mode='inline')


# In[ ]:


#check if the number of the subjects correspond to the correct one 

