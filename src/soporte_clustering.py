# Tratamiento de datos
# -----------------------------------------------------------------------
import numpy as np
import pandas as pd

# Otras utilidades
# -----------------------------------------------------------------------
import math
from tqdm import tqdm

# Para las visualizaciones
# -----------------------------------------------------------------------
import matplotlib.pyplot as plt
import seaborn as sns

# Preprocesado y modelado
# -----------------------------------------------------------------------
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# Sacar número de clusters y métricas
# -----------------------------------------------------------------------
from yellowbrick.cluster import KElbowVisualizer
from sklearn.metrics import silhouette_score, davies_bouldin_score

# Modelos de clustering
# -----------------------------------------------------------------------
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import SpectralClustering

# Para visualizar los dendrogramas
# -----------------------------------------------------------------------
import scipy.cluster.hierarchy as sch

class Exploracion:
    """
    Clase para realizar la exploración y visualización de datos en un DataFrame.

    Atributos:
    dataframe : pd.DataFrame
        El conjunto de datos a ser explorado y visualizado.
    """

    def __init__(self, dataframe):
        """
        Inicializa la clase Exploracion con un DataFrame.

        Params:
            - dataframe : pd.DataFrame. El DataFrame que contiene los datos a ser explorados.
        """
        self.dataframe = dataframe
    
    def explorar_datos(self):
        """
        Realiza un análisis exploratorio de un DataFrame.

        Params:
            - Ninguno.

        Returns:
            - None.
        """
        

        print("5 registros aleatorios:")
        display(self.dataframe.sample(5))
        print("\n")

        print(self.dataframe.shape)

        print("Información general del DataFrame:")
        print(self.dataframe.info())
        print("\n")

        print("Duplicados en el DataFrame:")
        print(self.dataframe.duplicated().sum())
        print("\n")

        print("Estadísticas descriptivas de las columnas numéricas:")
        display(self.dataframe.describe().T)
        print("\n")

        print("Estadísticas descriptivas de las columnas categóricas:")
        categorical_columns = self.dataframe.select_dtypes(include=['object']).columns
        if len(categorical_columns) > 0:
            display(self.dataframe[categorical_columns].describe().T)
        else:
            print("No hay columnas categóricas en el DataFrame.")
        print("\n")
        
        print("Número de valores nulos por columna:")
        print(self.dataframe.isnull().sum())
        print("\n")
        
        if len(categorical_columns) > 0:
            print("Distribución de valores categóricos:")
            for col in categorical_columns:
                print(f"\nColumna: {col}")
                print(self.dataframe[col].value_counts())
        
        df_corr = self.dataframe.corr(numeric_only=True)
        mascara = np.triu(np.ones_like(df_corr, dtype=np.bool))
        plt.figure(figsize=(10,5))
        sns.heatmap(df_corr, annot=True, vmin=-1, vmax=1, mask=mascara, cmap="coolwarm")

    def visualizar_numericas(self):
        """
        Genera histogramas, boxplots y gráficos de dispersión para las variables numéricas del DataFrame.

        Params:
            - Ninguno.

        Returns:
            - None.
        """
        columns = self.dataframe.select_dtypes(include=np.number).columns

        # Histogramas
        fig, axes = plt.subplots(nrows=math.ceil(len(columns)/2), ncols=2, figsize=(21, 13))
        axes = axes.flat
        plt.suptitle("Distribución de las variables numéricas", fontsize=24)
        for indice, columna in enumerate(columns):
            sns.histplot(x=columna, data=self.dataframe, ax=axes[indice], kde=True, color="#F2C349")

        if len(columns) % 2 != 0:
            fig.delaxes(axes[-1])

        plt.tight_layout()

        # Boxplots
        fig, axes = plt.subplots(nrows=math.ceil(len(columns)/2), ncols=2, figsize=(19, 11))
        axes = axes.flat
        plt.suptitle("Boxplots de las variables numéricas", fontsize=24)
        for indice, columna in enumerate(columns):
            sns.boxplot(x=columna, data=self.dataframe, ax=axes[indice], color="#F2C349", flierprops={'markersize': 4, 'markerfacecolor': 'cyan'})
        if len(columns) % 2 != 0:
            fig.delaxes(axes[-1])
        plt.tight_layout()
    
    def visualizar_categoricas(self, figsize=(15, 10)):
        """
        Genera gráficos de barras (count plots) para las variables categóricas del DataFrame.

        Params:
            - Ninguno.

        Returns:
            - None.
        """
        categorical_columns = self.dataframe.select_dtypes(include=['object', 'category']).columns

        if len(categorical_columns) > 0:
            try:
                _, axes = plt.subplots(nrows=len(categorical_columns), ncols=1, figsize=figsize)
                axes = axes.flat
                plt.suptitle("Distribución de las variables categóricas", fontsize=24)
                for indice, columna in enumerate(categorical_columns):
                    sns.countplot(data=self.dataframe, x=columna, ax=axes[indice])
                    axes[indice].set_title(f'Distribución de {columna}', fontsize=20)
                    axes[indice].set_xlabel(columna, fontsize=16)
                    axes[indice].set_ylabel('Conteo', fontsize=16)
                plt.tight_layout()
            except: 
                sns.countplot(data=self.dataframe, x=categorical_columns[0])
                plt.title(f'Distribución de {categorical_columns[0]}', fontsize=20)
                plt.xlabel(categorical_columns[0], fontsize=16)
                plt.ylabel('Conteo', fontsize=16)
        else:
            print("No hay columnas categóricas en el DataFrame.")

    def visualizar_categoricas_numericas(self):
        """
        Genera gráficos de dispersión para las variables numéricas vs todas las variables categóricas.

        Params:
            - Ninguno.

        Returns:
            - None.
        """
        categorical_columns = self.dataframe.select_dtypes(include=['object', 'category']).columns
        numerical_columns = self.dataframe.select_dtypes(include=np.number).columns
        if len(categorical_columns) > 0:
            for num_col in numerical_columns:
                try:
                    _, axes = plt.subplots(nrows=len(categorical_columns), ncols=1, figsize=(10, 5 * len(categorical_columns)))
                    axes = axes.flat
                    plt.suptitle(f'Dispersión {num_col} vs variables categóricas', fontsize=24)
                    for indice, cat_col in enumerate(categorical_columns):
                        sns.scatterplot(x=num_col, y=self.dataframe.index, hue=cat_col, data=self.dataframe, ax=axes[indice])
                        axes[indice].set_xlabel(num_col, fontsize=16)
                        axes[indice].set_ylabel('Índice', fontsize=16)
                        axes[indice].legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)
                    plt.tight_layout()
                except: 
                    sns.scatterplot(x=num_col, y=self.dataframe.index, hue=categorical_columns[0], data=self.dataframe)
                    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=10)
                    plt.xlabel(num_col, fontsize=16)
                    plt.ylabel('Índice', fontsize=16)
        else:
            print("No hay columnas categóricas en el DataFrame.")

    def correlacion(self, metodo="pearson", tamanio=(14, 8)):
        """
        Genera un heatmap de la matriz de correlación de las variables numéricas del DataFrame.

        Params:
            - metodo : str, optional, default: "pearson". Método para calcular la correlación.
            - tamanio : tuple of int, optional, default: (14, 8). Tamaño de la figura del heatmap.

        Returns:
            - None.
        """
        plt.figure(figsize=tamanio)
        mask = np.triu(np.ones_like(self.dataframe.corr(numeric_only=True), dtype=np.bool_))
        sns.heatmap(self.dataframe.corr(numeric_only=True, method=metodo), annot=True, cmap='viridis', vmax=1, vmin=-1, mask=mask)
        plt.title("Correlación de las variables numéricas", fontsize=24)



