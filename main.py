import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter



class Datos:
    def __init__(self,datos_limpios=None,datos_crudos=None):
        self.datos_limpios = datos_limpios
        self.datos_crudos = datos_crudos
        self.clase_category = self.Category()



##---limpieza de datos---##
    def cargar_dataset(self,file_path='amazon_canada_dataset.csv'):
        self.datos_crudos = pd.read_csv(file_path)

    def identificar_y_eliminar_null_values(self):
        "Muestra los datos faltantes de un DataFrame y luego los elimina"
        
        if self.datos_crudos.isna().any(axis=0).any():
            num_valores_no_nulos = self.datos_crudos.count()
            total_filas = len(self.datos_crudos)
            valores_faltantes = total_filas - num_valores_no_nulos
            resumen_faltantes = pd.DataFrame({'Valores Faltantes': valores_faltantes})
            print(resumen_faltantes)
            self.datos_crudos = self.datos_crudos.dropna()
            print(self.datos_crudos)
            
        else:
            print("No hay valores faltantes")

    def identificar_valores_duplicados(self):
        "La funcion revisa si hay valores duplicados, en caso de ser True los eliminara y retornara la lista limpia"
        if self.datos_crudos is not None:
            duplicados = self.datos_crudos.duplicated(subset=['title', 'imgUrl', 'productURL'], keep=False)
            if duplicados.any():
                self.datos_crudos = self.datos_crudos.drop_duplicates(subset=['title', 'imgUrl', 'productUrl'])
                
            else:
                print("No hay duplicados en el Dataframe")
        else:
            print("El dataframe esta vacio")
    
    def guardar_datos_limpios(self,file_path='datos_limpios.csv'):
        if self.datos_limpios is not None:
            self.datos_limpios.to_csv(file_path, index=False)
        else:
            print("Dataframe sin datos que guardar")

##----Analisis de tendencias de precio por categoria----##
    class Category:
        def __init__(self,datos_por_categoria=None,precio_promedio=None,datos=None):
            self.datos_por_categoria= datos_por_categoria
            self.precio_promedio = precio_promedio #Precio promedio por categoria
            self.datos = datos

##----Manejo de datos----##
        def cargar_dataset(self,file_path='datos_limpios.csv'):
            self.datos = pd.read_csv(file_path)

        def agrupar_datos_por_categoria(self):

            if self.datos is not None:
                df = self.datos.sort_index()
                self.datos_por_categoria = df.groupby('categoryName')
            else:
                print("Los datos limpios estan vacios")

        def calcular_precio_promedio(self):
            if self.datos_por_categoria is not None:
                self.precio_promedio = self.datos_por_categoria['price'].mean().reset_index()
            else:
                print("el Dataframe datos por categoria esta vacio")

