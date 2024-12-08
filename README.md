# Proyecto Clustering y Modelos de Regresión

En este proyecto asumimos el rol de cientifico de datos en una empresa de comercio global. La compañía busca comprender mejor su base de clientes, productos y operaciones para tomar decisiones informadas que maximicen el beneficio y optimicen sus procesos.

Disponemos un conjunto de datos del comercio global que incluye información sobre ventas, envíos, costos y beneficios a nivel de cliente y producto. Nuestro objetivo es segmentar los datos mediante clustering y luego diseñar modelos de regresión específicos para cada segmento, lo que permitirá obtener insights personalizados sobre los factores que influyen en el éxito de la compañía.

## Objetivos
En base a la premisa establecida el ojetivo del proyecto es realizar:

**Clustering**: Realizar un análisis de segmentación para agrupar clientes o productos según características clave, las cuales deberás elegir personalmente además de justificar el porque de su elección.

**Regresión por Segmentos**: Diseñar modelos de predicción para cada segmento, explicando las relaciones entre variables, intentando predecir el profit generado para la empresa.

## Estructura del Proyecto

Este proyecto se divide en tres carpetas principales dentro de los cuales podemos encontrar archivos de distinto carácter, a continación se muentra un esquema de la organización del respositorio:


```bash
Proyecto9-ClusteringRegresion/
├── datos/                       # Archivos de datos CSV y PKL para el proyecto.
│   ├── cluster_0/               # Dataframes generados durante el preprosecamiento de los datos de dicho cluster
|   |   ├── preprocesamiento/    # Almacenamiento de los modelos de encoding y scaler del cluster
|   ├── cluster_1/
|   |   ├── preprocesamiento/
|   ├── cluster_2/
|   |   ├── preprocesamiento/
│   ├── dataframes/              # Dataframes generados durante la fase de clustering
│
├── notebooks/                   
│   ├── clustering/              # Notebooks de Jupyter con los posibles clusters
│   │   ├── clustering_v1.ipynb
│   │   ├── clustering_v2.ipynb
│   │   ├── intrucciones.txt    # Instrucciones comparativas entre los modelos de clustering 
│   ├── regresion_logistica/    # Carpeta con el preprocesamiento de los datos y modelos de cada cluster
│   │   ├── Cluster_0/
│   │   ├── Cluster_1/
│   │   ├── Cluster_2/
│ 
├── src/                         # Archivos .py para funciones auxiliares del proyecto.
|
└── README.md                    # Descripción del proyecto, instrucciones de instalación y uso.                
```


## Resumen del proyecto

El proyecto se ha desarrollado en dos fases principales:

1. **Clustering**

    La primera parte del proyecto consistía en divdir los datos en distintos cluster para posteriormente hacer predicciones. Para desarrollar esta parte se llevaron a cabo dos aproximaciones que se encuentras en los notebooks de la carpeta `cluetring` donde la principal diferencia entre ellos son las colunas escogidas para hacer estas divisiones. En ambos notebooks se usaron los modelos k-means y dbsacn. Finalmente, la división de clusterings elegida se encuentra en` notebooks/clustering/clustering_v12.ipynb` con el modelo k-means, obteniendo unas métricas de 0.93 en el silhouette_score y 0.13 en el davies_bouldin_index.

    La división de los custers se hace en función de Category donde el cluster 1 abarca technology y furniture y los clusters 0 y 1 se dividen office supplies.
    Además, en cuanto a mercados el cluster dos solo abarca Africa, EMEA y un poco de Canadá.
    Viendo el Profit de cada cluster el clustar 0 va de -3700 a 5000, cluster 1 de -6500 a 8400 y cluster 2 de -2000 a 1400.
    Por lo que de nuevo, en cuanto a profit el cluster 1 tiene un rango muy amplio, sin embargo, tiene sentido pues abarca dos de las tres categorías de producto.

2. **Regresión logística**

    Un vez tenemos los tres clusters dividimos el data frame y para cada cluster llevamos a cabo un preprocesamiento diferente en función del EDA de cada uno. Probamos diferentes modelos de regresión, como son el Random Forest, Gradient Boosting o XGBoost y nos quedamos con aquel cuyas métricas de R2 y RMSE sean mejores, pero siempre intentando evitar el oerfitting. Estas métricas de pueden encontrar dentro de `notebooks/regresion_logistica/Cluster_X/5-modelos.ipynb`.


## Instalación y Requisitos
Este proyecto usa Python 3.11 y requiere las siguientes bibliotecas:
- [numpy](https://numpy.org/doc/stable/)
- [pandas](https://pandas.pydata.org/docs/reference/frame.html)
- [matplotlib.pyplot](https://matplotlib.org/3.5.3/api/_as_gen/matplotlib.pyplot.html)
- [seaborn](https://seaborn.pydata.org/)
- [shap](https://shap.readthedocs.io/en/latest/)
- [flask](https://flask.palletsprojects.com/en/stable/)
- [scikitlearn](https://scikit-learn.org/stable/)
- [imblearn](https://imbalanced-learn.org/stable/)
- [itertools](https://docs.python.org/3/library/itertools.html)
- [warnings](https://docs.python.org/3/library/warnings.html)

Este proyecto es funcional a fecha 8 de diciembre de 2024.



Para visualizar el proyecto en tu máquina local, sigue estos pasos:

1. **Clona el repositorio**:
   ```bash
   git clone [URL del repositorio]

   Instala las dependencias en tu entorno de Python.
   
2. **Navega a la carpeta del proyecto**:
   ```bash
   cd Proyecto8-PrediccionRetencionEmpleados

2. **Ejecutar o visualizar los archivos**:

   Para ver todo el ciclo de creación de principio a fin se debe comenzar por a carpeta de clustering y posteriorente con la carpeta de regresion_lositica, dentro de esta accederemos al Cluster_X deseado y podremos visualizar o ejecutar los archivos en el orden deseado.

