import plotly.express as px
import pandas as pd
from sklearn.datasets import load_wine
from dash import Dash, html, dcc, callback
from dash.dependencies import Input, Output

# Load the wine dataset
def load_data():
    wine = load_wine()
    wine_df = pd.DataFrame(wine.data, columns=wine.feature_names)
    wine_df["WineType"] = [wine.target_names[t] for t in wine.target]
    return wine_df

wine_df = load_data()
ingredients = wine_df.drop(columns=["WineType"]).columns

avg_wine_df = wine_df.groupby('WineType').mean().reset_index()

# Define a darker color palette with shades of purple
color_palette = px.colors.sequential.Purples_r

# Function to create scatter chart
def create_scatter_chart(x_axis="alcohol", y_axis="malic_acid", color_encode=False):
    scatter_fig = px.scatter(
        wine_df, 
        x=x_axis, 
        y=y_axis, 
        color="WineType" if color_encode else None,
        color_discrete_sequence=color_palette,
        title="{} vs {}".format(x_axis.capitalize(), y_axis.capitalize())
    )
    scatter_fig.update_layout(height=300)
    return scatter_fig

# Function to create bar chart
def create_bar_chart(ingredients=["alcohol", "malic_acid", "ash"]):
    bar_fig = px.bar(
        avg_wine_df, 
        x="WineType", 
        y=ingredients, 
        title="Avg Ingredient per Wine Type",
        color_discrete_sequence=color_palette
    )
    bar_fig.update_layout(height=300)
    return bar_fig

# Function to create pie chart
def create_pie_chart():
    pie_fig = px.pie(
        wine_df, 
        names='WineType', 
        title="Distribution of Wine Types",
        color_discrete_sequence=color_palette
    )
    pie_fig.update_layout(height=300)
    return pie_fig

# Function to create box plot chart
def create_box_plot():
    box_fig = px.box(
        wine_df, 
        x="WineType", 
        y="alcohol", 
        title="Alcohol Content Distribution by Wine Type",
        color_discrete_sequence=color_palette
    )
    box_fig.update_layout(height=300)
    return box_fig

# Function to create histogram chart
def create_histogram():
    hist_fig = px.histogram(
        wine_df, 
        x="alcohol", 
        title="Distribution of Alcohol Content",
        color_discrete_sequence=color_palette
    )
    hist_fig.update_layout(height=300)
    return hist_fig

# Function to create line chart
def create_line_chart():
    line_fig = px.line(
        avg_wine_df, 
        x="WineType", 
        y="alcohol", 
        title="Average Alcohol Content per Wine Type",
        color_discrete_sequence=color_palette
    )
    line_fig.update_layout(height=300)
    return line_fig

# Dash app setup
app = Dash(__name__, title="Wine Analysis")

# Widgets
x_axis = dcc.Dropdown(
    id="x_axis", options=[{"label": col, "value": col} for col in ingredients], value="alcohol", clearable=False,
    style={"display": "inline-block", "width": "47%"}
)
y_axis = dcc.Dropdown(
    id="y_axis", options=[{"label": col, "value": col} for col in ingredients], value="malic_acid", clearable=False,
    style={"display": "inline-block", "width": "47%"}
)
color_encode = dcc.Checklist(
    id="color_encode", options=[{'label': 'Color-Encode', 'value': 'Color-Encode'}]
)

multi_select = dcc.Dropdown(
    id='multi_select', options=[{"label": col, "value": col} for col in ingredients], value=["alcohol", "malic_acid", "ash"], clearable=False, multi=True
)

# Web app layout
app.layout = html.Div(
    children=[
        html.H1("Wine Analysis Dashboard", style={"text-align": "center", "font-family": "Roboto"}),
        html.Div(
            "Explore relationships between various ingredients used in the creation of three different types of wine", 
            style={"text-align": "center", "font-family": "Roboto"}
        ),
        html.Br(),
        html.Div(
            children=[
                html.Div(
                    children=[
                        x_axis, y_axis, color_encode,
                        dcc.Graph(id="scatter_chart", figure=create_scatter_chart())
                    ],
                    className="chart-box"
                ),
                html.Div(
                    children=[
                        multi_select, html.Br(),
                        dcc.Graph(id="bar_chart", figure=create_bar_chart())
                    ],
                    className="chart-box"
                ),
                html.Div(
                    children=[
                        dcc.Graph(id="pie_chart", figure=create_pie_chart())
                    ],
                    className="chart-box"
                ),
            ],
            className="chart-row"
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Graph(id="box_plot", figure=create_box_plot())
                    ],
                    className="chart-box"
                ),
                html.Div(
                    children=[
                        dcc.Graph(id="histogram", figure=create_histogram())
                    ],
                    className="chart-box"
                ),
                html.Div(
                    children=[
                        dcc.Graph(id="line_chart", figure=create_line_chart())
                    ],
                    className="chart-box"
                ),
            ],
            className="chart-row"
        )
    ],
    style={"padding": "20px"}
)

# Callbacks
@callback(
    Output('scatter_chart', "figure"),
    [Input("x_axis", "value"), Input("y_axis", "value"), Input("color_encode", "value")]
)
def update_scatter_chart(x_axis, y_axis, color_encode):
    return create_scatter_chart(x_axis, y_axis, color_encode)

@callback(
    Output('bar_chart', "figure"),
    [Input('multi_select', "value")]
)
def update_bar_chart(ingredients):
    return create_bar_chart(ingredients)

if __name__ == "__main__":
    app.run_server(debug=True)
