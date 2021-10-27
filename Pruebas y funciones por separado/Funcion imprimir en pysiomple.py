import sqlite3
import os   #Para listar los ficheros de un directorio
import matplotlib.pyplot as pyplot    #Para hacer el gráfico
import random  #Para obtener numeros al azar
from tkinter import *        #Para hacer la ventana
from tkinter import colorchooser   #Para importar el selector de color de tkinter



def crear_diccionario(fichero):
    '''A esta funcion se le pasa como parametro el fichero en el que tenemos almacenados los datos
    Con este fichero esta fucion nos DEVUELVE un diccionario cuyas claves serán el nombre del gasto y el valor será
    la suma (int) de todos los gastos de ese tipo'''
    try:
        diccionario={}
        f = open(fichero + '.csv')
        longitud=len(f.readlines())
        f.close
        f = open(fichero + '.csv')
        contador=0
        while contador != longitud:
            listalinea=f.readline().strip(', \n').split(',')
            if listalinea[2] in diccionario:
                diccionario[listalinea[2]]+=int(listalinea[3])
            else:
                diccionario[listalinea[2]]=int(listalinea[3])
            contador+=1
                
        return diccionario
    except (TypeError):
        print('\nNo existe aun el modelo introducido. \nHaz click en "Crear Otro Coche" en el menú')
    



def mostrar_grafico():
    '''Obtiene las claves del diccionario, los slices son los valores de cada clave y los colores los obtiene de la funcion
definir_colores()'''
    claves=list(diccionario.keys())
    slices=list(diccionario.values())   #Llamamos asi a los valores para mostrarlo en la grafica
    colores=definir_colores(claves)
    pyplot.pie(slices, colors=colores, labels=claves, autopct='%1.1f%%')  #Con esta linea creamos la grafica
    pyplot.axis('equal') #Para hacer redonda la grafica
    pyplot.title('Resumen de los gastos')  #Le ponemos titulo a la grafica
    #pyplot.legend(labels=claves)  #Ponemos las leyendas de la grafica
    pyplot.show()  #Imprimimos la grafica
    #pyplot.savefig('Imagen.png')    Por si queremos guardarlo en un fichero de imagen
    
    


def prueba(fichero):
    diccionario={}
    f = open(fichero + '.csv')
    a=f.readline()
    print(a)
    

def crear_diccionario(coche):
    lista=[]
    diccionario={}
    con = sqlite3.connect('proyecto.db')
    cur = con.cursor()
    cur.execute('select fecha, kms, concepto, detalle, coste from gasto where matricula="{}"'.format(coche))
    tablas = cur.fetchall()
    for u in tablas:
        lista.append(u)
    #print(lista)

    for e in lista:
        if e[2] in diccionario:
             diccionario[e[2]]+=e[4]
        else:
            diccionario[e[2]]=int(e[4])
    return diccionario
    
    
    

    