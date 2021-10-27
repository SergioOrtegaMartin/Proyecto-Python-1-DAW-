import matplotlib.pyplot as pyplot
import random
import PySimpleGUI as sg
from tkinter import *
from tkinter import colorchooser


def llamada_registrar():
    fichero='registros'
    def registrar_gasto(fichero):
        try:
            f = open(fichero + '.csv', 'a')
            
            print('Escribirás linea a linea hasta que introduzcas el nombre vacio')

            fecha = input('Introduce la fecha: \n')
            while fecha!= '':
                f.write(fecha + ',')
                kms = input('Introduce los kilometros: \n')
                f.write(kms + ',')
                tipo = input('Introduce tipo de gasto:  \n' )
                f.write(tipo + ',')
                coste = input('Introduce el coste:  \n' )
                f.write(coste + ',')
                f.write('\n')
                fecha = input('Introduce el nombre: \n')
                
        except(PermissionError):
            print('No tienes permisos para abrir el archivo, prueba a cerrarlo si lo tienes abierto con otro programa')
    registrar_gasto(fichero)


def crear_diccionario(fichero):
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
        

#diccionario=crear_diccionario('prueba1')


def definir_colores(listaclaves):
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
    claves=list(diccionario.keys())
    slices=list(diccionario.values())   #Llamamos asi a los valores para mostrarlo en la grafica
    colores=definir_colores(claves)
    pyplot.pie(slices, colors=colores, labels=claves, autopct='%1.1f%%')  #Con esta linea creamos la grafica
    pyplot.axis('equal') #Para hacer redonda la grafica
    pyplot.title('Resumen de los gastos')  #Le ponemos titulo a la grafica
    #pyplot.legend(labels=claves)  #Ponemos las leyendas de la grafica
    pyplot.show()  #Imprimimos la grafica
    #pyplot.savefig('Imagen.png')    Por si queremos guardarlo en un fichero de imagen

ventana=Tk()
ventana.config(bg="aqua")
ventana.geometry("460x360")
ventana.resizable(width=TRUE, height=TRUE)
ventana.title("Ventana de Python")
#definimos 2 botones
boton1=Button(ventana,text="Introducir datos",command=llamada_registrar).grid(row=1,column=1)
boton2=Button(ventana,text="Mostrar Grafico",command=mostrar_grafico).grid(row=2,column=1)



