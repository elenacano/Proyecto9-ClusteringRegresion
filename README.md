# Proyecto Clustering y Modelos de Regresión

![Descripción de la imagen](imagenes/portada.jpg)

En este proyecto asumimos el rol de cientifico de datos en una empresa de comercio global. La compañía busca comprender mejor su base de clientes, productos y operaciones para tomar decisiones informadas que maximicen el beneficio y optimicen sus procesos.

Disponemos un conjunto de datos del comercio global que incluye información sobre ventas, envíos, costos y beneficios a nivel de cliente y producto. Nuestro objetivo es segmentar los datos mediante clustering y luego diseñar modelos de regresión específicos para cada segmento, lo que permitirá obtener insights personalizados sobre los factores que influyen en el éxito de la compañía.

## Objetivos
En base a la premisa establecida el ojetivo del proyecto es realizar:

**Clustering**: Realizar un análisis de segmentación para agrupar clientes o productos según características clave, las cuales deberás elegir personalmente además de justificar el porque de su elección.

**Regresión por Segmentos**: Diseñar modelos de predicción para cada segmento, explicando las relaciones entre variables, intentando predecir el total de ventas en cada uno de los segmentos.

## Estructura del Proyecto


```bash
Proyecto9-ClusteringRegresion/
├── datos/                      # Archivos de datos CSV y PKL para el proyecto.
│   ├── cluster_0/              # Dataframes generados durante el preprosecamiento de los datos de dicho cluster
|   |   ├── preprocesamiento/   # Almacenamiento de los modelos de encoding y scaler del cluster
|   ├── cluster_1/
|   |   ├── preprocesamiento/
|   ├── cluster_2/
|   |   ├── preprocesamiento/
│   ├── dataframes/             # Dataframes generados durante la fase de clustering
│
├── notebooks/                  # Notebooks de Jupyter con los modelos probados.
│   ├── clustering/               # Carpeta del modelo
│   │   ├── 00_Sobre_El_Modelo.md
│   │   ├── 01_eda_inicial.ipynb
│   │   ├── 02_gestion_datos.ipynb
│   │   ├── 03_eda_gestionado.ipynb
│   │   ├── 04_encoding.ipynb
│   │   ├── 05_feature_scaling.ipynb
│   │   ├── 06_outliers.ipynb
│   │   ├── 07_desbalanceo.ipynb
│   │   ├── 08_modelos.ipynb
│   │   ├── 09_obtener_mejor_modelo.ipynb
│   ├── regresion_logistica/               # Carpeta del modelo
│   │   ├── 00_Sobre_El_Modelo.md
│ 
├── src/                        # Archivos .py para funciones auxiliares del proyecto.
│
├── streamlit/                  # Web para realizar predicciones de forma rápida y bonita
│    ├── main.py                # Configuración Web
│    ├── prueba_modelo.ipynb 
│
└── README.md                   # Descripción del proyecto, instrucciones de instalación y uso.                
```

1. **datos**

    Donde encontramos los `.csv` originales de los datos y otras dos carpetas:
    - `dataframes`:  donde se almacenan los diferentes dataframes generados en cada fase del modelo.
    - `preprocesamiento`: donde almacenamos el encoder o scaler utilizados en dicho modelo.

2. **src**

    Podemos encontrar todos los archivos .py con las fuciones de soporte para cada parte del modelo.

3. **notebooks**

    Donde se encuentran las distintas fases de la creación del modelo.
    - `1-EDA-nulos.ipynb`
    - `2-encoding.ipynb`
    - `3-outliers.ipynb`
    - `4-estandarizacion.ipynb`
    - `5-balanceo.ipynb`, aunque hay algunos modelos que no cuentan con este notebook.
    - `6-modelos.ipynb`, en este notebook se pueden encontrar las métricas obtenidas para dicho modelo.

4. **Modelo_.txt**

    Cada modelo tiene un .txt explicando más en profundidad como se han tratado los datos y las diferencias que hay respecto al modelo en el que están basados.


## Resumen del proyecto

Tras probar varios modelos podemos concluir que las mejores métricas obtenidas son las del `Modelo4`. Para este modelo el preprocesamiento de los datos fue el siguiente:

- **EDA**
    - Tras eliminar el EmploeeID eliminamos los duplicados.
    - Gestión de nulos: Hemos eliminado los nulos de las numéricas que representaban un 1.78% y los nulos de las categoricas las hemos imputado por "sin informacion".

- **Encoding**:
    - Devuelvo a numéricas: ['Education', 'JobLevel', 'StockOptionLevel', 'PerformanceRating', "TrainingTimesLastYear", "JobInvolvement"]
    -  "onehot":["Gender", 'JobRole']
        "target":['EnvironmentSatisfaction', 'JobSatisfaction', 'WorkLifeBalance', 'BusinessTravel', 'Department', 'EducationField',  'MaritalStatus']

- **Outliers**:
    - Detección con IFO.
    - Eliminamos los que cumplen que son outliers en al menos el 70% de los casos, estos representan un 1.62%.

