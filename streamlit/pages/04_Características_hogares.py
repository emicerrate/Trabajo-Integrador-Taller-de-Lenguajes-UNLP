import streamlit as st
import matplotlib.pyplot as plt
from package.data_graphics.individuos import agglomeration_id
from package.data_graphics.hogares import (
    load_hogar_data_04,
    get_available_years,
    get_total_houses,
    get_housing_type_distribution,
    get_floor_material_by_agglomerate,
    get_bathroom_access_by_agglomerate,
    get_villas_by_agglomerate,
    get_habitability_by_agglomerate,
    get_tenure_evolution_named
)

st.title("🏠 Características Hogares")

st.markdown("""
En esta sección podés explorar distintos **aspectos habitacionales** de la población argentina a partir de los datos de la **Encuesta Permanente de Hogares (EPH)**. 
A partir del **año seleccionado** (o incluyendo **todos los disponibles**), se dan a conocer:

- cuántas **viviendas** fueron relevadas  
- cómo se distribuyen según su **tipo**  
- qué **materiales predominan** en los pisos  
- si disponen de **baño interior**  
- el **régimen de tenencia** a lo largo del tiempo  
- y la proporción de viviendas ubicadas en **villas de emergencia**
""")
# Cargar los datos de hogares con las columnas necesarias
try:
    df = load_hogar_data_04()
except (FileNotFoundError, ValueError) as e:
    st.error(str(e))
    st.stop()

# Filtro por año, hago un selectbox para elegir el año o todos
available_years = get_available_years(df)

st.subheader("Seleccionar año:")
selected_year = st.selectbox("", ["Todos"] + available_years, index=len(available_years))

# 1.4.1 Cantidad total de viviendas
st.subheader("Cantidad total de viviendas")

st.markdown("""
Muestra de la cantidad total de viviendas incluidas en la encuesta para el año seleccionado.
""")

# Si el año seleccionado no es "Todos", filtro el dataframe por el año seleccionado
if selected_year != "Todos":
    df = df[df["ANO4"] == selected_year]

st.info(f"Total de viviendas de {selected_year:02}: {get_total_houses(df):02}")

# 1.4.2 Distribución por tipo de vivienda
st.subheader("Distribución por tipo de vivienda")

st.markdown("""
Muestra de la proporción de viviendas según su tipo para el año seleccionado.
""")

type_counts = get_housing_type_distribution(df)

# Diccionario para tipo de casa y reemplazar en grafico
type_housing = {
    1: "Casa",
    2: "Departamento",
    3: "Pieza en inquilinato",
    4: "Pieza en hotel/pensión",
    5: "Local no construido para habitación",
    6: "Otros"
}

type_counts.rename(index=type_housing, inplace=True)

# Preparar explosión para los segmento menores porcentajes
explode = [0.15 if label == "Casa" else 0 for label in type_counts.index]

# Colores personalizados
colors = [
    "#D32F2F",  
    "#FF8A65",  
    "#FFD54F",  
    "#FFB300",  
    "#FFA000",  
    "#FFF176"    
]

# Crear figura y fondo oscuro
fig, ax = plt.subplots(figsize=(7, 5.5), facecolor='#1D2B44')
ax.set_facecolor('#1D2B44')

# Gráfico
wedges, texts, autotexts = ax.pie(
    type_counts,
    autopct="%1.1f%%",
    explode=explode,
    startangle=90,
    colors=colors,
    textprops=dict(color="white", fontsize=9),
    pctdistance=0.8
)

# Ocultar porcentajes para los sectores chicos (posiciones 2 al final)
for i in range(2, len(autotexts)):
    autotexts[i].set_text("")

# Título
ax.set_title("Proporción por tipo de vivienda", fontsize=16, color="white", pad=5)

# Calcular porcentajes
total = type_counts.sum()
percentages = (type_counts / total * 100).round(1)

# Etiquetas en la leyenda con porcentaje
labels_with_pct = [f"{label} ({percentages[label]}%)" for label in type_counts.index]

# Leyenda externa para evitar superposición
leg = ax.legend(
    wedges,
    labels_with_pct,
    title="Tipo de vivienda",
    title_fontsize=10,
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
    fontsize=9,
    labelcolor="white",
    facecolor="#1D2B44",
    edgecolor="#1D2B44",
)
# Cambiar color del título a blanco
leg.get_title().set_color("white")
# Ajustar margen de arriba
plt.subplots_adjust(top=0.8)
# Mostrar en Streamlit
st.pyplot(fig)

