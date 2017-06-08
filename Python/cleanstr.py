# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 14:19:54 2017

@author: rrezzano
"""

def cleanstr(filtro):
    import re
    # En primer lugar debemos de abrir el fichero que vamos a leer.
    # Usa 'rb' en vez de 'r' si se trata de un fichero binario.
    infile = open('AguadaOficialTweetText.txt', 'r')
    outfile = open('AguadaOficialTweetTextClean.txt', 'w') # Indicamos el valor 'w'.
    outfile2 = open('AguadaOficialTweetTextBasura.txt', 'w') # Indicamos el valor 'w'.
    
    # Mostramos por pantalla y escribe en un fichero lo que leemos desde el fichero y filtramos
    print('>>> Lectura del fichero línea a línea')
    for line in infile:
    #    print(line)
        palabras = line.split()
        for n in palabras:
            if re.match('@.+', n):
                outfile2.write(n + "\n")
            elif re.match('[' + filtro+ ']', n):
                outfile2.writelines(n + "\n")
            else:
                outfile.writelines(n + "\n")
    #    if re.match('(@.+)',line):
    #        cleanline= line
    #        print(line)
    #        outfile.write(cleanline)
    #    if re.search('^@', line):
    #        cleanline2=line
    #        print(cleanline2)
    #        outfile2.write(cleanline)
    # Cerramos el fichero.
    outfile.close()
    outfile2.close()
    infile.close()
    print('>>> Termina proceso con exito')

cleanstr('-+|!😂')