- **Estandarizacion**:
    - Estandarizado con robust scaler.

- **Balanceo**
    - Obtenemos un balanceo del 62-37 aplicando primero Tomek link y después el smotenc.

Una vez llevado a cabo todo este preprocesamiento se probaron varios modelos de clasificación como la regresión logística, el descision tree, el random forst, el gradient boosting y el xgboost. Finalmente las métricas obtenidas fueron las siguientes:

![Descripción de la imagen](imagenes/metricas-modelo4.png)

Como podemos observar el modelo que mejor funciona es el gradient boosting con un **accuracy, precisión y recall de 0.9** y una **kappa de 0.8**. Además, la métrica que más queremos priorizar es recall pues nos interesa minimizar los falsos negativos, es decir, queremos el menor número de predicciones que digan que un empleado no se va de la empresa y finalmente se va. Si observamos las matrices de confusión para las distintas métricas el gradiente boosting es la que arroja un menor número de falsos negativos.

![Descripción de la imagen](imagenes/matrices_modelo4.png)

En los distintos modelos se han probado diferentes formas de gestionar los outliers, el encoding, la estandarización o el balanceo, sin embargo, es en este modelo donde mejores métricas se han obtenido.

Una vez hemos concluido que el gradient boosting del Modelo4 es el mejor, almacenamos el modelo y lo entrenamos con todos los datos dentro del notebook `6-modelos.ipynb` en el Módulo4. Además, encontraremos un notebook adicional que es el `7-prediccion.ipynb` donde nos inventamos unos datos ficticios y comprobamos que se hagan las predicciones correctamente.

Finalmente, para hacer una interfaz más amigable a la hora de hacer las predicciones se ha creado una API con Flask dentro de `src/main.py` la cual renderiza un html a través del cual le podemos meter las distintas métricas para un empleado y predecir con qué probabilidad abandona o no la empresa.

## Conclusiones 

Tras obtener nuestro mejor modelo lo que más nos interesa saber es: ¿cuáles son los factores que más influyen a la hora de hacer la predicción? ¿Qué valores se toman para cada categoría en las personas que deciden abandonar una empresa?

La primera pregunta la podemos responder viendo la gráfica de la impotancia de los predictores:

![Descripción de la imagen](imagenes/feture-importance.png)

Como podemos observar los predictores que mayor peso tienen a la hora de genera el modelo son: YearsAtCompany, YearsWithCurrentManager, Age, NumCompaniesWorked y MaritalStatus. Las primeras no nos sorprenden que parezcan juntas pues como se ve en el EDA las dos primeras están bastante correlacionadas, sin embargo, Maritalstatus si que me llama la atención. Por otro lado lo que menos parece influir es el JobInvolment, el género y el JobRole.

Contestemos a la segunda pregunta, para ello usaremos el gráfico shap:

![Descripción de la imagen](imagenes/shap.png)

Vemos como los valores de cada variable influye y en que nivel para que una persona abandone la compañía. Para entender los valores de MaritalStatus tenemos que volver al notebook 2 y ver a qué valores corresponde cada categría, vemos que Single es la más alta y casado y divorciado tienen valores muy similares. Por lo tanto las personas solteras son más propensas a irse de la compañía.
También podemos ver que aquellos que llevan menos años en la compañía, con su manager y en general menos años trabajando también son más propensos a irse, lo que coincide con las personas más jovenes. También podemos destacar que aquellas que tienen mayor nivel de estudios o las que tienden a viajar más suelen tener un porcentaje más alto para irse de la empresa. 

Por lo tanto, hemos visto cuales son las que más afectan y también dentro de cada categoría para qué valores suele haber más porcentaje de abandono. También hemos podido observar que métricas que en un primer momento no podían parecer decisorias como EnvironmentSatisfaction o Jobsatisfaction resulta que aquellos trabajadores que les dan valores más altos tiene mayor probabilidades de irse. Por lo que estos gráficos aportan una información de gran valor a la empresa a la hora de identificar en qué clase de perfiles incidir más para cambiar esas tendencias de abandono.


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

Este proyecto es funcional a fecha 1 de diciembre de 2024.



Para visualizar el proyecto en tu máquina local, sigue estos pasos:

1. **Clona el repositorio**:
   ```bash
   git clone [URL del repositorio]

   Instala las dependencias en tu entorno de Python.
   
2. **Navega a la carpeta del proyecto**:
   ```bash
   cd Proyecto8-PrediccionRetencionEmpleados

2. **Ejecutar o visualizar los archivos**:
   Accede a cualquier carpeta de los modelos y dentro ve a la carpeta `notebooks` y ejecuta o visualiza los archivos en el orden especificado.

   Para realizar predicciones accede a `Modulo4/src` y ejecuta:
   ```bash
   python main.py
   ```
   Abre el navegador e introduce la siguiente URL http://127.0.0.1:5000, introduce los datos deseados y pulsa "Enviar", a continuación aparecerá la predicción para los datos proporcionados.

   ![Descripción de la imagen](imagenes/api.png)

