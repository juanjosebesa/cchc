import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

SENDER_COLUMN = 'sender'
MSG_ID_COLUMN = 'msg_id'
REGION_COLUMN = 'region'
COMUNA_COLUMN = 'comuna'
CAT2_COLUMN = 'cat2'
CAT3_COLUMN = 'cat3'
PERCENTAGE_COLUMN = 'percentage'

# Ayudas
REGION_FILTER_HELP = "ayuda 1"
COMUNA_FILTER_HELP = "ayuda 2"
TEMA_FILTER_HELP = "ayuda 3"
HELP_TEXT_1 = """Bienvenido al análisis de temas relevantes para la comunidad a partir de información de las Redes Sociales que la Camara Chilena de la Construcción ha preparador para sus socios. El objetivo es que puedas seleccionar tu región y/o comunas, y asi puedas ver cuales son los temas más relevantes para la comunidad."""
HELP_TEXT_2 = """La idea primero es explicarte como trabajar en el Dashboard que puedes observar cuando hagas click en "Empezar Análisis".

Lo primero que veras sera dos filtros de Región y Comuna a la izquierda y un grafico de temas a la derecha. Ese gráfico muestra el total de mensajes sobre cada tema a nivel nacional. En los filtros se pueden elegir uno o mas regiones y/o comunas. Al seleccionar algo, el cambio de temas será filtrado por las localidades seleccionadas.

Habiendo elegido alguna localidad, aparecera un filtro adicional y dos gráficos mas en la parte inferior. Estos gráficos presentan indicadores relacionados a los subtemas de las temáticas anteriores. El gráfico de la izquierda muestra un indice de relevancia del subtema, el cual muestra que tan diferente es la distribución de un subtema con respecto a la media nacional. Con esto se puede tener una idea de que subtema es relativamente más relevante para la localidad seleccionada. Por otro lado, el gráfico de la derecha muestra la cantidad total de mensajes por subtema. En ambos gráficos, los colores relacionan los subtemas a los temas generales con los mismo colores del primera gráfico de temas.

Adicionalmente, si desea ver solo los subtemas de una temática general en especifica, puede usar el filtro para solo observar esa temática.

Ahora, para continuar, por favor hacer click en "Empezar Análisis" en la parte superior."""
HELP_TEXT_INTRO = """El impacto social de las empresas es un valor que ha crecido de manera extraordinaria. Incluso es considerada la gran revolución empresarial del siglo XXI.
 
Hoy en día las organizaciones competitivas deben alinear su misión y operaciones con las demandas de la sociedad, sobre todo en temas sociales y medioambientales. Cuando los valores de la empresa se conectan con los grupos de interés y con la sociedad en general, ésta además de convertirse en un aporte positivo hacia la comunidad, se hace más rentable y atractiva en la captación de talentos, hacia sus clientes y ante inversores. 
 
Las Redes Sociales constituyen hoy en día la principal fuente de información. Esta ha sido la gran herramienta para comunicarnos, generándose en época de pandemia un crecimiento explosivo de ellas. Por este motivo, para efectos de conocer las necesidades y principales preocupaciones de la comunidad, tener acceso a la enorme cantidad de información que entregan las Redes Sociales se hace indispensable. 
 
Con esta información las organizaciones tendrán la capacidad de generar cambios sociales significativos y medibles, ya que estarán diseñados en base a estudios de las necesidades específicas de cada comunidad ya sea en el ámbito medioambiental, laboral, educativo, de salud, entre otros. 
 
Por lo tanto, potenciar la comunicación entre las empresas y las comunidades depende directamente del conocimiento que se tiene de éstas. Esta información extraída de las RRSS podrá traducirse entonces en una influencia positiva de las compañías en la colectividad.
"""
METODOLOGIA_MD = """| Etapa                   | Descripción                                                                                                                                                                                                                                                            |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Diseño de investigación | Estudio cualitativo y cuantitativo sobre la base del recogimiento de información de las opiniones de usuarios registradas en redes sociales (Facebook) con cobertura a nivel nacional.                                                                                 |
| Población en estudio    | Población general, mujeres y hombres con cuentas en redes sociales, pertenecientes a todos los grupos etarios y socioeconómicos. Considera una cobertura de prácticamente todo el territorio nacional (salvo algunas comunas pequeñas que no cuentan con información). |
| Instrumento de medición | Software de inteligencia artificial con capacidad de leer el total de los comentarios.                                                                                                                                                                                 |
| Fecha de medición       | El estudio considera los comentarios emitidos a partir del 1 de Enero de 2021 hasta el 31 de Mayo de 2021   """
ANTECEDENTES_MD = """| Antecedente                                                | Descripción                                                                                                                                                                                                                                                                                                                                                       |
|------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Redes Sociales Utilizadas                                  | Cuenta de Facebook Oficial Comunas de Chile                                                                                                                                                                                                                                                                                                                       |
| Cuentas Monitoreadas                                       | 332 cuentas en 16 Regiones                                                                                                                                                                                                                                                                                                                                        |
| Periodo de Análisis                                        | 1 de Enero a 31 de Mayo de 2021                                                                                                                                                                                                                                                                                                                                   |
| Tamaño de la Muestra Total                                 | 1.966.339 Personas                                                                                                                                                                                                                                                                                                                                                |
| Tamaño de Muestra Relacionado a Temas Relevantes Comunales | 858.545 Personas                                                                                                                                                                                                                                                                                                                                                  |
| Metodología                                                | El software leyó comentarios emitidos por el total de la muestra y levantó 1.833 temas de forma automatizada. Entre esos temas el 43 son relevantes, de interés y potencialmente accionables. El software es capaz de interpretar las necesidades de las personas respecto de temas específicos en los que se pueda generar una acción para ayudar a la comunidad |"""

