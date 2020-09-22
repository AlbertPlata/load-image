#!/usr/bin/env python
# coding: utf-8

#
# ## Algoritmo analisis de imagenes
#
# <br />
# <div class="alert alert-info" role="alert">
# <p><strong>Proyecto Programacion</strong></p>
# <p>Nombres:</p>
# <p>Plata Alberto</p>
# <p>Medina Daniel</p>
# <p></p>
# <p>Secuencia: 1CM10</p>
#
#
#
# </div>

# ## Importar paqueterias necesarias

# In[1]:


import numpy as np
import pandas as pd
import cv2
import glob
import os
import datetime as dt

import os.path

from time import time

import plotly.graph_objects as go


# #### Declaracion de las extensiones y formato de guardado para el procesamiento

# In[2]:


save_folder_storage = './Envios/'
save_extension = '.csv'
name_to_save = '_medias_Pre_envio'


# **Rutas de las carpetas a guardar**

# In[3]:


name_Folder_csv = "/csv"
name_Folder_Graficas = '/Graficas'
name_Folder_Graficas_Promedio = '/Graficas/Promedio'
name_Folder_Graficas_Mediana = '/Graficas/Mediana'


# ## Formato de fotos

# In[4]:


def format():
    print("ejemplo: (.jpg) (.bmp) o escibe (*) para todos los tipos de fotos")
    formato = '*'
    return formato


# ## Traer todos los nombres de las imagenes

# In[5]:


def get_Data(path):
    path += '/*' + formato
    imgs_Names = glob.glob(path)
    return imgs_Names


# ## Validaciones

# ## Validar tamaño fotos

# In[6]:


def validate_photos_size(images, filenames):
    long = 128
    width = 128
    colors = 3

    flag = 1
    img = []

    for key in range(0,len(images)):
        temp = images[key].shape == (long, width, colors)

        if temp == False:
            flag = 0
            img.append(filenames[key])
    return flag, img


# ## Validar rango de numero de imagenes

# In[7]:


def image_number(num, min_img, max_img):

    flag = 0

    if num == 0:
        flag = 2
        return flag
    if num >= min_img and num <= max_img:
        flag = 1
        return flag
    else:
        return flag


# ## Validación de número de imágenes

# In[8]:


def image_number_validation():
    while True:

        minimum = int(input("Numero minimo de imagenes: "))
        maximum = int(input("Numero maximo de imagenes: "))

        if minimum > maximum: print("Orden incorrecto, intentelo denuevo")
        else :
            return minimum, maximum


# ## Validar que la carpeta tenga imagenes

# In[9]:


def there_Images(flag):

    empty_Folder = 0


    if flag == 2:

        print("")
        print("Carpeta vacia")

    elif flag == 1:
        empty_Folder = 1

        print("")
        print("Numero valido de img")


        return empty_Folder

    else:
        print("")
        print("Numero invalido de imagenes")
    return empty_Folder


# ## Cargas

# ### Carga una imagen

# In[10]:


def get_an_image(image_path):
    image = cv2.imread(image_path)
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


# En caso de que tus fotos se cargen en fortamo BGR, desmarcar la linea

# ### Cargar en una matriz todas las imagenes

# In[11]:


def read_images(IMAGE_DIRECTORY):
    images = []

    for file in IMAGE_DIRECTORY:
            images.append(get_an_image(os.path.join(file)))
    return images


# ## Procesos, Promedio y Mediana

# ### Color promedio de un lote de imagenes

# In[12]:


def average_Batch_Images(images):

    average = []
    time_A = []

    for key in range(len(images)):

        average_temp = 0
        start_time = 0
        elapsed_time = 0

        start_time = time()

        average_temp = images[key].mean(axis=0).mean(axis=0)

        elapsed_time = time() - start_time

        time_A.append(elapsed_time)
        average.append(average_temp)

    return average, time_A


# ### Mediana de un lote de imagenes

# In[13]:


def medianas(images):
    median = []
    for key in range(0, len(images)):
        median_temp = []

        image_temp = images[key]
        for j in range(0, 3):

            temp = np.median(image_temp[:,:,j])
            median_temp.append(temp)

        median_temp = np.array(median_temp)
        median.append(median_temp)
    return median


# ---
# ---
#

# ## Proceso corte images

# ### Nombres para las imagenes cortadas

# In[14]:


def cuts_Names(filenames, cuts):
    names = []

    for i in range(0, len(filenames)) :
        for j in range(0,4):
            name = filenames[i]
            temp = name[:-4] + '_' + str(j)
            temp = temp + name[-4:]

            names.append(temp)
    return names


