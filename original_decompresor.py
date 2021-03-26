import os
import argparse
from beautifultable import BeautifulTable
import binascii

aNovo = []
aGrafDef = []
colores = 0
aPalDef = []
aPalMod = []
aGraf = []
lista_graficos = []
lista_paletas = []

def get_size(offset):
    global aGraf 
    counter = 0
    i = 0
    orig = offset

    while True:
        if not (i & 256):
            k = int(aGraf[orig],16) & 255
            orig = orig + 1
            counter = counter + 1
            i = k | 65280

        k2 = int(aGraf[orig],16) & 255

        if (i & 1) == 0:
            orig = orig + 1
            counter = counter + 1
        else:
            if k2 & 128 != 0:
                orig = orig + 1
                counter = counter + 1

                if k2 & 64 !=0:
                    k = k2 & 255
                    k3 = k - 185
                    if k == 255:
                        size = counter
                        break

                    k2 = int(aGraf[orig],16) & 255
                    orig = orig + 1
                    counter = counter + 1
                    
                    k3 = k3 - 1
                    while not k3 < 0:
                        k2 = int(aGraf[orig],16) & 255
                        orig = orig + 1
                        counter = counter + 1
                        k3 = k3 - 1
                    i = i >> 1
                    continue

                j = (k2 & 15) + 1
                k3 =  (k2 >> 4) - 7
            else:
                j = int(aGraf[orig+1], 16) & 255
                orig = orig + 2
                counter = counter + 2
                k3 = (k2 >> 4) + 2
                j = (j | (k2 & 3)) * 256 
            k3 = k3 - 1
            
            while not k3 < 0:
                k3 = k3 - 1
        i = i >> 1
    return size

def visualiza(offset):
    global aNovo
    aNovo = ['00' for i in range(300000)]
    counter = 0
    i = 0
    modif = 2000
    orig = offset
    bits = 4

    while True:
        if (i & 256) == 0 :
            k = int(aGraf[orig],16)
            orig = orig + 1 
            counter = counter + 1
            i = k + 65280
        k2 = int(aGraf[orig], 16)

        if (i & 1) == 0:
            aNovo[modif] = hex(k2)[2:]
            modif =  modif + 1
            orig = orig + 1
            counter = counter + 1
        else:
            if (k2 & 128) != 0:
                orig = orig + 1
                counter = counter + 1
                if k2 & 64 != 0:
                    k = k2
                    k3 = k - 185
                    if k == 255:
                        #termina(id_graf, id_paleta, modif)
                        break
                    
                    for nloop in range(k3, -1, -1):
                        k2 = int(aGraf[orig], 16)
                        orig = orig + 1
                        modif = modif + 1
                        aNovo[modif - 1] =  hex(k2)[2:]
                    
                    counter = counter + k3
                    i = i >> 1
                    continue

                j = (k2 & 15) + 1
                k3 = (k2 >> 4) - 7

            else:
                j = int(aGraf[orig + 1],16)
                orig = orig + 2
                counter = counter + 2
                k3 = (k2 >> 2) + 2
                j = j | (k2 & 3) << 8
            
            for nloop in range(k3, -1, -1):
                tmp = int(aNovo[modif-j], 16)
                aNovo[modif] = hex(tmp)[2:]
                modif = modif + 1
        
        i = i >> 1


