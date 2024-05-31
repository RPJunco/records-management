from module_p2 import *
from datetime import datetime
import pickle
import os.path


# ----------------------------------------------------------------------------------------------------------------------

def menu():
    print('\nMENU DE OPCIONES: '
          '\n-Opcion 1:  Cargar el contenido del archivo en un vector de registros de proyectos.'
          '\n\n-Opcion 2: Mostrar todos aquellos registros que contengan al tag que usted ingrese por teclado en alguno '
          'de los elementos del vector alojado en el campo tag. \n\t * repositorio.'
          ' \n\t * la fecha de actualización. \n\t * cantidad de estrellas.'
          '\n\n-Opcion 3: Determinar y mostrar la cantidad de proyectos por cada lenguaje de programación ordenados de mayor a menor por cantidad. '
          '\n\n-Opcion 4: Generar una matriz con los meses en los que se actualizan los proyectos, de acuerdo a la cantidad de '
          'estrellas. \nCada celda contendra la cantidad de proyectos que tengan ese mes de actualización y esa cantidad de estrellas. '
          '\n\n-Opcion 5: Buscar un repositorio, si existe mostrar sus datos y permitir reemplazar la URL del proyecto y '
          'cambiar la fecha de actualización \npor la fecha actual.'
          '\n\n-Opcion 6:  A partir de la matriz generada en el punto 4, almacenar su contenido '
          '(sólo los elementos mayores a cero) en un archivo binario en el que \ncada elemento sea un registro en el que '
          'se representen los campos: \n| Mes del año | Estrellas (rango indicado en el punto 2) | Cantidad de proyectos |'
          '\n\n-Opcion 7: Leer el contenido del archivo binario y volver a generar la matriz. Mostrarla en formato de tabla.'
          '\n\n-Opcion 8: Finaliza la ejecución del programa.\n')


# ----------------------------------------------------------------------------------------------------------------------
# Validaciones

def validar_text_cargado(mensaje):
    text = input(mensaje)
    while len(text) == 0:
        text = input('¡¡ERROR!! Este campo no puede estar vacio: ')
    return text


def validate_range_mes(inf, sup, mensaje):
    num = int(input(mensaje))
    while num < inf or num > sup:
        num = int(input('¡¡ERRORR!! Debe ingresar un mes en el rango [' + str(inf) + ';' + str(sup) + ']:'))
    return num


# ----------------------------------------------------------------------------------------------------------------------
# Opcion 1


def agregar_registro_ordenado(reg, vector):
    n = len(vector)
    ingreso = False
    izq, der = 0, n - 1
    while izq <= der:
        c = (izq + der) // 2
        if vector[c].repositorio == reg.repositorio:
            ingreso = False
            break

        if vector[c].repositorio > reg.repositorio:
            der = c - 1
        else:
            izq = c + 1

    if izq > der:
        pos = izq
        vector[pos:pos] = [reg]
        ingreso = True

    return ingreso


def cargar_datos_en_arreglo_proyectos(linea, cont_proy_om):
    reg = None

    campos_reg = linea.split('|')
    nom = campos_reg[0]
    rep = campos_reg[1]
    fecha_act = campos_reg[3]
    leng = campos_reg[4]

    # Ingresamos los likes como valor en coma flotante.
    likes_car = campos_reg[5]
    likes = float(likes_car[:-1])

    # Ingresamos los tags como vector de cadena de caracteres.
    tags = campos_reg[6]
    if tags == '':
        tags = 'No tiene'
    else:
        tags = tags.split(',')

    url = campos_reg[7]

    if leng != '':
        reg = Proyecto(nom, rep, fecha_act, leng, likes, tags, url)
    else:
        cont_proy_om += 1
    return reg, cont_proy_om


def mostrar_arreglo_de_proyectos(proyectos):
    print('Listado de proyectos cargados: \n')
    for i in range(len(proyectos)):
        print(proyectos[i])
        print()


# ----------------------------------------------------------------------------------------------------------------------
# Opcion 2

# -La siguiente funcion tambien es utilizada para la opcion 4-
def calcular_cantidad_de_estrellas(likes):
    estrella = 0
    if likes < 10.1:
        estrella = 1
    if likes >= 10.1 and likes <= 20:
        estrella = 2
    if likes >= 20.1 and likes <= 30:
        estrella = 3
    if likes >= 30.1 and likes <= 40:
        estrella = 4
    if likes > 40:
        estrella = 5
    return estrella