# Opciones Visuales
FONT_SIZE = 14

# Colores
# category_colors = ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#8c564b","#e377c2"]
category_colors = ["#1a249e","#4a8dff","#e66c37","#e044a6","#e044a6","#6b077a"]

st.set_page_config(layout="wide")

# Logo
def get_logo():
    file = open("brand.svg")
    line = file.read().replace("\n", "")
    file.close()
    return line

@st.cache
def load_data():
    data = pd.read_csv('https://update.wholemeaning.com/model/cchc.csv', sep=',')
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

def generar_grafico(data,campoX,campoY,color,altura,formato):
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X(campoY,axis=alt.Axis(title=None,ticks=False,domain=False,gridDash=[2,5],labelPadding=5)),
        y=alt.Y(campoX,sort={"op": "sum", "field": campoY,"order":"descending"},axis=alt.Axis(title=None,ticks=False,labelPadding=10,domain=False)),
        color=alt.Color(color, scale=alt.Scale(domain=temas,range=category_colors),legend=None)
    )
    text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=3,  # Nudges text to right so it doesn't appear on top of the bar
        fontSize=FONT_SIZE,
        color='white'
    ).encode(
        text=alt.Text(campoY,format=formato)
    )
    chart = (chart + text).properties(height=altura).configure_axis(
        labelFontSize=FONT_SIZE,
        labelLimit=400
    ).configure_view(
        strokeWidth=0
    )
    return chart

# Header y ayuda
st.image(get_logo())
st.title('Análsis de Contingencia de la Camara Chilena de la Construcción')
help_container = st.beta_container()
start_button_container = st.empty()
help_container_2 = st.beta_container()
start_button = start_button_container.checkbox("Empezar Análisis")
if not start_button:
    help_container.write(HELP_TEXT_1)
    help_col_1,help_col_2 = help_container_2.beta_columns(2)
    help_col_1.subheader("Guía Rapida")
    help_col_1.write(HELP_TEXT_2)
    help_col_2.subheader("Antecedentes del Estudio")
    help_col_2.write(HELP_TEXT_INTRO)
    help_container_2.header("Marco Teórico")
    help_container_2.subheader("Metodología Empleada")
    help_container_2.markdown(METODOLOGIA_MD)
    help_container_2.subheader("Antecedentes Importantes")
    help_container_2.markdown(ANTECEDENTES_MD)
    st.stop()

# Columnas de filtros y grafico inicial
col1, col2 = st.beta_columns(2)

col1.subheader("Filtros de Región / Comuna")
col1.write("Al seleccionar de estos filtros aparecerá información detallada de la zona")
data = load_data()
regiones = data[REGION_COLUMN].unique().tolist()
regiones.sort()
region = col1.multiselect(label="Filtrar por Región",options=regiones)

comunas = data[COMUNA_COLUMN].unique().tolist()
if region:
    comunas = data[data[REGION_COLUMN].isin(region)][COMUNA_COLUMN].unique().tolist()
comunas.sort()
comuna = col1.multiselect(label="Filtrar por Comuna",options=comunas)

data_filtrada = data
data_filtrada = data_filtrada[data_filtrada[SENDER_COLUMN]==False]
data_filtrada = data_filtrada[data_filtrada[CAT2_COLUMN].notnull()]
data_filtrada = data_filtrada[data_filtrada[CAT2_COLUMN] != 'Otros']

if region:
    data_filtrada = data_filtrada[data_filtrada[REGION_COLUMN].isin(region)]
if comuna:
    data_filtrada = data_filtrada[data_filtrada[COMUNA_COLUMN].isin(comuna)]


data_temas = data_filtrada.groupby(CAT2_COLUMN)[MSG_ID_COLUMN].nunique().to_frame().reset_index(level='cat2')

temas = data[data[CAT2_COLUMN].notnull()][CAT2_COLUMN].unique().tolist()
temas.sort()

temas_chart = generar_grafico(data_temas,'cat2','msg_id','cat2',250,'.0f')
with col2:
    st.subheader("Cantidad de Mensajes por Tema")
    st.altair_chart(temas_chart,True)


if (not region) & (not comuna):
    st.stop()

st.subheader("Información detallada de subtemas para Region(es) y/o Comuna(s) escogida(s)")
tema = st.multiselect(label="Filtrar por Tema",options=temas)

data_subtemas = data_filtrada
if tema:
    data_subtemas = data_subtemas[data_subtemas[CAT2_COLUMN].isin(tema)]
data_q_subtemas = data_subtemas.groupby([CAT2_COLUMN,CAT3_COLUMN])[MSG_ID_COLUMN].nunique().to_frame().reset_index(level=['cat3','cat2'])
data_p_subtemas = data_subtemas.groupby([CAT2_COLUMN,CAT3_COLUMN])[PERCENTAGE_COLUMN].sum().to_frame().reset_index(level=['cat3','cat2'])
data_p_subtemas[PERCENTAGE_COLUMN] = data_p_subtemas[PERCENTAGE_COLUMN]/(data_p_subtemas[PERCENTAGE_COLUMN].sum())


q_subtemas_chart = generar_grafico(data_q_subtemas,'cat3','msg_id','cat2',0,'.0f')
p_subtemas_chart = generar_grafico(data_p_subtemas,'cat3','percentage','cat2',0,'.2%')


# Charts
col3, col4 = st.beta_columns(2)
with col3:
    st.subheader("Indice de Relevancia por Subtema (% Relativo a la Media Nacional)")
    st.altair_chart(p_subtemas_chart,True)
with col4:
    st.subheader("Cantidad de Mensajes por Subtema")
    st.altair_chart(q_subtemas_chart,True)