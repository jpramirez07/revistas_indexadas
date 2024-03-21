import pandas as pd ### para manejo de datos
import matplotlib.pyplot as plt

revistas2022 = 'https://raw.githubusercontent.com/jpramirez07/revistas_indexadas/main/revistas2022.csv'
df_revistas2022=pd.read_csv(revistas2022, encoding='latin1')
df_revistas2022['año'] = 2022

revistas2021 = 'https://raw.githubusercontent.com/jpramirez07/revistas_indexadas/main/revistas2021.csv'
df_revistas2021=pd.read_csv(revistas2021, encoding='latin1')
df_revistas2021['año'] = 2021

revistas2020 = 'https://raw.githubusercontent.com/jpramirez07/revistas_indexadas/main/revistas2020.csv'
df_revistas2020=pd.read_csv(revistas2020, encoding='latin1')
df_revistas2020['año'] = 2020

revistas2019 = 'https://raw.githubusercontent.com/jpramirez07/revistas_indexadas/main/revistas2019.csv'
df_revistas2019=pd.read_csv(revistas2019, encoding='latin1')
df_revistas2019['año'] = 2019

revistas2018 = 'https://raw.githubusercontent.com/jpramirez07/revistas_indexadas/main/revistas2018.csv'
df_revistas2018=pd.read_csv(revistas2018, encoding='latin1')
df_revistas2018['año'] = 2018

df_revistas2022.info()

#### revistas2018, revistas2019, revistas2020, revistas2021, revistas2022

# Concatenar todos los dataframes en uno solo
base_datos = pd.concat([df_revistas2018, df_revistas2019, df_revistas2020, df_revistas2021, df_revistas2022], ignore_index=True)

base_datos.info()
base_datos['Type']

#### En este caso solo nos interesa los tipos revista(journal), por lo que el resto de registros se borara

condicion = base_datos['Type'] == 'journal'
revistas = base_datos.loc[condicion]
revistas['Type'].unique()

#### En este caso y para simplificar la BD no necesitamos para nuestro ejercicio y analisis las variables Areas, Issn, Type

Eliminar = ['Issn', 'Type']
revistas = revistas.drop(Eliminar, axis=1)

#### Para el caso de clasificacion de colciencias se hace una transformacion de la variable SJR Best Quartile, y es que para colciencias los Quartiles los clasifica como Q1=A1, Q2=A2, Q3=B y Q4=C

revistas['SJR Best Quartile'] = revistas['SJR Best Quartile'].replace({
    'Q1': 'A1',
    'Q2': 'A2',
    'Q3': 'B',
    'Q4': 'C'
})

### Se encontro que en la variable SJR Best Quartile hay valores rellenos con -, por lo que se presume que no fueron categorizadas y se procede a borrar estos registros

revistas = revistas.drop(revistas[revistas['SJR Best Quartile'] == '-'].index)

### Ahora veremos cuales son las revistas que han cambiado hasta 3 veces de nivel

categorias_unicas_por_grupo = revistas.groupby(['Sourceid'])['SJR Best Quartile'].nunique()
grupos_con_mas_de_3_categorias = categorias_unicas_por_grupo[categorias_unicas_por_grupo == 3]
grupos_con_mas_de_3_categorias.head(100)
revistas[revistas['Sourceid'] == 15629]


### Mejores revistas de latinoamerica teniendo en cuenta el rank de la ultima edicion de la revista homologada

### Vemos que paises de latinoamerica tiene nuestro DataFrame

revistas['Country'].unique()

### Extraemos estos paises de latino america en un array 

latinoamerica = ['Brazil', 'Mexico', 'Colombia', 'Chile', 'Costa Rica', 'Argentina', 'Peru', 'Cuba', 'Venezuela', 'Trinidad and Tobago', 'Ecuador', 'Uruguay', 'Bolivia']

### Apartir de esta lista creamos nuestra condicion y mostramos las 10 mejores revistas de latino america

revistas_latinoamerica = revistas[revistas['Country'].isin(latinoamerica)]
revistas_latinoamerica = revistas_latinoamerica.groupby('Sourceid').last()

### Las mejores 10 revistas de latinoamerica segun el rank de la ultima revista homologada en COlCIENCIAS:

mejores10 = revistas_latinoamerica.sort_values(by='Rank').head(10)

mejores10['Title']

### Vamos a comparar la cantidad de revistas publicadas por las regines de latino america, europa, asia y estados unidos

paises_europa = [
    'Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria',
    'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany',
    'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kosovo', 'Latvia', 'Liechtenstein',
    'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands',
    'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino',
    'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom',
    'Vatican City'
]

paises_asia = [
    'Afghanistan', 'Armenia', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Bhutan', 'Brunei', 'Cambodia',
    'China', 'Cyprus', 'Georgia', 'India', 'Indonesia', 'Iran', 'Iraq', 'Israel', 'Japan', 'Jordan',
    'Kazakhstan', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Lebanon', 'Malaysia', 'Maldives', 'Mongolia', 'Myanmar',
    'Nepal', 'North Korea', 'Oman', 'Pakistan', 'Palestine', 'Philippines', 'Qatar', 'Saudi Arabia',
    'Singapore', 'South Korea', 'Sri Lanka', 'Syria', 'Tajikistan', 'Thailand', 'Timor-Leste', 'Turkey',
    'Turkmenistan', 'United Arab Emirates', 'Uzbekistan', 'Vietnam', 'Yemen'
]

United_States = 'United States'

### Apartir de estas listas creamos nuestras condiciones para saber cuantas revistas tiene cada zona 

revistas_europa = revistas[revistas['Country'].isin(paises_europa)]
revistas_europa = revistas_europa.groupby('Sourceid').last()
revistas_europa.__len__()

revistas_asia = revistas[revistas['Country'].isin(paises_asia)]
revistas_asia = revistas_asia.groupby('Sourceid').last()
revistas_asia.__len__()

revistas_EEUU = revistas[revistas['Country'] == United_States]
revistas_EEUU = revistas_EEUU.groupby('Sourceid').last()
revistas_EEUU.__len__()

revistas_latinoamerica.__len__()

cantidad_revistas = {
    'latinoamerica' : revistas_latinoamerica.__len__(),
    'europa' : revistas_europa.__len__(),
    'asia' : revistas_asia.__len__(),
    'estados_unidos' : revistas_EEUU.__len__()
}

# Convertir el diccionario en un DataFrame
df_revistas = pd.DataFrame.from_dict(cantidad_revistas, orient='index', columns=['cant_revistas'])

# Crear el gráfico de torta
df_revistas.plot(kind='pie', y='cant_revistas', autopct='%1.1f%%', startangle=90, legend=False)

# Añadir título al gráfico
plt.title('Distribución de revistas por Región')

# Mostrar el gráfico
plt.axis('equal')  # Para asegurar que el gráfico sea un círculo
plt.show()

### Segun lo que podemos observar en el grafico de torta de la distribucion de las revistas por region podemos concluir que latino america es la region con menos catidad de revistas por mucho, un dato alarmante y que nos debe poner a reflexionar de la importancia de la investigacion en la region.