def validate_respuesta_s_o_n(mensaje):
    respuesta = input(mensaje).lower()
    while len(respuesta) == 0 or (respuesta[0] != 's' and respuesta[0] != 'n'):
        print('¡¡¡Error!!!')
        respuesta = input('Debe ingresar una letra "S", "s" o "N", "n": ').lower()
    return respuesta


def mostrar_datos_del_archivo_cargado(arc_text):
    file = open(arc_text, 'rt')
    for line in file:
        print(line)
    file.close()


def cargar_archivo_del_listado_generado(arc_tag, vec_reg_tags):
    archivo = open(arc_tag, 'wt')
    nom_campos = '|nombre_usuario|repositorio|fecha_actualizacion|lenguaje|estrellas|tags|url|'
    archivo.write(nom_campos + '\n')
    for i in range(len(vec_reg_tags)):
        campo_1 = 'Nombre_usuario: ' + str(vec_reg_tags[i].nombre_usuario)
        campo_2 = 'Repositorio: ' + str(vec_reg_tags[i].repositorio)
        campo_3 = 'Fecha_actualizacion: ' + str(vec_reg_tags[i].fecha_actualizacion)
        campo_4 = 'Lenguaje: ' + str(vec_reg_tags[i].lenguaje)
        campo_5 = 'Likes: ' + str(vec_reg_tags[i].likes) + 'k'
        campo_6 = 'Tags: ' + str(vec_reg_tags[i].tags)
        campo_7 = 'Url: ' + str(vec_reg_tags[i].url)
        archivo.write('|' + campo_1 + '|' + campo_2 + '|' + campo_3 + '|' + campo_4 + '|' + campo_5 + '|' + campo_6
                      + '|' + campo_7 + '' + '|' + '\n')
    archivo.close()


# ----------------------------------------------------------------------------------------------------------------------
# Opcion 3


def agregar_por_lenguajes(proy, vector):
    n = len(vector)
    izq, der = 0, n - 1
    while izq <= der:
        c = (izq + der) // 2
        if vector[c].lenguaje == proy.lenguaje:
            break

        if vector[c].lenguaje > proy.lenguaje:
            der = c - 1
        else:
            izq = c + 1

    if izq > der:
        pos = izq
        vector[pos:pos] = [proy]


def cargar_vector_lenguajes(proyectos):
    vec_a_cargar = []
    vec_leng = []

    for i in range(len(proyectos)):
        if proyectos[i].lenguaje != '':
            agregar_por_lenguajes(proyectos[i], vec_a_cargar)

    for j in range(len(vec_a_cargar)):
        vec_leng.append(vec_a_cargar[j].lenguaje)

    return vec_leng


def determinar_cant_proy_por_leng(v_proy):
    vec_lenguaje = cargar_vector_lenguajes(v_proy)

    vec_cont_por_leng = [0] * len(vec_lenguaje)

    for c in range(len(vec_lenguaje)):
        for j in range(len(v_proy)):
            if vec_lenguaje[c] == v_proy[j].lenguaje:
                vec_cont_por_leng[c] += 1

    return vec_cont_por_leng, vec_lenguaje


def ordenar_vec_cont_por_cant(cont, leng):
    n = len(cont)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if cont[i] < cont[j]:
                cont[i], cont[j] = cont[j], cont[i]
                leng[i], leng[j] = leng[j], leng[i]


def mostrar_cant_proy_por_lenguajes(v_cont, leng):
    ordenar_vec_cont_por_cant(v_cont, leng)
    for i in range(len(v_cont)):
        print('| El lenguaje: ' + str(leng[i]) + ' tiene una cantidad de: ' + str(v_cont[i]) + ' proyectos |')


# ----------------------------------------------------------------------------------------------------------------------
# Opcion 4


def devolver_a_cero_la_matriz(mat):
    for f in range(len(mat)):
        for c in range(len(mat[f])):
            mat[f][c] = 0


def mostrar_total_proy_actualizados_mes(cons_mes, mat):
    acum_proyectos = 0
    for f in range(len(mat)):
        if f + 1 == cons_mes:
            for c in range(len(mat[f])):
                acum_proyectos += mat[f][c]

    print('=' * 80)
    print('| El mes ' + str(cons_mes) + ' tuvo un total de ' + str(acum_proyectos) + ' proyectos acumulados |')
    print('=' * 80)