# ### Cortar las imagenes en 32 o 64

# In[15]:


def curt_Images(cutting_size, cuts, images):

    cut_images = []

    for key in range(0, len(images)):

        inferior =0
        maximo= 0
        inferior2 = 0
        maximo2 = 0

        img = images[key]

        for i in range(0, int(cuts)):

            inferior = (i * cutting_size)
            maximo = ((i+1) * cutting_size)

            for j in range (0, int(cuts)):

                inferior2 = (j * cutting_size)
                maximo2 = ((j+1) * cutting_size)

                temp = img[inferior:maximo, inferior2:maximo2]
                cut_images.append(temp)

    return cut_images


# ### Guardar las imagenes cortadas

# In[16]:


def save_images(filenames, images, destination_Directory):
    name_folder = '/images'

    temp = destination_Directory + name_folder
    create_folder(temp)

    for key in range(0, len(filenames)):
        cv2.imwrite(temp+ '/' + filenames[key], images[key])


# ### Menu para escojer el tamaño de corte

# In[17]:


def menu_pre_process():
    print("")
    print("""Menu de preprocesamiento:
    1.-Tamaño original
    2.-Divir a 32 x 32
    3.-Dividir a 64 x 64
    """)
    option = str(3)
    return option


# ### Proceso de corte de las img

# In[18]:


def cutting_Process(images, filenames):

    while True:
        option = menu_pre_process()

        if option == '1':

            return images, filenames

        if option == '2':
            filenames = cuts_Names(filenames, 4**2)
            images = curt_Images(32, 4,images)

            return images, filenames

        if option == '3':
            filenames = cuts_Names(filenames, 2**2)
            images = curt_Images(64, 2,images)

            return images, filenames
        else:
            print("")
            print("invalida")


# ---
# ---

# ## Proceso central

# In[19]:


def process(images):

    #images = read_images(path)

    average , time = average_Batch_Images(images)

    mdn = medianas(images)

    return average, mdn, time


# ## Guardar analisis

# In[20]:


def save_average(filenames, average,total_time, mediana):
    columns={"Nombre de la imagen" ,"Color Promedio","Mediana", "Tiempo total por todo el lote"}
    df = pd.DataFrame(columns=columns)
    df["Nombre de la imagen"] = filenames
    df["Color Promedio"] = average
    df["Mediana"] = mediana
    df["Tiempo total por todo el lote"] = total_time
    df.instrument_name = total_time
    df.to_csv(save_name, index=False)


# ## Funcion que retorna la existensia de un directorio

# In[21]:


def exist_Directory(path):
    return os.path.exists(path)


# ## Funcion para optener ruta de la imagen

# In[22]:


def input_path_images():
    while True:
        print("")
        path = './images'

        flag = exist_Directory(path)

        if flag == True:
            print("")
            print("La ruta existe")
            return path
        else:
            print("")
            print("La carpeta no existe ")
            print("Intentalo de nuevo")


# ### Nombres cortos

# In[23]:


def new_names(filenames):
    new_file_names = []

    for key in range(0, len(filenames)):
        temp = os.path.basename(filenames[key])
        new_file_names.append(temp)
    return new_file_names


# ---
# ---

# ## Funciones para carpetas

# ### Crear carpetas necesarias

# In[24]:


def create_Branched_Folders(destination_Directory):
    create_folder(destination_Directory)
    create_folder(destination_Directory + name_Folder_csv)
    create_folder(destination_Directory + name_Folder_Graficas)
    create_folder(destination_Directory + name_Folder_Graficas_Promedio)
    create_folder(destination_Directory + name_Folder_Graficas_Mediana)


# ### Crear carpetas

# In[25]:


def create_folder(destination_Directory):
    try:
        os.stat(destination_Directory)
    except:
        os.mkdir(destination_Directory)


# ---
# ---

# ## Graficas

# ### Graficas promedio

# In[26]:


def average_graphs(average, filenames, path):
    for key in range(0,len(average)):
        Colors=['R', 'G', 'B']

        name = filenames[key]
        name = name[:-3]

        x = Colors
        y = average[key]

        # Use textposition='auto' for direct text
        fig = go.Figure(data=[go.Bar(
                    x=x, y=y,
                    text=y,
                    textposition='auto',
                    marker_color= 'rgb(' + str(y[0])+','+str(y[1])+','+str(y[2]) + ')'
                )])
        fig.update_layout(title_text='Color Promedio')

        fig.write_image(average_graphics_path+"/"+ name + "jpg")


