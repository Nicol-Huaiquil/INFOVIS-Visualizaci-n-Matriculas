import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def grafico_Stacked_area_chart(colores, titulo):
    _, ax = plt.subplots(figsize=(12, 6))

    handles = []
    areas = []  # Lista para almacenar las áreas antes de graficar

    for genero in ['mujeres', 'hombres']:
        for institucion, color in colores.items():
            subset = df[(df['Tipo Institucion'] == institucion) & df[f'Matricula primer agno {genero}'].notna()]

            # Calcular la suma por año y tipo de institución
            matriculas_por_anio_tipo = subset.groupby('Agno')[f'Matricula primer agno {genero}'].sum()
            areas.append(matriculas_por_anio_tipo.values)  # Almacenar área antes de graficar

            # Añadir a la leyenda
            handles.append(Patch(facecolor=[c/255 for c in color[genero]], edgecolor='black', label=f'{institucion} - {genero.capitalize()}'))

    # Ordenar las áreas por tamaño (de mayor a menor)
    areas = sorted(areas, key=lambda x: sum(x), reverse=True)

    # Graficar en Stacked Area Chart con colores sólidos en el orden correcto
    for area, handle, color_definido in zip(areas, handles, [color for col in colores.values() for color in col.values()]):
        ax.fill_between(matriculas_por_anio_tipo.index, 0, area, color=[c/255 for c in color_definido], edgecolor='black', alpha=0.7)

    # Configuración adicional del gráfico
    plt.xlabel('Año')
    plt.ylabel('Matrículas')
    plt.title(f'Matricula por Año de {titulo}')
    plt.legend(handles=handles)
    if titulo == 'F.F.A.A.':
        ax.set_ylim(bottom=ax.get_ylim()[0], top=3000)

    plt.show()

# Paso 1: Cargar datos desde el archivo CSV
archivo_csv = 'matriculasgenero.csv'
df = pd.read_csv(archivo_csv, delimiter=';')

# Definir colores
colores = {
    'Univ.': {
        'mujeres': (255, 151, 253),   # Rosa claro
        'hombres': (150, 214, 255)    # Azul claro
    },
    'I.P.': {
        'mujeres': (255, 0, 251),   # Rosa 
        'hombres': (0, 155, 255)    # Azul 
    },
    'C.F.T.': {
        'mujeres': (148, 71, 130),   # Rosa oscuro
        'hombres': (59, 110, 143)    # Azul oscuro
    }
}

colores_2 = {
    'F.F.A.A.': {
        'mujeres': (136, 0, 104),  # Rosa más oscuro
        'hombres': (0, 83, 136)    # Azul más oscuro
    }
}

# Invertir el orden de las tuplas en el diccionario
colores_2 = {k: dict(reversed(v.items())) for k, v in colores_2.items()}

grafico_Stacked_area_chart(colores, 'Univ., I.P. y C.F.T.')
grafico_Stacked_area_chart(colores_2, 'F.F.A.A.')
