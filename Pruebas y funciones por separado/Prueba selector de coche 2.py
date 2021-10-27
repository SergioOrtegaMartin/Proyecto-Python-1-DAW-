'''funcion que cuando cree un fichero me cree otro fichero en el que almacenamos los nombres de los ficheros
para poder acceder mas tarde a todos esos nombres'''

import os   #Para listar los ficheros de un directorio
import matplotlib.pyplot as pyplot    #Para hacer el gráfico
import random  #Para obtener numeros al azar
from tkinter import *        #Para hacer la ventana
from tkinter import colorchooser   #Para importar el selector de color de tkinter

def llamada_nuevo():
    def nuevo_coche(fichero):
        '''A esta funcion se le pasa como parametro un fichero al cual le introduciremos los datos que queramos.
            No devuelve nada, solo almacena los datos en nuestro fichero'''
        f = open(fichero + '.csv', 'a')

    fichero=input('Introduce el nombre del coche: \n')
    nuevo_coche(fichero)

def elegir_coche():
    '''devuelve una lista con los archivos .csv que hay en el directorio,
cada archivo csv será donde guardemos los gastos de cada coche'''
    contenido = os.listdir()

    csv=[]

    for fichero in contenido:
        if fichero.endswith('.csv'):
            csv.append(fichero)
    print('Los coches almacenados en el sistema son: \n')
    for e in csv:
        print(e.rstrip('csv').rstrip('.'))
    
    
    nombre_fichero= input('Introduce el que quieres elegir:   \n ')
    if nombre_fichero+'.csv' not in csv:
        print('')
    else:
        return nombre_fichero

fichero=elegir_coche()





def llamada_registrar():
    '''Funcion que llama a la funcion registrar_gastos() porque el tkinter no permite pasarle parametros'''
    
    def registrar_gasto(fichero):
        '''A esta funcion se le pasa como parametro un fichero al cual le introduciremos los datos que queramos.
            No devuelve nada, solo almacena los datos en nuestro fichero'''
        try:
            f = open(fichero + '.csv', 'a')
            
            print('Escribirás linea a linea hasta que introduzcas el nombre vacio')

            fecha = input('Introduce la fecha: \n')
            f.write(fecha + ',')
            kms = input('Introduce los kilometros: \n')
            f.write(kms + ',')
            tipo = input('Introduce tipo de gasto:  \n' )
            f.write(tipo + ',')
            coste = input('Introduce el coste:  \n' )
            f.write(coste + ',')
            f.write('\n')
                
        except(PermissionError):
            print('No tienes permisos para abrir el archivo, prueba a cerrarlo si lo tienes abierto con otro programa')
    registrar_gasto(fichero)


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
    

diccionario=crear_diccionario(fichero)



def definir_colores(listaclaves):
    '''Le pasamos como parametro una lista (obtenida en la funcion mostrar_grafico()) para saber la longitud de la lista a devolver
nos devuelve una lista con tantos colores como claves haya(longitud de la lista de claves)
La lista que nos devuelve la usamos en la funcion de mostrar_grafico()'''
    print('')
    colores=['aquamarine','azure','beige','blue','brown','chartreuse','chocolate','coral','crimson','cyan','fuchsia','gold','green','grey','ivory','khaki','lavender','lightblue','lightgreen','lime','magenta','maroon','olive','orange','orchid','pink','plum','purple','red','salmon','sienna','silver','tan','teal','turquoise','violet','wheat','yellow','yellowgreen']
    entrada=input('¿Quieres elegir los colores al azar? S/N \n')
    if entrada =='s' or entrada =='S':
        desordenados=[]
        for e in listaclaves:
            desordenados.append(colores[random.randint(0, len(colores)-1 )])
        return desordenados
    else:
        ordenados=[]
        for e in listaclaves:
            root=Tk()
            root.title('Selector de color')
            root.geometry('200x5')
            color=colorchooser.askcolor()
            ordenados.append(str(color[-1]))
            root.destroy()
        return ordenados
        
    


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

def cerrar_ventana():
    '''Cierra la ventana de Tkinter'''
    ventana.destroy()

def llamada_resumengeneral():

    def mostrar_resumen(fichero):
        '''A esta funcion se le pasa como parametro el fichero en el que tenemos almacenados los datos
        Con este fichero esta fucion nos DEVUELVE un diccionario cuyas claves serán el nombre del gasto y el valor será
        la suma (int) de todos los gastos de ese tipo'''
        print('')
        f = open(fichero + '.csv')
        longitud=len(f.readlines())
        f.close
        f = open(fichero + '.csv')
        contador=0
        print ('--- Fecha ------ Kms --- Concepto --- €')
        while contador != longitud:
            listalinea=f.readline().strip(', \n').split(',')
            print('{} ---- {} -- {} ---- {}'.format (listalinea[0],listalinea[1],listalinea[2],listalinea[3]))
            contador+=1
    mostrar_resumen(fichero)


def llamada_resumengastos():

    def resumen_gastos(diccionario):
        print('')
        for clave, valor in diccionario.items(): 
            print ("El gasto total en {} es de {} €".format (clave, valor))
    
    
    resumen_gastos(diccionario)




ventana=Tk()
ventana.config(bg="pink")
ventana.geometry("550x250")
ventana.resizable(width=TRUE, height=TRUE)
ventana.title("Menú")
#definimos 2 botones
boton1=Button(ventana,text="Introducir otro dato",command=llamada_registrar).grid(row=2,column=1)
boton2=Button(ventana,text="Mostrar Grafico",command=mostrar_grafico).grid(row=3,column=1)
boton3=Button(ventana,text="Cerrar ventana",command=cerrar_ventana).grid(row=10,column=3)
boton4=Button(ventana,text="Resumen Gastos",command=llamada_resumengastos).grid(row=4,column=1)
boton4=Button(ventana,text="Resumen General",command=llamada_resumengeneral).grid(row=5,column=1)
boton5=Button(ventana,text="Crear Otro Coche",command=llamada_nuevo).grid(row=6,column=1)
etiqueta1=Label(ventana,text="PARA ACTUALIZAR REINICIA EL SCRIPT").grid(row=1,column=2)
ventana.config(bd=15)
ventana.mainloop()





