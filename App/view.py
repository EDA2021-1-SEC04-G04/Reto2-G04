"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
import time
from DISClib.ADT import list as lt
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
assert cf

default_limit = 1000
sys.setrecursionlimit(default_limit*10)
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

catalog = None
def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar los videos de una categoría más vistos en un país")
    print("3- Conocer el video que más días ha sido trending en un país")
    print("4- Averiguar el video que más días ha sido trending en una categoría")
    print("5- Consultar los n videos con un tag específico que más likes han tenido en un país")
    print("0- Salir")

#Funciones de carga

def loadData(catalog,tipo):
    """
    Carga los videos en la estructura de datos
    """
    controller.loadData(catalog,tipo)

#Funciones de requerimiento

def views_country_category(catalog,country,num_countries,category,sort):
    """
    Cumple el requerimiento número 1 del reto buscando los videos 
    con más views en un país con una categoría dada. Imprime el 
    número de videos pedido por el usuario.
    """
    countries = controller.look_for_country(catalog,country)
    categories = controller.look_for_category(countries,category)
    size = lt.size(categories)
    lista_videos = controller.videos_by_views(categories,sort,size)
    printVideosMostViews(lista_videos,country,num_countries,category)
    
def trending_country(catalog, country):
    """
    Cumple el requerimiento número 2 del reto buscando el video
    con más tiempo trending en un país. Imprime este mismo.
    """
    countries = controller.look_for_country(catalog,country)
    most_trending = controller.look_for_most_trending(countries)
    print_most_trending_categories(most_trending, country)

def trending_category(catalog, category):
    """
    Cumple el requerimiento número 3 del reto buscando el video
    con más tiempo trending en una categoría. Imprime este mismo.
    """
    categories = controller.look_for_category(catalog,category)
    most_trending = controller.look_for_most_trending(categories)
    print_most_trending_categories(most_trending, category)

def likes_country_tag(num_videos,country,tag,catalog_videos):
    """
    Cumple el requerimiento número 4 del reto buscando los videos 
    con más likes en un país con un tag específico. Imprime el 
    número de videos pedido por el usuario.
    """
    countries = controller.look_for_country(catalog_videos,country)
    tags = controller.look_for_tags(countries,tag)
    tags_by_likes = controller.videos_by_likes(tags)
    print_video_tags(tags_by_likes,num_videos,country,tag)

#Funciones de impresion

def print_first_element(videos):
    size = lt.size(videos)
    if size:
        primera_linea = "{0:^13}{1:^100}{2:^25}{3:^25}{4:^15}{5:^10}{6:^10}".format('Trending Date','Title','Channel Title','Publish Time','Views','Likes','Dislikes')
        print(primera_linea)
        i = 1
        while i < 2:
            video = lt.getElement(videos,i)
            t_date = video['trending_date']
            title = video['title']
            ch_title = video['channel_title']
            pub_time = video['publish_time']
            views = video['views']
            likes = video['likes']
            dislikes = video['dislikes']
            info_video = "{0:^13}{1:^100}{2:^25}{3:^25}{4:^15}{5:^10}{6:^10}".format(t_date, title, ch_title, pub_time, views, likes, dislikes)
            print(info_video)
            i+=1

def print_categories(categorias):
    """
    Imrpime las categorias con su respectivo id
    """
    size = mp.size(categorias)
    for i in range(0,size):
        ide = mp.getElement(categorias,i)['id']
        categoria = mp.getElement(categorias,i)['name']
        print(ide + ': ' +categoria)

def printVideosMostViews(videos,country,num_countries,category):
    """
    Imprime los n videos con más vistas especficando, su trending date,
    título, título del canal, tiempo de publicación, vistas likes y dislikes.
    """
    size = lt.size(videos)
    if size:
        print(' Estos son los videos con más views en ' + country.title() + " para la categoría " + category + ":")
        primera_linea = "{0:^13}{1:^100}{2:^25}{3:^25}{4:^15}{5:^10}{6:^10}".format('Trending Date','Title','Channel Title','Publish Time','Views','Likes','Dislikes')
        print(primera_linea)
        i = 1
        while i < num_countries and i <size:
            video = lt.getElement(videos,i)
            t_date = video['trending_date']
            title = video['title']
            ch_title = video['channel_title']
            pub_time = video['publish_time']
            views = video['views']
            likes = video['likes']
            dislikes = video['dislikes']
            info_video = "{0:^13}{1:^100}{2:^25}{3:^25}{4:^15}{5:^10}{6:^10}".format(t_date, title, ch_title, pub_time, views, likes, dislikes)
            print(info_video)
            i+=1