# ----------------------------------------------------------------------------------------------------------------------
# Opcion 5


def busqueda_binaria(vec_proy, repo):
    n = len(vec_proy)
    izq, der = 0, n - 1
    c = 0
    while izq <= der:
        c = (der + izq) // 2
        if vec_proy[c].repositorio == repo:
            return 1, c
        elif vec_proy[c].repositorio > repo:
            der = c - 1
        elif vec_proy[c].repositorio < repo:
            izq = c + 1

    return -1, c


def actualizar_fecha(now):
    if now.month < 10:
        mes = '0' + str(now.month)
    else:
        mes = str(now.month)

    if now.day < 10:
        dia = '0' + str(now.day)
    else:
        dia = str(now.day)

    actualizacion = str(now.year) + '-' + mes + '-' + dia

    return actualizacion


# ----------------------------------------------------------------------------------------------------------------------
# Opciones


def opcion_1(vec_proy, pasadas, omitidos):
    if pasadas == 0:
        cont_proy_om = 0
        m = open("proyectos.csv", mode="rt", encoding="utf8")
        lineas_car = m.readlines()
        lineas_car = lineas_car[1:]
        for line in lineas_car:
            line = line[:-1]
            reg, cont_proy_om = cargar_datos_en_arreglo_proyectos(line, cont_proy_om)
            if reg is not None:
                contar = agregar_registro_ordenado(reg, vec_proy)
                if not contar:
                    cont_proy_om += 1
        m.close()
        return cont_proy_om
    else:
        return omitidos


def opcion_2(v_proy, tag, arc_tag):
    existe = False
    vec_reg_tags = []
    print('-' * 80)
    for i in range(len(v_proy)):
        vec_tags = v_proy[i].tags
        for j in range(len(vec_tags)):
            if v_proy[i].tags[j] == tag:
                estrellas = calcular_cantidad_de_estrellas(v_proy[i].likes)
                print('Repositorio: ' + str(v_proy[i].repositorio + ' ---  Fecha de actualizacion: '
                                            + str(
                    v_proy[i].fecha_actualizacion) + ' --  Cantidad de estrellas(likes): ' + str(estrellas)))
                vec_reg_tags.append(v_proy[i])
                existe = True
    print('-' * 80)
    if existe:
        respuesta = validate_respuesta_s_o_n('Ingresar el listado generado anteriormente en un archivo de texto("S"(si) o "N"(no)): ')

        if respuesta == 's':
            print('~' * 80)
            print('La respuesta fue afirmativa..\nGenerando archivo del listado de tags obtenido: ')
            print()

            cargar_archivo_del_listado_generado(arc_tag, vec_reg_tags)

            mostrar_datos_del_archivo_cargado(arc_tag)
            print('~' * 80)
        else:
            print('~' * 80)
            print('La respuesta fue negativa...\nVolviendo al menu de opciones.')
            print('~' * 80)
    else:
        print('No se encontro el tag ' + '"' + str(tag) + '"' + ' entre los proyectos..')
        print('-' * 80)


def opcion_3(vec_proy):
    cant_proy_por_leng, lenguajes = determinar_cant_proy_por_leng(vec_proy)

    print('-' * 80)
    mostrar_cant_proy_por_lenguajes(cant_proy_por_leng, lenguajes)
    print('-' * 80)


def opcion_4(vec_proy, cons_mes, mat):
    devolver_a_cero_la_matriz(mat)
    est = "1  2  3  4  5"
    for i in range(len(vec_proy)):
        estrella = calcular_cantidad_de_estrellas(vec_proy[i].likes)
        mes_car = vec_proy[i].fecha_actualizacion[5:7]
        mes = int(mes_car)
        mat[mes - 1][estrella - 1] += 1

    print('\t\tEstrellas')
    print('\t  ', est)
    for f in range(len(mat)):
        print('Mes', f + 1, mat[f], '\n')

    mostrar_total_proy_actualizados_mes(cons_mes, mat)

    return mat


