##### IMPORTACION DE LIBRERIAS
import sqlite3   #Trabajar con bases de datos
import PySimpleGUI as sg  #Interface gráfica
import os   #Para listar los ficheros de un directorio
import matplotlib.pyplot as pyplot    #Para hacer el gráfico
import random  #Para obtener numeros al azar
from tkinter import *        #Para hacer la ventana
from tkinter import colorchooser   #Para importar el selector de color de tkinter

#### COMENTARIOS Y CORRECCIONES
'''Poner en todo momento el coche sobre el que se está trabajando
tratar errores y excepciones
poner mejor imprimir datos
primero pregunta que coche quieres elegir o si deseas crear un coche nuevo
despues trabajas sobre el coche elegido (mostrandolo en todos los menus)
y si creas un coche nuevo vas a trabjar directamente con ese coche
'''
'''corregir ejecución del programa (hacer funciones para parte grafica1 y 2)
En el menu poner un boton que sea ir atrás que vuelva al selector de coche
cuando registro un nuevo gasto en el coche, que automaticamente me lo meta en la BD(funcion actualizar)'''

##### FUNCIONES COMPORTAMIENTO DEL PROGRAMA
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
    if len(values[0]) != 0:
        matricula = values[0]
        marca = values[1]
        modelo = values[2]
        año = values[3]
        con = sqlite3.connect('proyecto.db')
        cur = con.cursor()
        cur.execute("insert into coche values ('{}','{}','{}', '{}')".format(matricula, marca, modelo, año))
        con.commit()
    else:
        sg.theme('BlueMono')     
        layout = [
        [sg.Text('No has rellenado todos los campos')],
        [sg.Text('¿Volver a rellenar?')],
        [sg.Button('Si'),sg.Button('No')]]
        window = sg.Window('Colores', layout)
        event, values = window.read()
        if event == 'Si':
            insertar_coche()
        if event == 'No':
            pass
        window.close()

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
            [sg.Button('Aceptar'),sg.Button('Insertar nuevo coche')]  ]

    window = sg.Window('Elegir', layout)


    event, values = window.read()
    if event == 'Insertar nuevo coche':
        window.close()
        insertar_coche()
        elegir_coche()
    if event == 'Aceptar':
        if values:    # Si hay algo seleccionado en la lista
            elegido = values[0]
        window.close()
        return elegido

def registrar_gasto(coche):
    sg.theme('BlueMono')     
    layout = [
        [sg.Text('Introduce los datos del gasto del coche con matricula: {} '.format(coche))],
        [sg.Text('Fecha', size =(15, 1)), sg.InputText()],
        [sg.Text('Kilometros', size =(15, 1)), sg.InputText()],
        [sg.Text('Concepto', size =(15, 1)), sg.InputText()],
        [sg.Text('Detalle', size =(15, 1)), sg.InputText()],
        [sg.Text('Coste', size =(15, 1)), sg.InputText()],
        [sg.Button('Enviar'), sg.Button('Cancelar')]
    ]
    window = sg.Window('Introducir datos', layout)
    event, values = window.read()
    window.close()
    if event == 'Cancelar':
        pass
    if len(values[0]) != 0:
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
    else:
        sg.theme('BlueMono')     
        layout = [
        [sg.Text('No has rellenado todos los datos')],
        [sg.Text('¿Volver a rellenar?')],
        [sg.Button('Si'),sg.Button('No')]]
        window = sg.Window('Colores', layout)
        event, values = window.read()
        if event == 'Si':
            registrar_gasto(coche)
        if event == 'No':
            pass
        window.close()

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