def print_most_trending_country(most_trending, category):
    """
    Imprime el video más trending en un país específico. Muestra además su título, el canal
    que lo publicó, el país donde fue publicado y el número de días que ha sido trending
    """
    print('El video mas trending en la categoria ' + category.title() + ":")
    primera_linea = "{0:^100}{1:^25}{2:^15}{3:^15}".format('Title','Channel Title','Pais','Numero de dias')
    print(primera_linea)
    video = most_trending
    title = video['title']
    ch_title = video['channel_title']
    country = video['country']
    info_video = "{0:^100}{1:^25}{2:^15}".format(title, ch_title, country)
    print(info_video)
            
def print_most_trending_categories(most_trending, category):
    """
    Imprime el video más trending en una categoría específica. Muestra además su título, el canal
    que lo publicó, el id de la categoría y el número de días que ha sido trending
    """

    
    print('El video mas trending en la categoria ' + category.title() + ":")
    primera_linea = "{0:^100}{1:^25}{2:^15}".format('Title','Channel Title','Category ID')
    print(primera_linea)
    
    video = most_trending
    title = video['title']
    ch_title = video['channel_title']
    category_id = video['category_id']
    info_video = "{0:^100}{1:^25}{2:^15}".format(title, ch_title, category_id)
    print(info_video)

def print_video_tags(tags_by_likes,num_videos,country,tag):
    """
    Imprime los n videos con más likes especficando, su título, título del canal, tiempo de publicación, 
    vistas likes, dislikes y los tags con los que está marcado el video
    """
    size = lt.size(tags_by_likes)
    if size:
        print(' Estos son los videos con más likes en ' + country.title() + " con el tag " + tag + ':')
        primera_linea = "{0:^100}{1:^25}{2:^25}{3:^15}{4:^10}{5:^10}{6:100}".format('Title','Channel Title','Publish Time','Views','Likes','Dislikes','tags')
        print(primera_linea)
        i = 0
        while i < num_videos and i < size :
            video = lt.getElement(tags_by_likes,i)
            tags= video['tags']
            title = video['title']
            ch_title = video['channel_title']
            pub_time = video['publish_time']
            views = video['views']
            likes = video['likes']
            dislikes = video['dislikes']
            info_video = "{0:^100}{1:^25}{2:^25}{3:^15}{4:^10}{5:^10}{6:100}".format(title, ch_title, pub_time, views, likes, dislikes, tags)
            print(info_video)
            i+=1
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        tipo = int(input("Ingrese 1 si desea un arreglo o cualquier otro caracter para una lista encadenada: "))
        #cambio medida tiempo y memoria
        catalog = controller.initCatalog(tipo)
        answer = loadData(catalog,tipo)

        #print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
        #      "Memoria [kB]: ", f"{answer[1]:.3f}")
        print('Videos cargados: ' + str(lt.size(catalog['Videos'])))
        print('Categorias cargadas: ' + str(mp.size(catalog['Categories'])))
        print('Asociación de Categorías a Videos cargados: ' +
              str(lt.size(catalog['Videos'])))
        print("El primer video cargado fue: ")
        print_first_element(catalog['Videos'])
        print('Las categorias cargadas fueron:')
        #print_categories(catalog['Categories'])     
        #print("MEMORIA : " + str(answer[1])+ " kbs")
        #print("TIEMPO : " + str(answer[0]) + " ms")
        print(answer) 
        
    elif int(inputs[0]) == 2:
        num_countries = int(input("Escriba en numeros la cantidad de videos que desea consultar: "))
        country = input("Escriba el país sobre el que desea hacer la consulta: ").lower()
        category = input("Ingrese la categoria que desea buscar: ")
        #print("\nSeleccione el tipo de ordenamiento:\n-1 para insertion\n-2 para selection\n-3 para shellshort\n-4 para quickshort\n-5 para mergeshort")
        #sort = int(input("Ingrese su eleccion: "))
        sort = 5
        views_country_category(catalog['Videos'],country,num_countries,category,sort)

    elif int(inputs[0]) == 3:
        country = input("Ingrese el pais en el que desea buscar: ")
        trending_country(catalog['Videos'],country)

    elif int(inputs[0]) == 4:
        category = input("Ingrese la categoria en la que desea buscar: ")
        trending_category(catalog['Videos'],category)

    elif int(inputs[0]) == 5:
        num_videos = int(input("Escriba en numeros la cantidad de videos que desea consultar: "))
        country = input("Ingrese el pais en el que desea buscar: ")
        tag = input("Ingrese el tag que desea buscar: ")
        likes_country_tag(num_videos,country,tag,catalog['Videos'])

    else:
        sys.exit(0)
sys.exit(0)