def opcion_5(vec_proy, repositorio, now):
    busqueda, posicion = busqueda_binaria(vec_proy, repositorio)
    if busqueda == 1:
        print('\nRepositorio encontrado..\nRegistro correspondiente: \n')
        print(vec_proy[posicion])
        nueva_url = input('Ingrese la url actualizada del proyecto: ')
        nueva_fecha = actualizar_fecha(now)
        vec_proy[posicion].url = nueva_url
        vec_proy[posicion].fecha_actualizacion = nueva_fecha
        print('\nRegistro actualizado: \n')
        print(vec_proy[posicion])

    else:
        print('¡¡ERROR!! El repositorio ' + str(repositorio) + ' no fue encontrado..')


def opcion_6(mat, ingreso):
    if not ingreso:
        print('=' * 80)
        print('No hay datos cargados en la matriz.. Debe pasar por el punto 4.')
        print('=' * 80)
        return

    cargado = False
    file_mat = 'matriz.dat'
    archivo = open(file_mat, 'wb')
    for f in range(len(mat)):
        for c in range(len(mat[f])):
            if mat[f][c] >= 1:
                cargado = True
                reg = Matriz(f + 1, c + 1, mat[f][c])
                pickle.dump(reg, archivo)
    archivo.close()

    if cargado:
        print('-' * 80)
        print('El archivo fue cargado con exito.. \nVolviendo al menu de opciones.')
        print('-' * 80)

    return file_mat


def opcion_7(file, ingreso):
    if not ingreso:
        print('No hay datos cargados en el archivo.. Debe pasar por el punto 6.')
        return

    est = '1  2  3  4  5'

    mat = [[0] * 5 for f in range(12)]

    archivo = open(file, 'rb')
    tamanio = os.path.getsize(file)
    while archivo.tell() < tamanio:
        reg = pickle.load(archivo)
        mat[reg.mes - 1][reg.estrellas - 1] += reg.cantidad
    archivo.close()

    print('\t\tEstrellas')
    print('\t  ', est)
    for f in range(len(mat)):
        print('Mes', f + 1, mat[f], '\n')


def principal():
    print('PROYECTOS DE SOFTWARE')

    vec_proyectos = []
    mat = [[0] * 5 for i in range(12)]
    cont_pasadas_op_1 = cont_omitidos_respaldo = 0
    archivo_tags = 'listado.txt'
    archivo_mat = 'matriz.dat'
    now = datetime.now()
    ingreso_al_6 = False
    ingreso_al_4 = False

    opcion = -1
    while opcion != 8:
        menu()
        opcion = int(input('Ingrese la opcion que desee: '))
        print()

        if opcion == 1:
            cont_proy_om = opcion_1(vec_proyectos, cont_pasadas_op_1, cont_omitidos_respaldo)
            print('-' * 120)
            mostrar_arreglo_de_proyectos(vec_proyectos)
            print('-' * 120)
            print('\nCantidad de proyectos cargados: \n' + str(len(vec_proyectos)) + '\nCantidad de proyectos que se '
                  'omitieron: \n' + str(cont_proy_om) + '\n')
            print('-' * 80)
            cont_pasadas_op_1 += 1
            cont_omitidos_respaldo = cont_proy_om
        elif len(vec_proyectos) == 0 and opcion != 8:
            print('No hay datos cargados en el vector de proyectos...\n')
        elif opcion == 2:
            print('-' * 80)
            tag = validar_text_cargado('Ingrese el tag a buscar entre los proyectos: ')
            opcion_2(vec_proyectos, tag, archivo_tags)
        elif opcion == 3:
            opcion_3(vec_proyectos)
        elif opcion == 4:
            ingreso_al_4 = True
            print('-' * 80)
            consulta_mes = validate_range_mes(1, 12, 'Ingrese el mes para analizar en la matriz: ')
            print('-' * 80)
            mat = opcion_4(vec_proyectos, consulta_mes, mat)
        elif opcion == 5:
            rep = validar_text_cargado('Ingrese el repositorio a buscar en los proyectos: ')
            opcion_5(vec_proyectos, rep, now)
        elif opcion == 6:
            archivo_mat = opcion_6(mat, ingreso_al_4)
            if ingreso_al_4:
                ingreso_al_6 = True
        elif opcion == 7:
            print('-' * 80)
            opcion_7(archivo_mat, ingreso_al_6)
            print('-' * 80)
        elif opcion > 8 or opcion < 1:
            print('¡Error! Opcion invalida.. Vuelva a ingresar una opcion..')

    print('Usted eligio la opcion 8 --> Salir \n¡¡¡Vuelva pronto!!!')


if __name__ == '__main__':
    principal()