def mostrar_grafico(coche):
    '''Obtiene las claves del diccionario, los slices son los valores de cada clave y los colores los obtiene de la funcion
definir_colores()'''

    if len(diccionario.keys()) != 0:
        claves=list(diccionario.keys())
        slices=list(diccionario.values())   #Llamamos asi a los valores para mostrarlo en la grafica
        colores=definir_colores(claves)
        pyplot.pie(slices, colors=colores, labels=claves, autopct='%1.1f%%')  #Con esta linea creamos la grafica
        pyplot.axis('equal') #Para hacer redonda la grafica
        pyplot.title('Resumen de los gastos del coche con matricula   {} '.format(coche))  #Le ponemos titulo a la grafica
        
        #pyplot.legend(labels=claves)  #Ponemos las leyendas de la grafica
        pyplot.show()  #Imprimimos la grafica
        #pyplot.savefig('Imagen.png')    Por si queremos guardarlo en un fichero de imagen
    else:
        sg.theme('BlueMono')     
        layout = [
        [sg.Text('Todavia no hay ningun gasto introducido')],
        [sg.Text('¿Quieres introducir algun gasto?')],
        [sg.Button('Si'),sg.Button('No')]]
        window = sg.Window('Colores', layout)
        event, values = window.read()
        if event == 'Si':
            registrar_gasto(coche)
        if event == 'No':
            pass
        window.close()

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
        lista=[]
        for clave, valor in diccionario.items(): 
            lista.append("{}  ➠  {} €       ".format (clave, valor))
        cadena= "".join(lista)
        sg.theme('BlueMono')     
        layout = [
        [sg.Text(coche)],
        [sg.Text('Total gastado en cada categoria')],
        [sg.Text(cadena)],
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

def eliminar_coche(coche):
    sg.theme('BlueMono')     
    layout = [
    [sg.Text('Vas a borrar este coche y todos sus datos registrados')],
    [sg.Text('¿Continuar?')],
    [sg.Button('Si'),sg.Button('No')]]
    window = sg.Window('Colores', layout)
    event, values = window.read()
    if event == 'Si':
        con = sqlite3.connect('proyecto.db')
        cur = con.cursor()
        cur.execute('delete from gasto where matricula = "{}"'.format(coche))
        cur.execute('delete from coche where matricula = "{}"'.format(coche))
        con.commit()
        eliminado = True
        window.close()
        return eliminado
    if event == 'No':
        pass
    window.close()
    

########  FUNCIONES PARTE GRAFICA
def graficos_1():
    try:
        coche = elegir_coche()[0]
        return coche
    except IndexError:
        pass
        '''sg.theme('BlueMono')     
        layout = [
        [sg.Text('No has seleccionado ningun coche')],
        [sg.Button('Seleccionar coche')]]
        window = sg.Window('Colores', layout)
        event, values = window.read()
        if event == 'Seleccionar coche':
            window.close()
            coche = elegir_coche()[0]
            return coche'''
def global_diccionario(coche):    
    try:
        diccionario=crear_diccionario(coche)
        return diccionario
    except ValueError:
        pass
def graficos_2(diccionario, coche): 
    layout = [
        [sg.Text('', size =(15, 1)), sg.Text(coche)],
        [sg.Button('Imprimir Grafico'),sg.Button('Imprimir datos coche')],
        [sg.Button('Registrar nuevo gasto'),sg.Button('Resumen suma gastos')],
        [sg.Button('Elegir otro coche'),sg.Button('Eliminar coche'),sg.Button('Salir')]
        ]

    window = sg.Window('Menu').Layout(layout)

    while True:              #Llamada a las funciones
        event, values = window.Read()
        if event in (None, 'Salir'):
            break
        if event == 'Elegir otro coche':
            window.close()
            coche=graficos_1()
            diccionario=global_diccionario(coche)
            graficos_2(diccionario, coche)
        if event == 'Imprimir datos coche':
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
            mostrar_grafico(coche)
        if event == 'Registrar nuevo gasto':
            registrar_gasto(coche)
            #diccionario=global_diccionario(coche)
        if event == 'Actualizar':
            try:
                diccionario=crear_diccionario(coche)
            except ValueError:
                print ('Ha habido un error con la base de datos')
        if event == 'Todos los gastos':
            mostrar_gastos(coche)
        if event == 'Eliminar coche':
            eliminado = eliminar_coche(coche)
            if eliminado:
                window.close()
                coche=graficos_1()
                diccionario=global_diccionario(coche)
                graficos_2(diccionario, coche)
                
       
    window.Close()

#######  LLAMADA A LAS FUNCIONES
coche=graficos_1()
diccionario = global_diccionario(coche)
graficos_2(diccionario, coche)

