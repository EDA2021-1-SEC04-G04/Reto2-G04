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
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog(tipo: str, factor:float):
    """
    Inicializa el catálogo de videos. Crea una lista vacia para guardar
    todos los videos, adicionalmente, crea una lista vacia para los paises,
    una lista vacia para las categorias y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    catalog = {'Videos': None,
               'Categories': None,
               'Videos_Category':None,
               'Countries':None
               }

    catalog['Videos'] = lt.newList(tipo, cmpfunction = compareVideos)
    catalog['Categories'] = mp.newMap(35,
                                      maptype=tipo,
                                      loadfactor=factor)
    catalog['Videos_Category'] = mp.newMap(35,
                                      maptype=tipo,
                                      loadfactor=factor                                  
                                      )
    catalog['Countries'] = mp.newMap(240,
                                      maptype=tipo,
                                      loadfactor=factor                                  
                                      )
    return catalog

# Funciones para agregar informacion al catalogo

def addCategory(catalog, category):
    """
    Adiciona una cateogría a la lista de categorías
    """
    
    mp.put(catalog['Categories'], category['id'], category['name'])

def addVideo(catalog, video,typ):
    # Se adiciona el video a la lista de videos y se le agrega su categoria correspondiente
    categories = catalog['Categories']
    videos_by_categories = catalog['Videos_Category']
    videos_by_countries = catalog['Countries']
    category = addVideoCategory(video['category_id'],categories)
    video['category'] = category
    addVideoByCategory(videos_by_categories,video)
    addVideoByCountry(videos_by_countries,video)
    video["tags"] = addtags(video)
    lt.addLast(catalog['Videos'],video)

def addVideoCategory(category_id, categories):
    """
    Cambia la categoria del libro con la correspondiente
    """
    new_category = mp.get(categories,category_id)
    new_category = new_category['value']
    return new_category

def addVideoByCategory(categories,video):
    vid_category = video['category']
    existcategory = mp.contains(categories, vid_category)
    if existcategory:
        entry = mp.get(categories, vid_category)
        category = me.getValue(entry)
    else:
        category = newCategory(vid_category)
        mp.put(categories, vid_category, category)
    lt.addLast(category['Videos'], video)

def addVideoByCountry(countries,video):
    vid_country = video['country']
    existcountry = mp.contains(countries, vid_country)
    if existcountry:
        entry = mp.get(countries, vid_country)
        country = me.getValue(entry)
    else:
        country = newCountry(vid_country)
        mp.put(countries, vid_country, country)
    lt.addLast(country['Videos'], video)

# Funciones para creacion de datos

def newCategory(vid_category):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'category': "", "Videos": None}
    entry['category'] = vid_category
    entry['Videos'] = lt.newList('SINGLE_LINKED', compareCategories)
    return entry

def newCountry(vid_country):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'country': "", "Videos": None}
    entry['country'] = vid_country
    entry['Videos'] = lt.newList('SINGLE_LINKED', compareCountries)
    return entry

# Funciones de consulta
def addtags(video):
    tags = video["tags"].split("|")
    mapatags = mp.newMap(len(tags),maptype="CHAINING",loadfactor=3.0)
    for i in tags:
        mp.put(mapatags, i, True)
    return mapatags

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
    category = category.lower()
    categories = lt.newList('ARRAY_LIST')
    while pos < lt.size(videos):
        video = lt.getElement(videos,pos)
        if video['category'].lower() == (" " + category):
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
        if mp.contains(video["tags"],tag):
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

def compareCategories(cat1, cat2):
    if cat1 == cat:
        return 0
    elif cat1 > cat2:
        return 1
    else:
        return -1

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




    