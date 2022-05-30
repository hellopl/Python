from dash import Dash, html, dcc
import dash
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State


df = pd.read_csv('user_product_data.csv', header=1, names=['user', 'year', 'month', 'Products', 'score'])
#fig = px.bar(df, x='user', y = 'year')
print(df.head)
app = Dash(__name__)

app.layout = html.Div([html.Div('hello KURS!'),
    html.H1('Choose user'), 
    html.Div(dcc.Dropdown(id='users-dropdown', options=[{'label':i, 'value':i} for i in df.user.unique()], value=["Eve","Tom","Amy"], multi=True)),
    html.H1('Choose year'),
    html.Div(dcc.Checklist(id ='years-checklist', options=[{'label':u, 'value':u} for u in df.year.unique()])),
    html.H1('Choose product'),
    html.Div(dcc.Checklist(id ='product-checklist', options=[{'label':k, 'value':k} for k in df.Products.unique()])),
    dcc.Graph(id = 'meanscore_new', figure={})                                    
])


@app.callback(
     Output(component_id= 'meanscore_new', component_property= 'figure'),
     [Input(component_id= 'years-checklist', component_property= 'value'),   
      Input(component_id= 'users-dropdown', component_property= 'value'),
      Input(component_id= 'product-checklist', component_property= 'value')],
    prevent_initial_call=True
)              
def update_means_score(year_chosen, user_chosen, product_chosen):
    if len(user_chosen) > 0:
        print(f"value user chose: {user_chosen}")
        print(type(user_chosen))
        print(f"value user chose: {year_chosen}")
        print(type(year_chosen))
        print(f"value user chose: {product_chosen}")
        print(type(product_chosen))
        sdf = df[(df["user"].isin(user_chosen)) &
                 (df["year"].isin(year_chosen)) &
                 (df["Products"].isin(product_chosen))]
        fig = px.pie(sdf, values="score", names="user", title=f'{round(sdf.score.mean(),6)} Mean score for selected users')
        return fig
    elif len(user_chosen) == 0:
        raise dash.exceptions.PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)