# ### Graficas Mediana

# In[27]:


def median_graphs(mdn, filenames, path):
    for key in range(0,len(mdn)):
        Colors=['R', 'G', 'B']

        name = filenames[key]
        name = name[:-3]

        x = Colors
        y = mdn[key]

        # Use textposition='auto' for direct text
        fig = go.Figure(data=[go.Bar(
                    x=x, y=y,
                    text=y,
                    textposition='auto',
                    marker_color= 'rgb(' + str(y[0])+','+str(y[1])+','+str(y[2]) + ')'
                )])
        fig.update_layout(title_text='Color Promedio')

        fig.write_image(median_graphics_path+"/"+ name + "jpg")


# ### Funciones que crea las graficas

# In[28]:


def make_graphics_save(average, mdn, filenames, average_graphics_path, median_graphics_path):
    average_graphs(average, filenames, average_graphics_path)
    median_graphs(mdn, filenames, median_graphics_path)


# ---
# ---

# ## Tiempos

# ### Funcion para obtener la fecha y hora

# In[29]:


def date_And_Time():
    FechaHoy = dt.datetime.now()
    FechaAAAAMMDDHHMMSSss = FechaHoy.strftime("%Y%m%d_%H%M%S")
    return FechaAAAAMMDDHHMMSSss


# ---
# ---

# ## Impreciones

# In[30]:


def print_Img_Not_Sized(bad_images):
    for key in range(0, len(bad_images)):
        print(bad_images[key])


# -----------------------------------
# -----------------------------------
#
# # Inicio de los procesos para el programa
#

# ## obtener la ruta de la carpte a usar

# In[31]:


path = input_path_images()


# ### formato de las imagenes

# In[32]:


formato = format()


# ### Definimos un rango de fotos

# In[33]:


minimum = 1
maximum = 30


# In[34]:


# SI quiere definir un rango probable de imagenes desmarque esta opccion
#minimum, maximum = image_number_validation()


# ### Validaciones para el programa

# In[35]:


filenames = get_Data(path)

numero_imagenes = len(filenames)

flag = image_number(numero_imagenes, minimum, maximum)

folder_status = there_Images(flag)


# ---
# validar si la carpeta tiene imagenes
# obtener validacion si las imagenes cumplen con el tamaño y las imagenes que no cumplen con el

# In[36]:


flag2 = -1
if folder_status == 1:
    images = read_images(filenames)
    flag2, glitch_Image= validate_photos_size(images, filenames)


# ---
# Si las imagenes cumplen con el tamaño, pregunta si las quiere cortar
# Si no cumplen con el tamaño te dice las imagenes que son incorrectas

# In[37]:


if flag2 == 1:
    images, filenames =  cutting_Process(images, filenames)
if flag2 == 0:
    print("Imagenes fuera de rango: ")
    print("")
    print_Img_Not_Sized(glitch_Image)


# ##### Creamos las variables necesarias para terminar el programa

# In[38]:


save_name = -1

if flag2 == 1:

    start_time = time()

    Tiempo = date_And_Time()

    destination_Directory = save_folder_storage + Tiempo

    save_name = destination_Directory + '/csv/' +Tiempo + name_to_save + save_extension

    average_graphics_path  = destination_Directory + name_Folder_Graficas_Promedio

    median_graphics_path = destination_Directory + name_Folder_Graficas_Mediana


# ##### Proceso final

# In[39]:


if flag2 == 1:

    create_Branched_Folders(destination_Directory)

    average, mdn, time_A , = process(images)


    filenames = new_names(filenames)

    save_images(filenames, images, destination_Directory)

    make_graphics_save(average, mdn, filenames, average_graphics_path, median_graphics_path)

    elapsed_time = time() - start_time


    save_average(filenames, average, elapsed_time, mdn)

    print("")
    print("Tiempo de analisis: %0.10f segundos" % elapsed_time)
    print ("Medias de imagenes obtenidas y guardadas sin ningun problema")
    print("Se guardo en {}".format(save_name))
    print("")


# ## Prueba / vista de los datos, guardados

# In[40]:


if save_name != -1:
    df = pd.read_csv(save_name)
    print(df)


# In[41]:


df


# In[42]:


print("Adios")
print("")


# El proceso se alarga, por que las graficas se crean con iplot, si canviamos la herramienta de graficado el tiempo puede bajar.
#
# El algoritmo por analisis individual dura 0.001
#
# Por lo que un que tu lote sea muy grande rara vez dura mas de 1 deg