class Preprocesado:
    """
    Clase para realizar preprocesamiento de datos en un DataFrame.

    Atributos:
        - dataframe : pd.DataFrame. El conjunto de datos a ser preprocesado.
    """
    
    def __init__(self, dataframe):
        """
        Inicializa la clase Preprocesado con un DataFrame.

        Params:
            - dataframe : pd.DataFrame. El DataFrame que contiene los datos a ser preprocesados.
        """
        self.dataframe = dataframe

    def estandarizar(self):
        """
        Estandariza las columnas numéricas del DataFrame.

        Este método ajusta y transforma las columnas numéricas del DataFrame utilizando `StandardScaler` para que
        tengan media 0 y desviación estándar 1.

        Returns:
            - pd.DataFrame. El DataFrame con las columnas numéricas estandarizadas.
        """
        # Sacamos el nombre de las columnas numéricas
        col_numericas = self.dataframe.select_dtypes(include=np.number).columns

        # Inicializamos el escalador para estandarizar los datos
        scaler = StandardScaler()

        # Ajustamos los datos y los transformamos
        X_scaled = scaler.fit_transform(self.dataframe[col_numericas])

        # Sobreescribimos los valores de las columnas en el DataFrame
        self.dataframe[col_numericas] = X_scaled

        return self.dataframe
    
    def frequency_encoding(self, col_encode):
        """
        Realiza codificación de frecuencia en las columnas especificadas en el diccionario de codificación.

        Returns:
        - dataframe: DataFrame de pandas, el DataFrame con codificación de frecuencia aplicada.
        """
        # si hay contenido en la lista 
        if col_encode:

            # iteramos por cada una de las columnas a las que les queremos aplicar este tipo de encoding
            for categoria in col_encode:

                # calculamos las frecuencias de cada una de las categorías
                frecuencia = self.dataframe[categoria].value_counts(normalize=True)

                # mapeamos los valores obtenidos en el paso anterior, sobreescribiendo la columna original
                self.dataframe[categoria] = self.dataframe[categoria].map(frecuencia)
        
        return self.dataframe
    
    def one_hot_encoding(self, col_encode):
        """
        Realiza codificación one-hot en las columnas especificadas en el diccionario de codificación.

        Returns:
            - dataframe: DataFrame de pandas, el DataFrame con codificación one-hot aplicada.
        """
        # si hay contenido en la lista 
        if col_encode:

            # instanciamos la clase de OneHot
            one_hot_encoder = OneHotEncoder()

            # transformamos los datos de las columnas almacenadas en la variable col_code
            trans_one_hot = one_hot_encoder.fit_transform(self.dataframe[col_encode])

            # el objeto de la transformación del OneHot es necesario convertilo a array (con el método toarray()), para luego convertilo a DataFrame
            # además, asignamos el valor de las columnas usando el método get_feature_names_out()
            oh_df = pd.DataFrame(trans_one_hot.toarray(), columns=one_hot_encoder.get_feature_names_out())

            # concatenamos los resultados obtenidos en la transformación con el DataFrame original
            self.dataframe = pd.concat([self.dataframe.reset_index(drop=True), oh_df.reset_index(drop=True)], axis=1)

            #self.dataframe.drop(columns=[col_encode], inplace=True)
    
        return self.dataframe, one_hot_encoder


