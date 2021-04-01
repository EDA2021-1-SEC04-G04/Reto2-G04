"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
import time
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de videos

def initCatalog(tipo: int):
    list_type = def_type_list(tipo)
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog(list_type)
    return catalog

# Funciones para la carga de datos

def def_type_list(typ:int):
    if typ == 1:
        x = "ARRAY_LIST"
    else:
        x = "LINKED_LIST"
    return x

def loadData(catalog,typ):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    # MEDICION TIEMPO Y MEMORIA
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    list_type = def_type_list(typ)
    loadCategories(catalog)
    loadVideos(catalog,list_type)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return delta_time, delta_memory
    #sortVideos(catalog)



def loadCategories(catalog):
    """
    Carga todos los tags del archivo y los agrega a la lista de tags
    """
    categoryfile = cf.data_dir + 'category-id.csv'
    input_file = csv.DictReader(open(categoryfile, encoding='utf-8'),delimiter = '\t')
    for category in input_file:
        model.addCategory(catalog, category)
    return catalog


def loadVideos(catalog,typ):
    """
    Carga los videos del archivo.  Por cada video se toman su canal y por
    cada uno de ellos, se crea en la lista de canales, a dicho canal y una
    referencia al video que se esta procesando.
    """
    videosfile = cf.data_dir + 'videos-5pct.csv'
    input_file = csv.DictReader(open(videosfile, encoding='utf-8'))
    for video in input_file:
        model.addVideo(catalog, video, typ)

# Funciones de ordenamiento

def videos_by_views(catalog,sort,size)->list:
    """
    Organiza la lista por número de views
    """
    catalog_videos = catalog
    return model.sortVideosbyViews(catalog,sort,size)

def videos_by_likes(catalog)->list:
    """
    Organiza la lista por número de likes
    """
    return model.sort_videos_by_likes(catalog)

# Funciones de consulta sobre el catálogo

def look_for_country(countries,country):
    """
    Filtra una lista de videos por un país dado
    """
    return model.look_for_country(countries,country)

def look_for_category(countries,category):
    """
    Filtra una lista de videos por una categoría dada
    """
    return model.look_for_category(countries,category)

def look_for_most_trending(categories):
    """
    Busca el video con más tiempo trending
    """
    return model.look_for_most_trending(categories)

def look_for_tags(countries,tag):
    """
    Filtra una lista de videos por un tag dado
    """
    return model.look_for_tags(countries,tag)


#FUNCIONES TIEMPO
def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory