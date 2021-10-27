import sqlite3   #Trabajar con bases de datos
import PySimpleGUI as sg  #Interface gráfica
import os   #Para listar los ficheros de un directorio
import matplotlib.pyplot as pyplot    #Para hacer el gráfico
import random  #Para obtener numeros al azar
from tkinter import *        #Para hacer la ventana
from tkinter import colorchooser   #Para importar el selector de color de tkinter


def insertar_coche():
    sg.theme('BlueMono')     
    layout = [
        [sg.Text('Introduce los datos del coche ')],
        [sg.Text('Matricula', size =(15, 1)), sg.InputText()],
        [sg.Text('      Con mayuscula y guiones    EJ: 0000-XXX     XX-0000-XX')],
        [sg.Text('  ')],
        [sg.Text('Marca', size =(15, 1)), sg.InputText()],
        [sg.Text('Modelo', size =(15, 1)), sg.InputText()],
        [sg.Text('Año', size =(15, 1)), sg.InputText()],
        [sg.Submit('Enviar'), sg.Cancel('Cancelar')]
    ]
    window = sg.Window('Introducir datos', layout)
    event, values = window.read()
    window.close()
    matricula = values[0]
    marca = values[1]
    modelo = values[2]
    año = values[3]
    
    con = sqlite3.connect('proyecto.db')
    cur = con.cursor()
    cur.execute("insert into coche values ('{}','{}','{}', '{}')".format(matricula, marca, modelo, año))
    con.commit()
   

def elegir_coche():    
    '''muestra los coches y elegimos uno, devuelve un coche (matricula)'''
    
    listacoches = []
    con = sqlite3.connect('proyecto.db')
    cur = con.cursor()
    cur.execute('select matricula from coche')
    tablas = cur.fetchall()
    for u in tablas:
        listacoches.append(u[0])
    
    layout = [  [sg.Text('Elige tu coche')],
            [sg.Listbox(listacoches, size=(15, len(listacoches)))],
            [sg.Button('Aceptar')]  ]

    window = sg.Window('Pick a color', layout)
    
    while True:                  # the event loop
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Aceptar':
            if values:    # if something is highlighted in the list
                elegido = values[0]
                #print(elegido)
            window.close()
    return elegido
    
    
def registrar_gasto(coche):
    sg.theme('BlueMono')     
    layout = [
        [sg.Text('Introduce los datos del GASTO ')],
        [sg.Text('Fecha', size =(15, 1)), sg.InputText()],
        [sg.Text('Kilometros', size =(15, 1)), sg.InputText()],
        [sg.Text('Concepto', size =(15, 1)), sg.InputText()],
        [sg.Text('Detalle', size =(15, 1)), sg.InputText()],
        [sg.Text('Coste', size =(15, 1)), sg.InputText()],
        [sg.Submit('Enviar'), sg.Cancel('Cancelar')]
    ]
    window = sg.Window('Introducir datos', layout)
    event, values = window.read()
    window.close()
    fecha = values[0]
    kms = values[1]
    concepto = values[2]
    detalle = values[3]
    coste = values[4]
    matricula = coche
    con = sqlite3.connect('proyecto.db')
    cur = con.cursor()
    cur.execute('INSERT into gasto VALUES("{}","{}","{}","{}","{}","{}")'.format(fecha, kms, concepto, detalle, coste, matricula))
    con.commit()
        
                
def imprimir_datos(coche):    
    con = sqlite3.connect('proyecto.db')
    cur = con.cursor()
    cur.execute('select * from coche where matricula="{}"'.format(coche))
    tablas = cur.fetchall()
    for u in tablas:
        listadatos = u
    
    sg.theme('BlueMono')     
    layout = [
    [sg.Text('Datos del coche')],
    [sg.Text('Matricula', size =(15, 1)), sg.Text(listadatos[0])],
    [sg.Text('Marca', size =(15, 1)), sg.Text(listadatos[1])],
    [sg.Text('Modelo', size =(15, 1)), sg.Text(listadatos[2])],
    [sg.Text('Año', size =(15, 1)), sg.Text(listadatos[3])],
    [sg.Text('')],
    [sg.Cancel('Salir')]]
    window = sg.Window('Datos', layout)
    event, values = window.read()
    window.close()
        
        
def crear_diccionario(coche):
    lista=[]
    diccionario={}
    con = sqlite3.connect('proyecto.db')
    cur = con.cursor()
    cur.execute('select fecha, kms, concepto, detalle, coste from gasto where matricula="{}"'.format(coche))
    tablas = cur.fetchall()
    for u in tablas:
        lista.append(u)

    for e in lista:
        if e[2] in diccionario:
             diccionario[e[2]]+=e[4]
        else:
            diccionario[e[2]]=int(e[4])
    return diccionario
    
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
  
  
def definir_colores(listaclaves):
    '''Le pasamos como parametro una lista (obtenida en la funcion mostrar_grafico()) para saber la longitud de la lista a devolver
nos devuelve una lista con tantos colores como claves haya(longitud de la lista de claves)
La lista que nos devuelve la usamos en la funcion de mostrar_grafico()'''
    colores=['aquamarine','azure','beige','blue','brown','chartreuse','chocolate','coral','crimson','cyan','fuchsia','gold','green','grey','ivory','khaki','lavender','lightblue','lightgreen','lime','magenta','maroon','olive','orange','orchid','pink','plum','purple','red','salmon','sienna','silver','tan','teal','turquoise','violet','wheat','yellow','yellowgreen']
    sg.theme('BlueMono')     
    layout = [
    [sg.Text('¿Quieres elegir los colores al azar?')],
    [sg.Button('Si'),sg.Button('No')]]
    window = sg.Window('Colores', layout)
    event, values = window.read()
    window.close()
    if event =='Si':
        desordenados=[]
        for e in listaclaves:
            desordenados.append(colores[random.randint(0, len(colores)-1 )])
        return desordenados
    if event =='No':
        ordenados=[]
        for e in listaclaves:
            root=Tk()
            root.title('Selector de color')
            root.geometry('200x5')
            color=colorchooser.askcolor()
            ordenados.append(str(color[-1]))
            root.destroy()
        return ordenados
         
         
def resumen_gastos(diccionario):
        '''for clave, valor in diccionario.items(): 
            print ("El gasto total en {} es de {} €".format (clave, valor))'''
        sg.theme('BlueMono')     
        layout = [
        [sg.Text('Total gastado en cada categoria')],
        [sg.Text(diccionario)],
        [sg.Cancel('Salir')]]
        window = sg.Window('Datos', layout)
        event, values = window.read()
        window.close()
  
  
def mostrar_gastos(coche):
    lista=[]
    con = sqlite3.connect('proyecto.db')
    cur = con.cursor()
    cur.execute('select fecha, kms, concepto, detalle, coste from gasto where matricula = "{}"'.format(coche))
    tablas = cur.fetchall()
    for u in tablas:
        lista.append(u)
    sg.theme('BlueMono')     
    layout = [
    [sg.Text('Gastos introducidos (Fecha, Kms, Concepto, Detalle, Coste) ')],
    [sg.Text(lista)],
    [sg.Cancel('Salir')]]
    window = sg.Window('Datos', layout)
    event, values = window.read()
    window.close()


#########
    #Parte Grafica
layout = [
    [sg.Button('Elegir coche'),sg.Button('Registrar gasto'),sg.Button('Imprimir coche')],
    [sg.Button('Resumen suma gastos'),sg.Button('Imprimir Grafico'),sg.Button('Registrar coche')],
    [sg.Button('Actualizar'),sg.Button('Todos los gastos'),sg.Button('VACIO')]
    ]

window = sg.Window('Menu').Layout(layout)

while True:             # Event Loop
    event, values = window.Read()
    if event in (None, 'Exit'):
        break
    if event == 'Elegir coche':
        coche=elegir_coche()[0]
        diccionario=crear_diccionario(coche)
    if event == 'Registrar coche':
        insertar_coche()
    if event == 'Imprimir coche':
        try:
            imprimir_datos(coche)
        except NameError:
            sg.theme('BlueMono')     

            layout = [
            [sg.Text('Primero tienes que elegir un coche')],

            [sg.Cancel('Ok')]]
            window = sg.Window('Error', layout)
            event, values = window.read()
            window.close()
    if event == 'Resumen suma gastos':
        resumen_gastos(diccionario)
    if event == 'Imprimir Grafico':
        mostrar_grafico()
    if event == 'Registrar gasto':
        registrar_gasto(coche)
    if event == 'Actualizar':
        diccionario=crear_diccionario(coche)
    if event == 'Todos los gastos':
        mostrar_gastos(coche)
   
window.Close()