# 1.4.3 Material predominante en pisos por aglomerado
st.subheader("Material predominante en pisos por aglomerado")
st.markdown("""
Muestra de los materiales en pisos interiores de las viviendas por aglomerado para el año seleccionado.
""")
st.dataframe(get_floor_material_by_agglomerate(df), hide_index=True)

# 1.4.4 Porcentaje de viviendas con baño dentro del hogar por aglomerado
st.subheader("Porcentaje de viviendas con baño dentro del hogar por aglomerado")
st.markdown("""
Muestra de los porcentajes de las viviendas con baño de las viviendas para el año seleccionado.
""")
st.dataframe(get_bathroom_access_by_agglomerate(df), hide_index=True)

# 1.4.5 Evolución del régimen de tenencia
st.subheader("Evolución del régimen de tenencia")
st.markdown("""
Muestra de la evolución del régimen de tenencia (propia, alquilada, cedida, etc.) para el aglomerado elegido en el año seleccionado.
""")

# Diccionario y listas de aglomerados
dict_ag_id = agglomeration_id()
dict_name_to_id = {v: int(k) for k, v in dict_ag_id.items()}
agglomerates = sorted(dict_name_to_id.keys())

# Selector de aglomerado
selected_agglomerate_name = st.selectbox("Aglomerado", agglomerates, key="ten_agglom")
selected_agglomerate = dict_name_to_id[selected_agglomerate_name]

# Diccionario de regimen de tenencia
TENENCIA_LABELS = {
    1: "Propietario vivienda y terreno",
    2: "Propietario vivienda solo",
    3: "Inquilino / arrendatario",
    4: "Ocupante por impuestos/expensas",
    5: "Ocupante en relación laboral",
    6: "Ocupante con permiso",
    7: "Ocupante sin permiso",
    8: "Está en sucesión"
}

# Selector de tenencias por nombre
selected_labels = st.multiselect(
    "Tipo(s) de tenencia",
    options=list(TENENCIA_LABELS.values()),
    default=list(TENENCIA_LABELS.values())
)

pivot = get_tenure_evolution_named(df, selected_agglomerate, selected_labels)

if pivot.empty:
    st.warning("No hay datos disponibles para la selección.")
else:
    pivot["Periodo"] = pivot["ANO4"].astype(str) + "-T" + pivot["TRIMESTRE"].astype(str)

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#1D2B44')
    ax.set_facecolor('#1D2B44')

    for label in selected_labels:
        if label in pivot.columns:
            ax.plot(pivot["Periodo"], pivot[label], label=label, linewidth=2)

    ax.set_title("Evolución del régimen de tenencia", fontsize=14, color='white')
    ax.set_xlabel("Periodo", fontsize=12, color='white')
    ax.set_ylabel("Viviendas", fontsize=12, color='white')
    ax.tick_params(axis='x', labelrotation=45, colors='white')
    ax.tick_params(axis='y', colors='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    ax.legend(labelcolor='white', facecolor='#1D2B44', frameon=False)
    st.pyplot(fig)

# 1.4.6 - Viviendas en villa de emergencia
st.subheader("Viviendas en villa de emergencia")
st.markdown("""
Muestra de manera decreciente la cantidad de viviendas ubicadas en villa de emergencia por aglomerado. 
También se informa el total y el porcentaje de viviendas en villa de emergencia con respecto al total.
""")

villa_df = get_villas_by_agglomerate(df)
villa_df = villa_df.sort_values(by="Cantidad en Villas", ascending=False)
st.dataframe(villa_df[["Aglomerado", "Cantidad en Villas", "Total", "Porcentaje"]], hide_index=True)

# 1.4.7 - Condición de habitabilidad por aglomerado
st.subheader("Condición de habitabilidad por aglomerado")
st.markdown("""
Muestra el porcentaje de viviendas por su condición de habitabilidad. Se puede descargar el CSV.
""")
hab_df = get_habitability_by_agglomerate(df)
st.dataframe(hab_df[["Aglomerado", "CONDICION_DE_HABITABILIDAD", "Cantidad", "Porcentaje"]])

csv = hab_df.to_csv(index=False).encode("utf-8")
st.download_button("Descargar CSV", data=csv, file_name="habitabilidad.csv", mime="text/csv")