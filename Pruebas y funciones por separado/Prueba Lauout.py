import PySimpleGUI as sg  #Interface gráfica

lista=[]
diccionario={'Reparacion': 50, 'Extra': 500, 'Mantenimiento': 100}
for clave, valor in diccionario.items(): 
    lista.append("{}  ➠  {} €       ".format (clave, valor))
cadena= "".join(lista)
sg.theme('BlueMono')     
layout = [
[sg.Text('pepe')],
[sg.Text('Total gastado en cada categoria')],
[sg.Text(cadena)],
[sg.Cancel('Salir')]]
window = sg.Window('Datos', layout)
event, values = window.read()
window.close()
