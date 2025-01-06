from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])  # Inicialización de la app Dash

df = pd.read_csv('./data/Student Depression Dataset.csv')  # Leemos la base de datos

# Definir el layout de la aplicación Dash
app.layout = html.Div([
    html.H1("Dashboard Interactivo"),

    # Selector de categorías
    html.Label("Selecciona una ciudad:"),
    # Dropdown para seleccionar una ciudad
    dcc.Dropdown(
        id='city-dropdown',
        options=[{'label': city, 'value': city} for city in sorted(df['City'].unique())],
        value=df['City'].unique()[0],  # Valor inicial
        multi=False  # No es multi selección, solo un valor
    ),

    # Gráfico
    dcc.Graph(id="bar-chart"),
    dcc.Graph(id="scatter-plot"),
    dcc.Graph(id="scatter-plot1"),
    dcc.Graph(id="bar1-chart"),
])

# Callback para actualizar el gráfico en función de la ciudad seleccionada
@app.callback(
    Output("bar-chart", "figure"),
    Output("scatter-plot", "figure"),
    Output("scatter-plot1", "figure"),
    Output("bar1-chart", "figure"),  # Aquí se ha corregido el error de sintaxis
    Input("city-dropdown", "value"),
)
def update_graphs(selected_city):  # Función para hacer los gráficos
    # Filtramos los datos según la ciudad seleccionada
    filtered_df = df[df['City'] == selected_city]
 
    # Crear el gráfico de barras
    bar_fig = px.bar(filtered_df, x="Gender", y="Age", color="Study Satisfaction",
                     title=f"Distribución de Edad por Género en {selected_city}")
    
    # Gráfico de dispersión
    scatter_fig = px.scatter(filtered_df, x="CGPA", y="Study Satisfaction", color="Study Satisfaction", 
                              title="Relación entre CGPA y Satisfacción con el Estudio")
    
    # Gráfico de dispersión1
    scatter_fig1 = px.scatter(filtered_df, x="Family History of Mental Illness", y="id", color="Family History of Mental Illness", 
                              title="Porcentaje de Personas con Historia Familiar de Enfermedades Mentales según Depresión")
    
    # Gráfico de barras apiladas
    bar_fig1 = px.bar(filtered_df, x="Family History of Mental Illness", 
                    y="id", 
                    color="Family History of Mental Illness", 
                    title="Porcentaje de Personas con Historia Familiar de Enfermedades Mentales según Depresión", 
                    barmode='stack')

    return bar_fig, scatter_fig, scatter_fig1, bar_fig1

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)