##-----Visualización de datos-----##
        def visualizar_tendencias_categoria_alta(self):
            "Toma el dataframe en precio_promedio que esta agrupado por categoria y lo grafica para indentificar las 10 categorias con precio medio mas alto"
            if self.precio_promedio is not None or False:
                precio_promedio_alto = self.precio_promedio.nlargest(10,'price')
                precio_promedio_alto.set_index('categoryName', inplace=True)
                precio_promedio_alto.plot(kind='bar', color='skyblue', figsize=(10, 6))
                # Añadir etiquetas y título
                plt.xlabel('Categorías')
                plt.ylabel('Precio Medio')
                plt.title('Top 10 Categorías con Precios Medios Más Alto en Dolares')
                # Rotar las etiquetas del eje x
                plt.xticks(rotation=45, ha='right')
                # Ajustar el diseño para evitar cortar las etiquetas
                plt.tight_layout()
                # Mostrar la gráfica
                plt.show()

        def visualizar_tendencias_categoria_baja(self):
            "Toma el dataframe en precio_promedio que esta agrupado por categoria y lo grafica para indentificar las 10 categorias con precio medio mas bajos"
            if self.precio_promedio is not None or False:
                precio_promedio_alto = self.precio_promedio.nsmallest(10,'price').reset_index()
                precio_promedio_alto.set_index('categoryName', inplace=True)
                precio_promedio_alto.plot(kind='bar', color='red', figsize=(10, 6))
                # Añadir etiquetas y título
                plt.xlabel('Categorías')
                plt.ylabel('Precio Medio')
                plt.title('Top 10 Categorías con Precios Medios Más Alto en Dolares')
                # Rotar las etiquetas del eje x
                plt.xticks(rotation=45, ha='right')
                # Ajustar el diseño para evitar cortar las etiquetas
                plt.tight_layout()
                # Mostrar la gráfica
                plt.show()

        def vizualizar_categorias_ventas_altas(self):
            "Toma el dataframe ordenado por categorias y grafica las categorias con mas ventas por unidad del ultimo mes"
            def formato_miles(valor, _):
                return f'{int(valor / 1000)}'
            if self.datos_por_categoria is not None or False:
                # 1. Calcular las ventas por categoría
                ventas_por_categoria = self.datos_por_categoria['boughtInLastMonth'].sum()
                top_10_categorias = ventas_por_categoria.nlargest(10)
                top_10_categorias.plot(kind='bar', color='green')
                formatter = FuncFormatter(formato_miles)
                plt.xlabel('Categorías')
                plt.ylabel('Ventas totales')
                plt.title('Top 10 Categorías con mas ventas en el ultimo mes')
                # Rotar las etiquetas del eje x
                plt.xticks(rotation=45, ha='right')
                # Ajustar el diseño para evitar cortar las etiquetas
                plt.tight_layout()
                plt.gca().yaxis.set_major_formatter(formatter)
                # Mostrar la gráfica
                plt.show()
        
        def vizualizar_productos_ventas_altas(self):
            "Toma el dataframe en self.datos, filtra los 10 productos con mas ventas y los grafica en un pie charts"
            if self.datos is not None:
                
                datos_filtrados = self.datos.nlargest(10,'boughtInLastMonth')
                sizes = datos_filtrados['boughtInLastMonth']
                labels = datos_filtrados['title']
                plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                plt.axis('equal')  
                plt.title('Distribución de Ventas de los 10 productos mas vendidos')
                plt.show()

        def vizualizar_productos_reseñas_calificacion(self):
            "Toma el dataframe en self.datos, filtra los 10 productos con mas reseñas y calificaciones y los grafica"
            if self.datos is not None:
                datos_filtrados = self.datos.nlargest(10,['stars','reviews'])
                fig, ax = plt.subplots()

                # Ajusta el ancho de la barra según la cantidad de columnas
                bar_width = 0.35

                # Posiciones de las barras
                indices = range(len(datos_filtrados))
                calificaciones = ax.bar(indices, datos_filtrados['stars'], bar_width, label='Calificaciones', alpha=0.7)
                reseñas = ax.bar(indices, datos_filtrados['reviews'], bar_width, label='Reseñas', bottom=datos_filtrados['stars'], alpha=0.7)

                # Configuración del gráfico
                ax.set_xlabel('Productos', fontsize=12)
                ax.set_ylabel('Valores', fontsize=12)
                ax.set_title('Calificaciones y Reseñas de los Productos Principales', fontsize=14)
                ax.set_xticks(indices)
                ax.set_xticklabels(datos_filtrados['title'], rotation=45, ha="right", fontsize=10)  
                ax.legend()
                for i, (calif, res) in enumerate(zip(datos_filtrados['stars'], datos_filtrados['reviews'])):
                    ax.text(i, calif / 2, f'{calif}', ha='center', va='center', color='white', fontsize=10)
                    ax.text(i, calif + res / 2, f'{res}', ha='center', va='center', color='white', fontsize=10)
                plt.subplots_adjust(bottom=0.5)
                plt.tight_layout()  

                plt.show()

            
if __name__== '__main__':
    datos1 = Datos()
    '''datos1.cargar_dataset()
    datos1.identificar_y_eliminar_null_values()
    datos1.identificar_valores_duplicados()
    datos1.datos_limpios = datos1.datos_crudos'''

    datos1.clase_category.cargar_dataset()
    datos1.clase_category.agrupar_datos_por_categoria()
    datos1.clase_category.calcular_precio_promedio()
    datos1.clase_category.vizualizar_productos_reseñas_calificacion()
    