class Clustering:
    """
    Clase para realizar varios métodos de clustering en un DataFrame.

    Atributos:
        - dataframe : pd.DataFrame. El conjunto de datos sobre el cual se aplicarán los métodos de clustering.
    """
    
    def __init__(self, dataframe):
        """
        Inicializa la clase Clustering con un DataFrame.

        Params:
            - dataframe : pd.DataFrame. El DataFrame que contiene los datos a los que se les aplicarán los métodos de clustering.
        """
        self.dataframe = dataframe
        self.diccionario_modelos = {}
    
    def sacar_clusters_kmeans(self, n_clusters=(2, 15)):
        """
        Utiliza KMeans y KElbowVisualizer para determinar el número óptimo de clusters basado en la métrica de silhouette.

        Params:
            - n_clusters : tuple of int, optional, default: (2, 15). Rango de número de clusters a probar.
        
        Returns:
            None
        """
        model = KMeans()
        visualizer = KElbowVisualizer(model, k=n_clusters, metric='silhouette')
        visualizer.fit(self.dataframe)
        visualizer.show()
    
    def modelo_kmeans(self, dataframe_original, num_clusters):
        """
        Aplica KMeans al DataFrame y añade las etiquetas de clusters al DataFrame original.

        Params:
            - dataframe_original : pd.DataFrame. El DataFrame original al que se le añadirán las etiquetas de clusters.
            - num_clusters : int. Número de clusters a formar.

        Returns:
            - pd.DataFrame. El DataFrame original con una nueva columna para las etiquetas de clusters.
        """
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        km_fit = kmeans.fit(self.dataframe)
        labels = km_fit.labels_
        dataframe_original["clusters_kmeans"] = labels.astype(str)

        self.diccionario_modelos["kmeans"]=dataframe_original

        return dataframe_original, labels
    
    def visualizar_dendrogramas(self, lista_metodos=["average", "complete", "ward"]):
        """
        Genera y visualiza dendrogramas para el conjunto de datos utilizando diferentes métodos de distancias.

        Params:
            - lista_metodos : list of str, optional, default: ["average", "complete", "ward"]. Lista de métodos para calcular las distancias entre los clusters. Cada método generará un dendrograma
                en un subplot diferente.

        Returns:
            None
        """
        _, axes = plt.subplots(nrows=1, ncols=len(lista_metodos), figsize=(20, 8))
        axes = axes.flat

        for indice, metodo in enumerate(lista_metodos):
            sch.dendrogram(sch.linkage(self.dataframe, method=metodo),
                           labels=self.dataframe.index, 
                           leaf_rotation=90, leaf_font_size=4,
                           ax=axes[indice])
            axes[indice].set_title(f'Dendrograma usando {metodo}')
            axes[indice].set_xlabel('Muestras')
            axes[indice].set_ylabel('Distancias')
    
    def modelo_aglomerativo_malo(self, num_clusters, metodo_distancias, dataframe_original):
        """
        Aplica clustering aglomerativo al DataFrame y añade las etiquetas de clusters al DataFrame original.

        Params:
            - num_clusters : int. Número de clusters a formar.
            - metodo_distancias : str. Método para calcular las distancias entre los clusters.
            - dataframe_original : pd.DataFrame. El DataFrame original al que se le añadirán las etiquetas de clusters.

        Returns:
            - pd.DataFrame. El DataFrame original con una nueva columna para las etiquetas de clusters.
        """
        modelo = AgglomerativeClustering(
            linkage=metodo_distancias,
            distance_threshold=None,
            n_clusters=num_clusters
        )

        aglo_fit = modelo.fit(self.dataframe)
        labels = aglo_fit.labels_
        dataframe_original["clusters_agglomerative"] = labels.astype(str)
        return dataframe_original
    
    def modelo_aglomerativo(self, clusters_min=2, clusters_max=5, linkage_methods = ['single', 'complete', 'average', 'ward'], distance_metrics = ['euclidean', 'cosine', 'chebyshev']):
        
        # Crear un DataFrame para almacenar los resultados
        results = []

        # Suponiendo que tienes un DataFrame llamado df_copia
        # Aquí df_copia debería ser tu conjunto de datos
        # Asegúrate de que esté preprocesado adecuadamente (normalizado si es necesario)

        for linkage_method in linkage_methods:
            for metric in distance_metrics:
                for cluster in tqdm(range(clusters_min, clusters_max)):
                    print(f"Estoy ejecutando {linkage_method} con {metric} y {cluster} clusters")
                    try:
                        # Configurar el modelo de AgglomerativeClustering
                        modelo = AgglomerativeClustering(
                            linkage=linkage_method,
                            metric=metric,  
                            distance_threshold=None,  # Para buscar n_clusters
                            n_clusters=cluster, # Cambia esto según tu análisis
                        )
                        
                        # Ajustar el modelo
                        labels = modelo.fit_predict(self.dataframe)

                        # Calcular métricas si hay más de un cluster
                        if len(np.unique(labels)) > 1:
                            # Silhouette Score
                            silhouette_avg = silhouette_score(self.dataframe, labels, metric=metric)

                            # Davies-Bouldin Index
                            db_score = davies_bouldin_score(self.dataframe, labels)

                            # Cardinalidad (tamaño de cada cluster)
                            cluster_cardinality = {cluster: sum(labels == cluster) for cluster in np.unique(labels)}
                        
                        else:
                            cluster_cardinality = {'Cluster único': len(self.dataframe)}

                        # Almacenar resultados
                        results.append({
                            'linkage': linkage_method,
                            'metric': metric,
                            'silhouette_score': silhouette_avg,
                            'davies_bouldin_index': db_score,
                            'cluster_cardinality': cluster_cardinality,
                            'n_cluster': cluster
                        })

                    except Exception as e:
                        print(f"Error con linkage={linkage_method}, metric={metric}: {e}")

        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values(by='silhouette_score', ascending=False)

        return results_df
    
    def modelo_divisivo(self, dataframe_original, threshold=0.5, max_clusters=5):
        """
        Implementa el clustering jerárquico divisivo.

        Params:
            - dataframe_original : pd.DataFrame. El DataFrame original al que se le añadirán las etiquetas de clusters.
            - threshold : float, optional, default: 0.5. Umbral para decidir cuándo dividir un cluster.
            - max_clusters : int, optional, default: 5. Número máximo de clusters deseados.

        Returns:
            - pd.DataFrame. El DataFrame original con una nueva columna para las etiquetas de los clusters.
        """
        def divisive_clustering(data, current_cluster, cluster_labels):
            # Si el número de clusters actuales es mayor o igual al máximo permitido, detener la división
            if len(set(current_cluster)) >= max_clusters:
                return current_cluster

            # Aplicar KMeans con 2 clusters
            kmeans = KMeans(n_clusters=2)
            kmeans.fit(data)
            labels = kmeans.labels_

            # Calcular la métrica de silueta para evaluar la calidad del clustering
            silhouette_avg = silhouette_score(data, labels)

            # Si la calidad del clustering es menor que el umbral o si el número de clusters excede el máximo, detener la división
            if silhouette_avg < threshold or len(set(current_cluster)) + 1 > max_clusters:
                return current_cluster

            # Crear nuevas etiquetas de clusters
            new_cluster_labels = current_cluster.copy()
            max_label = max(current_cluster)

            # Asignar nuevas etiquetas incrementadas para cada subcluster
            for label in set(labels):
                cluster_indices = np.where(labels == label)[0]
                new_label = max_label + 1 + label
                new_cluster_labels[cluster_indices] = new_label

            # Aplicar recursión para seguir dividiendo los subclusters
            for new_label in set(new_cluster_labels):
                cluster_indices = np.where(new_cluster_labels == new_label)[0]
                new_cluster_labels = divisive_clustering(data[cluster_indices], new_cluster_labels, new_cluster_labels)

            return new_cluster_labels

        # Inicializar las etiquetas de clusters con ceros
        initial_labels = np.zeros(len(self.dataframe))

        # Llamar a la función recursiva para iniciar el clustering divisivo
        final_labels = divisive_clustering(self.dataframe.values, initial_labels, initial_labels)

        # Añadir las etiquetas de clusters al DataFrame original
        dataframe_original["clusters_divisive"] = final_labels.astype(int).astype(str)

        return dataframe_original

    def modelo_espectral(self, dataframe_original, n_clusters=3, assign_labels='kmeans'):
        """
        Aplica clustering espectral al DataFrame y añade las etiquetas de clusters al DataFrame original.

        Params:
            - dataframe_original : pd.DataFrame. El DataFrame original al que se le añadirán las etiquetas de clusters.
            - n_clusters : int, optional, default: 3. Número de clusters a formar.
            - assign_labels : str, optional, default: 'kmeans'. Método para asignar etiquetas a los puntos. Puede ser 'kmeans' o 'discretize'.

        Returns:
            - pd.DataFrame. El DataFrame original con una nueva columna para las etiquetas de clusters.
        """
        spectral = SpectralClustering(n_clusters=n_clusters, assign_labels=assign_labels, random_state=0)
        labels = spectral.fit_predict(self.dataframe)
        dataframe_original["clusters_spectral"] = labels.astype(str)
        return dataframe_original
    
    def modelo_dbscan(self, dataframe_original, eps_values=[0.5, 1.0, 1.5], min_samples_values=[5, 10, 15, 20]):
        """
        Aplica DBSCAN al DataFrame y añade las etiquetas de clusters al DataFrame original.

        Params:
            - dataframe_original : pd.DataFrame. El DataFrame original al que se le añadirán las etiquetas de clusters.
            - eps_values : list of float, optional, default: [0.5, 1.0, 1.5]. Lista de valores para el parámetro eps de DBSCAN.
            - min_samples_values : list of int, optional, default: [3, 2, 1]. Lista de valores para el parámetro min_samples de DBSCAN.

        Returns:
            - pd.DataFrame. El DataFrame original con una nueva columna para las etiquetas de clusters.
        """
        best_eps = None
        best_min_samples = None
        best_silhouette = -1  # Usamos -1 porque la métrica de silueta varía entre -1 y 1

        metrics_results_dbscan = []

        # Iterar sobre diferentes combinaciones de eps y min_samples
        for eps in eps_values:
            for min_samples in tqdm(min_samples_values):
                # Aplicar DBSCAN
                dbscan = DBSCAN(eps=eps, min_samples=min_samples)
                labels = dbscan.fit_predict(self.dataframe)

                # Calcular la métrica de silueta, ignorando etiquetas -1 (ruido)
                if len(set(labels)) > 1 and len(set(labels)) < len(labels):
                    silhouette = silhouette_score(self.dataframe, labels)
                    davies_bouldin = davies_bouldin_score(self.dataframe, labels)
                    
                    unique, counts = np.unique(labels, return_counts=True)
                    cardinalidad = dict(zip(unique, counts))
                    metrics_results_dbscan.append({
                        "eps": eps,
                        "min_samples": min_samples,
                        "silhouette_score": silhouette,
                        "davies_bouldin_score": davies_bouldin,
                        "cardinality": cardinalidad,
                        "num_clusters": len(unique)
                    })
                
                else:
                    silhouette = -1
                    davies_bouldin = -1
             
                # Actualizar el mejor resultado si la métrica de silueta es mejor
                if silhouette > best_silhouette:
                    best_silhouette = silhouette
                    best_eps = eps
                    best_min_samples = min_samples

        try:
            # Mostrar las métricas en un DataFrame para análisis posterior
            metrics_df_dbscan = pd.DataFrame(metrics_results_dbscan).sort_values(by = "silhouette_score", ascending=False)
            display(metrics_df_dbscan)

            # Aplicar DBSCAN con los mejores parámetros encontrados
            print(f"best_eps: {best_eps}, best_min_samples: {best_min_samples}")
            best_dbscan = DBSCAN(eps=best_eps, min_samples=best_min_samples)
            best_labels = best_dbscan.fit_predict(self.dataframe)

            # Añadir los labels al DataFrame original
            dataframe_original["clusters_dbscan"] = best_labels

        except:
            print("Todos los puntos son ruido o están en el mismo cluster")

        return dataframe_original

    def calcular_metricas(self, labels: np.ndarray):
        """
        Calcula métricas de evaluación del clustering.
        """
        if len(set(labels)) <= 1:
            raise ValueError("El clustering debe tener al menos 2 clusters para calcular las métricas.")

        silhouette = silhouette_score(self.dataframe, labels)
        davies_bouldin = davies_bouldin_score(self.dataframe, labels)

        unique, counts = np.unique(labels, return_counts=True)
        cardinalidad = dict(zip(unique, counts))

        return pd.DataFrame({
            "silhouette_score": silhouette,
            "davies_bouldin_index": davies_bouldin,
            "cardinalidad": [cardinalidad]
        }, index = [0])
    
    def plot_clusters(self, df=pd.DataFrame(), col_clusters=None):
        
        if df.empty:
            df = self.diccionario_modelos["kmeans"]

        if col_clusters == None:
            col_clusters = "clusters_kmeans"

        columnas_plot = df.columns.drop(col_clusters)
        columnas_plot

        fig, axes = plt.subplots(nrows=2, ncols=math.ceil(len(columnas_plot)/2), figsize=(20,8))
        axes = axes.flat

        for indice, col in enumerate(columnas_plot):
            df_grop = df.groupby(col_clusters)[col].mean().reset_index()
            sns.barplot(x=col_clusters, y=col, data=df_grop, ax=axes[indice], palette="coolwarm")
            axes[indice].set_title(col)

        if (len(columnas_plot)) % 2 == 1:
            fig.delaxes(axes[-1])

        plt.tight_layout()
        plt.show

    def radar_plot(self, metrica, df=None, figsize=(8, 8)):

        try:
            df_metrica = self.diccionario_modelos[metrica]
        except:
            df_metrica=df

        col_metrica = f"clusters_{metrica}"
        variables = df_metrica.drop(columns=[col_metrica]).columns

        # Agrupar por cluster y calcular la media
        cluster_means = df_metrica.groupby(col_metrica)[variables].mean()

        # Repetir la primera columna al final para cerrar el radar
        cluster_means = pd.concat([cluster_means, cluster_means.iloc[:, 0:1]], axis=1)

        # Crear los ángulos para el radar plot
        num_vars = len(variables)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]  # Cerrar el gráfico

        # Crear el radar plot
        fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(polar=True))

        # Dibujar un gráfico para cada cluster
        for i, row in cluster_means.iterrows():
            ax.plot(angles, row, label=f'Cluster {i}')
            ax.fill(angles, row, alpha=0.25)

        # Configurar etiquetas de los ejes
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(variables)

        # Añadir leyenda y título
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        plt.title('Radar Plot de los Clusters', size=16)
        plt.show()

    def show_cols_clusters(self, df_inicial, col_cluster_name, figsize=(15,15)):
        """
            Devuelve una gráfica con cada columna dividida por clusters

            Params:
                - df_inical : pd.DataFrame. Es el df original antes de hacer encoding o scaler y con una nueva columna que indique a que cluster pertenece cada registro.
                - col_cluster_name : str. Es el nombre de la neva columna del df_inicial donde se indica a que cluster pertenece cada registro.

            Returns:
                - pd.DataFrame. El DataFrame original con una nueva columna para las etiquetas de clusters.
        """

        col_cat = df_inicial.select_dtypes(exclude=np.number).columns
        col_num = df_inicial.select_dtypes(include=np.number).columns
        lista_clusters = df_inicial[col_cluster_name].unique()

        num_nrows = (len(col_cat) + len(col_num)*len(lista_clusters)) / len(col_num)

        fig, axes = plt.subplots(nrows=math.ceil(num_nrows), ncols=len(col_num), figsize=figsize)
        axes = axes.flat


        indice=0
        for clust in lista_clusters:
            df_aux = df_inicial[df_inicial[col_cluster_name]==clust]

            for col in col_num:
                sns.histplot(df_aux, x=col, bins=50, ax=axes[indice])
                axes[indice].set_title(f"Distribución de {col} para el cluster {clust}")
                indice+=1


        for col in col_cat:
            print(f"columna: {col}")
            sns.countplot(df_inicial, x=col, hue=col_cluster_name, ax=axes[indice])
            indice+=1

        if num_nrows % 2 != 0:
            fig.delaxes(axes[-1])

        plt.tight_layout()
        plt.show()