def guardar(id_graf, id_paleta):
    global lista_graficos
    global lista_paletas
    global colores
    global aGraf
    global aNovo

    palx = int(lista_paletas[id_paleta][3])
    paly = int(lista_paletas[id_paleta][4])
    vramx = int(lista_graficos[id_graf][3])
    vramy = int(lista_graficos[id_graf][4])

    respuesta = []

    pospal = hex(palx)[2:].zfill(4)
    pospal2 = pospal[2:] + pospal[:2]
    pospal = hex(paly)[2:].zfill(4)
    pospal2 = pospal2 + pospal[2:] + pospal[:2]


    alt = lista_graficos[id_graf][6]
    larg = lista_graficos[id_graf][5]
    offpal = lista_paletas[id_paleta][1]
    
    if colores == 16:
        larg = larg * 2
    
    col = 0
    lin = 0

    if colores == 16:
        cabezaTIM = '10000000080000002C000000'+ pospal2 +'10000100'
        cabeza2TIM = hex((alt * larg) + 12)[2:].zfill(4)
        cabeza2TIM = cabeza2TIM[2:] + cabeza2TIM[:2]+ '0000'

        tmpstr = hex(vramx)[2:].zfill(4)
        tmpstr2 = tmpstr[2:] + tmpstr[:2]
        cabeza2TIM= cabeza2TIM+tmpstr2

        tmpstr = hex(vramy)[2:].zfill(4)
        tmpstr2 = tmpstr[2:] + tmpstr[:2]
        cabeza2TIM= cabeza2TIM+tmpstr2

        tmpstr = hex(larg//4)[2:].zfill(4)
        tmpstr2 = tmpstr[2:] + tmpstr[:2]
        cabeza2TIM= cabeza2TIM+tmpstr2

        tmpstr = hex(alt)[2:].zfill(4)
        tmpstr2 = tmpstr[2:] + tmpstr[:2]
        cabeza2TIM= cabeza2TIM+tmpstr2
    else:
        cabezaTIM = '10000000090000000C020000'+ pospal2 +'00010100'
        cabeza2TIM = hex((alt * larg) + 12)[2:].zfill(4)
        cabeza2TIM = cabeza2TIM[2:] + cabeza2TIM[:2]+ '0000'
        
        tmpstr = hex(vramx)[2:].zfill(4)
        tmpstr2 = tmpstr[2:] + tmpstr[:2]
        cabeza2TIM= cabeza2TIM+tmpstr2

        tmpstr = hex(vramy)[2:].zfill(4)      
        tmpstr2 = tmpstr[2:] + tmpstr[:2]
        cabeza2TIM= cabeza2TIM+tmpstr2

        tmpstr = hex(larg//2)[2:].zfill(4)
        tmpstr2 = tmpstr[2:] + tmpstr[:2]
        cabeza2TIM= cabeza2TIM+tmpstr2

        tmpstr = hex(alt)[2:].zfill(4)
        tmpstr2 = tmpstr[2:] + tmpstr[:2]
        cabeza2TIM= cabeza2TIM+tmpstr2
    
    
    archivo = open(str(id_graf)+'-'+str(id_paleta)+'.tim', 'wb')

    mm=0
    while mm<len(cabezaTIM) or mm==len(cabezaTIM):
        dato = cabezaTIM[mm:mm+2]
        respuesta.append(dato)
        mm = mm + 2

    posicion = int(offpal) 
    mm = 0
    while mm < (colores * 2):
        respuesta.append(aGraf[posicion])
        mm = mm + 1
        posicion = posicion + 1
    
    mm=0

    while mm<len(cabeza2TIM) or mm==len(cabeza2TIM):
        dato =cabeza2TIM[mm:mm+2]
        respuesta.append(dato)
        mm = mm + 2

    mm = 0
    largo2 =larg
    if colores == 16:
        largo2=larg // 2

    for i in range((alt*largo2)):
        respuesta.append(aNovo[2000+i])


    for dato in respuesta:
        if len(dato)==1:
            dato = '0' + str(dato)
        archivo.write(binascii.a2b_hex(dato))
    archivo.close()





#leer el archivo
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True,
	help="path to file")

args = vars(ap.parse_args())

ArChivo= open(args['file'], 'rb')
x = os.path.getsize(args['file'])

ArChivo.seek(0,0)

aBuffer = ArChivo.read()
aGraf = ['00' for i in range(x)]

for b in range(x):
    h = aBuffer[b]
    he = hex(h)[2:].upper().zfill(2)
    aGraf[b] = he

ArChivo.close()

table = BeautifulTable()
table.columns.header = ["ID","Offset Decimal", "Offset Hexadecimal", "VRAM X",
                        "VRAM Y","Width", "Heigth", "Size"]
id_tabla = 0
for b in range(x-16):
    if (
            (aGraf[b]=='0A') and (aGraf[b+1]=='00') and \
            (aGraf[b+10]=='00') and (aGraf[b+11] == '00') and \
            (aGraf[b+15]=='80') and ((aGraf[b+14]=='10') or \
            (aGraf[b+14]=='11') or (aGraf[b+14]=='12') or \
            (aGraf[b+14]=='0C') or (aGraf[b+14]=='0D') or \
            (aGraf[b+14]=='0E') or (aGraf[b+14]=='0F')or \
            (aGraf[b+14]=='08'))
        ):
            offset = 0
            if aGraf[b+14] == '08':  
                offset = int(aGraf[b+13] + aGraf[b+12],16) + 5320
            elif aGraf[b+14] == '0C': 
                offset = int(aGraf[b+13] + aGraf[b+12],16) - 32768
            elif aGraf[b+14] == '0D': 
                offset = int(aGraf[b+13] + aGraf[b+12],16) + 32768
            elif aGraf[b+14] == '0E': 
                offset = int(aGraf[b+13] + aGraf[b+12],16) + 98304
            elif aGraf[b+14] == '0F': 
                offset = int(aGraf[b+13] + aGraf[b+12],16)
            elif aGraf[b+14] == '10': 
                offset = int('1' + aGraf[b+13] + aGraf[b+12],16)
            elif aGraf[b+14] == '11': 
                offset = int('2' + aGraf[b+13] + aGraf[b+12],16)
            elif aGraf[b+14] == '12': 
                offset = int('3' + aGraf[b+13] + aGraf[b+12],16)

            lista_graficos.append([
                                id_tabla,           
                                offset, 
                                str(hex(offset))[2:].zfill(4), 
                                int('0x'+aGraf[b+3] + aGraf[b+2],16), 
                                int('0x'+aGraf[b+5] + aGraf[b+4],16), 
                                int('0x'+aGraf[b+7],16) + int('0x'+aGraf[b+6],16)*2, 
                                int('0x'+aGraf[b+9],16) + int('0x'+aGraf[b+8],16),
                                get_size(offset)])
            
            id_tabla = id_tabla + 1


for i in lista_graficos:
    table.rows.append(i)

print(table)
print()

offset_graf = offset

#Colores
table = BeautifulTable()
table.columns.header = ["ID","Offset Decimal", "Offset Hexadecimal", 
                    "VRAM X", "VRAM Y","Width", "Heigth", "Size","Colors"]

lista_offset= []
lista_tabla_pal = []
id_tabla = 0
for b in range(x-15):
    if (
        (aGraf[b] =='09') and
        (aGraf[b+10] =='00') and (aGraf[b+11] =='00') and
        (aGraf[b+15]=='80') and ((aGraf[b+14]=='10') or
        (aGraf[b+14]=='11') or (aGraf[b+14]=='12') or
        (aGraf[b+14]=='0C') or (aGraf[b+14]=='0D') or
        (aGraf[b+14]=='0E') or (aGraf[b+14]=='0F') or
        (aGraf[b+14]=='08'))
    ):
        offset = 0
        if aGraf[b+14] == '08':  
            offset = int(aGraf[b+13] + aGraf[b+12],16) + 5352
        elif aGraf[b+14] == '0C': 
            offset = int(aGraf[b+13] + aGraf[b+12],16) - 32768
        elif aGraf[b+14] == '0D': 
            offset = int(aGraf[b+13] + aGraf[b+12],16) + 32768
        elif aGraf[b+14] == '0E': 
            offset = int(aGraf[b+13] + aGraf[b+12],16) + 98304
        elif aGraf[b+14] == '0F': 
            offset = int(aGraf[b+13] + aGraf[b+12],16)
        elif aGraf[b+14] == '10': 
            offset = int('1' + aGraf[b+13] + aGraf[b+12],16)
        elif aGraf[b+14] == '11': 
            offset = int('2' + aGraf[b+13] + aGraf[b+12],16)
        elif aGraf[b+14] == '12': 
            offset = int('3' + aGraf[b+13] + aGraf[b+12],16)

        lista_paletas.append([id_tabla,
                            offset, 
                            str(hex(offset))[2:].zfill(4), 
                            int(aGraf[b+3] + aGraf[b+2],16), 
                            int(aGraf[b+5] + aGraf[b+4],16), 
                            int(aGraf[b+7] + aGraf[b+6],16)*2, 
                            int(aGraf[b+9],16) + int(aGraf[b+8],16),
                            0,0])
        lista_tabla_pal.append(offset)
        lista_offset.append(offset)
        id_tabla = id_tabla + 1
    

    if (
        (aGraf[b]=='0A') and (aGraf[b+1]=='00') and \
        (aGraf[b+10]=='00') and (aGraf[b+11] == '00') and \
        (aGraf[b+15]=='80') and ((aGraf[b+14]=='10') or \
        (aGraf[b+14]=='11') or (aGraf[b+14]=='12') or \
        (aGraf[b+14]=='0C') or (aGraf[b+14]=='0D') or \
        (aGraf[b+14]=='0E') or (aGraf[b+14]=='0F')or \
        (aGraf[b+14]=='08'))
    ):
        if aGraf[b+14] == '08':  
            offset = int(aGraf[b+13] + aGraf[b+12],16) + 5320
        elif aGraf[b+14] == '0C': 
            offset = int(aGraf[b+13] + aGraf[b+12],16) - 32768
        elif aGraf[b+14] == '0D': 
            offset = int(aGraf[b+13] + aGraf[b+12],16) + 32768
        elif aGraf[b+14] == '0E': 
            offset = int(aGraf[b+13] + aGraf[b+12],16) + 98304
        elif aGraf[b+14] == '0F': 
            offset = int(aGraf[b+13] + aGraf[b+12],16)
        elif aGraf[b+14] == '10': 
            offset = int('1' + aGraf[b+13] + aGraf[b+12],16)
        elif aGraf[b+14] == '11': 
            offset = int('2' + aGraf[b+13] + aGraf[b+12],16)
        elif aGraf[b+14] == '12': 
            offset = int('3' + aGraf[b+13] + aGraf[b+12],16)
        
        lista_offset.append(offset)

npos = 0
#Acordarme de arreglar este pedo
for b in range(-1,3):
    for c in range(len(lista_offset)):
        if lista_offset[c] == lista_tabla_pal[b + 1]:
            npos=c
    valor = lista_tabla_pal[b+2]
    tempor = lista_offset[npos+1] - lista_offset[npos]
    lista_paletas[b+1][7] = tempor
    lista_paletas[b+1][8] = tempor // 2

    if (
        ((aGraf[valor-32]=='0A') and (aGraf[valor-31]=='00') and
        (aGraf[valor-23]=='00') and (aGraf[valor-22] =='00') and
        (aGraf[valor-17]=='80') and ((aGraf[valor-18]=='10') or
        (aGraf[valor-18]=='11') or (aGraf[valor-18]=='12') or
        (aGraf[valor-18]=='0C') or (aGraf[valor-18]=='0D') or
        (aGraf[valor-18]=='0E') or (aGraf[valor-18]=='0F')or
        (aGraf[valor-18]=='08'))) or
        ((aGraf[valor-32]=='09') and
        (aGraf[valor-23]=='00') and (aGraf[valor-22] =='00') and
        (aGraf[valor-17]=='80') and ((aGraf[valor-18]=='10') or
        (aGraf[valor-18]=='11') or (aGraf[valor-18]=='12') or
        (aGraf[valor-18]=='0C') or (aGraf[valor-18]=='0D') or
        (aGraf[valor-18]=='0E') or (aGraf[valor-18]=='0F') or
        (aGraf[valor-18]=='08')))
        ):
        tempor = lista_offset[npos + 1] - lista_offset[npos] - 32
        lista_paletas[b+1][7] = tempor
        lista_paletas[b+1][8] = tempor // 2
    
    busca = lista_tabla_pal[-1] 

    #PELIGRO
    busca = busca + 1
    while not (
            ((aGraf[busca]=='0A') and (aGraf[busca+1]=='00') and \
            (aGraf[busca+10]=='00') and (aGraf[busca+11] == '00') and \
            (aGraf[busca+15]=='80') and ((aGraf[busca+14]=='10') or \
            (aGraf[busca+14]=='11') or (aGraf[busca+14]=='12') or \
            (aGraf[busca+14]=='0C') or (aGraf[busca+14]=='0D') or \
            (aGraf[busca+14]=='0E') or (aGraf[busca+14]=='0F')or \
            (aGraf[busca+14]=='08'))) 
            or 
            (aGraf[busca] =='09') and
            (aGraf[busca+10] =='00') and (aGraf[busca+11] =='00') and
            (aGraf[busca+15]=='80') and ((aGraf[busca+14]=='10') or
            (aGraf[busca+14]=='11') or (aGraf[busca+14]=='12') or
            (aGraf[busca+14]=='0C') or (aGraf[busca+14]=='0D') or
            (aGraf[busca+14]=='0E') or (aGraf[busca+14]=='0F') or
            (aGraf[busca+14]=='08'))
        ): 
            busca = busca + 1

    tempor = busca - lista_tabla_pal[-1]
    lista_paletas[-1][7] = tempor
    lista_paletas[-1][8] = tempor // 2

    if lista_paletas[1][8] == 16:
        colores = 16
    else:
        colores = 256

for i in lista_paletas:
    table.rows.append(i)

print(table)

#Local Numeros jugador y portero
visualiza(lista_graficos[0][1])
guardar(0, 0)
guardar(0, 1)

#Mangas Local
visualiza(lista_graficos[1][1])
guardar(1, 0)

#Visitante Numeros jugador y portero
visualiza(lista_graficos[2][1])
guardar(2, 2)
guardar(2, 3)

#Mangas Visitante
visualiza(lista_graficos[3][1])
guardar(3, 2)

#bandera
visualiza(lista_graficos[4][1])
guardar(4, 4)