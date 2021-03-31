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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import time
import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import insertionsort as nsr
from DISClib.Algorithms.Sorting import selectionsort as stn
from DISClib.Algorithms.Sorting import shellsort as shr
from DISClib.Algorithms.Sorting import quicksort as qst
from DISClib.Algorithms.Sorting import mergesort as mst
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog(tipo: str):
    """
    Inicializa el catálogo de videos. Crea una lista vacia para guardar
    todos los videos, adicionalmente, crea una lista vacia para los paises,
    una lista vacia para las categorias y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    catalog = {'Videos': None,
               'Categories': None,
               }

    catalog['Videos'] = lt.newList(tipo, cmpfunction = compareVideos)
    catalog['Categories'] = lt.newList(tipo)
    return catalog

# Funciones para agregar informacion al catalogo

def addCategory(catalog, category):
    """
    Adiciona una cateogría a la lista de categorías
    """
    lt.addLast(catalog['Categories'],category)

def addVideo(catalog, video,typ):
    # Se adiciona el video a la lista de videos y se le agrega su categoria correspondiente
    categories = catalog['Categories']
    category = addVideoCategory(video['category_id'],categories)
    video['category'] = category
    lt.addLast(catalog['Videos'],video)

def addVideoCategory(category_id, categories):
    """
    Cambia la categoria del libro con la correspondiente
    """
    new_category = None
    found = False
    ticker = 0
    while found == False and ticker <len(categories):
        for pos in range(0,lt.size(categories)):
            if lt.getElement(categories,pos)['id'] == category_id:
                new_category = lt.getElement(categories,pos)['name']
                found == True
        ticker +=1
    return new_category

# Funciones para creacion de datos
    
# Funciones de consulta

def look_for_country(videos,country):
    """
    Busca todos los videos que coincidan con un país enviado por parámetro
    y devuelve una lista con todos ellos
    """
    pos = 0
    countries = lt.newList('ARRAY_LIST')
    while pos < lt.size(videos):
        video = lt.getElement(videos,pos)
        if video['country'].lower() == country:
            lt.addLast(countries,video)
        pos +=1
    return countries

def look_for_category(videos,category):
    """
    Busca todos los videos que coincidan con una categoría enviada por parámetro
    y retorna una lista con todos ellos
    """
    pos = 0
    category = " " + category
    categories = lt.newList('ARRAY_LIST')
    while pos < lt.size(videos):
        video = lt.getElement(videos,pos)
        if video['category'].lower() == category:
            lt.addLast(categories,video)
        pos +=1
    return categories

def look_for_most_trending(videos):
    sublist = {}
    masvistas = 0
    videomasvisto  = None
    for x in range(0,lt.size(videos)):
        video = lt.getElement(videos,x)
        if video['video_id'] in sublist:
            sublist[video['video_id']] += 1
            if sublist[video['video_id']] > masvistas:
                masvistas = sublist[video['video_id']]
                videomasvisto = video
        else:
            sublist[video['video_id']] = 1

    return videomasvisto

def look_for_tags(countries,tag):
    """
    Filtra todos los videos con un tag específico, los agrega a 
    una lista y retorna la misma
    """
    pos = 0
    tag = '"' + tag + '"'
    vid_tags = lt.newList('ARRAY_LIST')
    while pos < lt.size(countries):
        video = lt.getElement(countries,pos)
        tags = video['tags'].split("|")
        if tag in tags:
            lt.addLast(vid_tags,video)
        pos +=1
    return vid_tags

# Funciones utilizadas para comparar elementos dentro de una lista

def compareVideos(video1, video2):
    if video2 > video1:
        return 1
    elif video2 == video1:
        return 0
    elif video2 < video1:
        return -1
    
def cmpVideosByViews(video1, video2):
    return float(video1['views']) > float(video2['views'])

def compareCountries(country1, country2):
    if country1 > country2:
        return 1
    elif country1 == country2:
        return 0
    else:
        return -1

def cmpByLikes(Video1,Video2):
    return float(Video1['likes']) < float(Video2['likes'])
    

# Funciones de ordenamiento

def sortVideosbyViews(catalog, ordenamiento, size):
    """
    Organiza todos los videos de una lista por número de views 
    y retorna una nueva lista organizada
    """
    sortedlist = lt.subList(catalog, 0, size)
    sortedlist = sortedlist.copy()
    start_time = time.process_time()
    if ordenamiento == 1:
        sublist = nsr.sort(sortedlist, cmpVideosByViews)
    elif ordenamiento == 2:
        sublist = stn.sort(sortedlist, cmpVideosByViews)
    elif ordenamiento == 3:
        sublist = shr.sort(sortedlist, cmpVideosByViews)
    elif ordenamiento == 4:
        sublist = qst.sort(sortedlist, cmpVideosByViews)
    elif ordenamiento == 5:
        sublist = mst.sort(sortedlist, cmpVideosByViews)
    return sublist

def sort_videos_by_likes(catalog):
    """
    Organiza todos los videos de una lista por número de likes
    y retorna una nueva lista organizada
    """
    sorted_list = lt.subList(catalog,1,lt.size(catalog))
    sorted_list = sorted_list.copy()
    sublist = mst.sort(sorted_list,cmpByLikes)
    return sublist




    