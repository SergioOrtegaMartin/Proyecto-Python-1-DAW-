import matplotlib.pyplot as pyplot

claves=['hola' , 'pepe', 'juan']
slices=[10,20,15]   #Llamamos asi a los valores para mostrarlo en la grafica
colores=['#f34ee7','green','black']
pyplot.pie(slices, colors=colores, labels=claves, autopct='%1.1f%%')  #Con esta linea creamos la grafica
pyplot.axis('equal') #Para hacer redonda la grafica
pyplot.title('Resumen de los gastos')  #Le ponemos titulo a la grafica
#pyplot.legend(labels=claves)  #Ponemos las leyendas de la grafica
pyplot.show()  #Imprimimos la grafica
#pyplot.savefig('Imagen.png')    Por si queremos guardarlo en un fichero de imagen