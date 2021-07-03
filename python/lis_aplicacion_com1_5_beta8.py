# Hacer funcion automatico de cartel luminoso
#este programa es para windows.
#Funciona con programa arduino: centralita_lis_1_beta_6
#NOTA: para parar la consola pulsar CONTROL + C


from tkinter import *
from tkinter import messagebox
from tkinter import colorchooser #importar para ventana de eleccion de color
import tkinter as tk
from tkinter import ttk

import serial
from datetime import datetime
import threading

puerto_serie=serial.Serial()
#puerto_serie=serial.Serial("COM6", 9600)
v_tiempo=0
tiempo=0
crono1=0
cont1=0
principio_tx='#@99@'
final_tx='$'
direccion_tx='0'
dato1_tx='0'
dato2_tx='0'
dato3_tx='0'
separador_tx='@'


checksun_rx=2000
direccion_rx=1000
dato1_rx=0
lectura_rx=False
puerto_serie_on=False

dt=datetime.now()
segundos=dt.second



raiz=Tk()
#raiz.geometry("1280x720") #define el tamaño de la ventana
raiz.resizable(1,1) #habilitar si se puede modificar el ancho y el alto de la ventana. admite 0 y 1
#si no se escrive la intruccion de definir el tamaño de la ventana, se ajusta al frame
raiz.config(bg="black") #configurar el color de fondo de la ventana
raiz.title("Control sala LIS")
raiz.iconbitmap("control_lis\imagenes\icono_lis_1.ico")



t_sala=StringVar()
t_ext=StringVar()
fecha=StringVar()
i_tira_led=StringVar()
auto_man=IntVar()
auto_selec=IntVar()
foco_auto=IntVar()
cartel_auto=IntVar()


# ESTILOS ------------------------------------------------------------------------------------------------------------
style = ttk.Style()
style.map("estilo_1.TButton",
    background=[('active', 'white')],
    #highlightcolor=[('focus', 'green'), ('!focus', 'red')],
    #highlightbackground=[('pressed', 'purple'), ('focus', 'green'), ('!focus', 'red')]
)
"""
style.map("estilo_2.TButton",
    foreground=[('pressed', 'purple')],
    background=[('pressed', '#33f537'), ('active', 'cyan'), ('!active', '#33f537'), ('!focus', '#33f537') ],
    highlightcolor=[('focus', 'green'), ('!focus', 'red')],
    highlightbackground=[('!pressed', '#33f537'), ('!focus', '#33f537')]
)
"""
style.configure('separador_1.TSeparator', 
    background='#5E595F',
    highlightthickness='0',
    relief='ridge'
    )

style.configure('estilo_1.TLabel',
    font=('Helvetica', 10, 'bold'),
    background='#78637C'
)

style.configure('estilo_2.TLabel',
    font=('Helvetica', 15, 'bold', 'underline'),
    background='#78637C'
)

style.configure('estilo_5.TLabel',
    font=('Helvetica', 14),
    background='#78637C'
)

style.configure('estilo_6.TLabel',
    font=('Helvetica', 60),
    background='#78637C'
)

style.configure('estilo_1.TButton',
    background='white',
    foreground='black',
    font=('Helvetica', 15, 'bold')
)

style.configure('estilo_2.TButton',
    background='#33f537', 
    #foreground='green',
    foreground='#26d113',
    font=('Helvetica', 15, 'bold')
)

style.configure('Wild.TButton',
    background='black',
    foreground='white',
    highlightthickness='100',
    font=('Helvetica', 18, 'bold')
)

style.map("Wild.TButton",
    foreground=[('disabled', 'yellow'), ('pressed', 'red'), ('active', 'blue')],
    background=[('disabled', 'magenta'), ('pressed', '!focus', 'cyan'), ('active', 'green')],
    highlightcolor=[('focus', 'green'), ('!focus', 'red')],
    relief=[('pressed', 'groove'), ('!pressed', 'ridge')]
)

#COLOR LILA FLOJO = #f8e7ff
#COLOR GRIS-FONDO = #5E595F
#COLOR GRIS-LILA = #78637C
#COLOR AZUL FLOJO = #00a8f3
#COLOR AMARILLO FLOJO = #fff79a
#COLOR VERDE ON = #33f537
#COLOR VERDE PARA LETRAS BOTONES TTK = #26d113



# FUNCIONES --------------------------------------------------------------------------------------------------------------------
def conectar():
    global puerto_serie
    global puerto_serie_on
    if puerto_serie_on==False:
        try:
            puerto_serie.close()
            puerto_serie=serial.Serial(lista_desp_1.get(), lista_desp_2.get())
            puerto_serie.flushInput()
            etiqueta_7.configure(text="CONECTADO", background="#33f537")
            puerto_serie_on=True
            boton_11.config(text="DESCONECTAR")
            messagebox.showinfo("Conexión centralita control", "Conexión establecida con éxito.\nPuerto: "+ lista_desp_1.get() +  "\nVelocidad: " + str(lista_desp_2.get()) + " baudios")
        except serial.serialutil.SerialException:
            messagebox.showinfo("Conexión centralita control", "No es posible realizar la conexión.\n\nPuerto no asignado a la centralita control\no cable desconectado.")
    else:
        puerto_serie.close()
        boton_11.config(text="CONECTAR")
        etiqueta_7.configure(text="DESCONECTADO", background="red")
        puerto_serie_on=False
        messagebox.showinfo("Conexión centralita control", "Desconectado.\nConexión cerrada.             ")


def enviar_arduino(boton_pulsado):
    global puerto_serie
    global direccion_tx
    global dato1_tx
    global dato2_tx
    global dato3_tx
    global t_extractor_temp_off
    global t_extractor_auto_on
    global t_extractor_auto_off
    global rgb_red
    global rgb_green
    global rgb_blue
    

    if puerto_serie_on==True:
        pass

    else:
        messagebox.showinfo("Conexión centralita control", "No hay conexión con centralita control") 
    
    """
    nombres direccion de envio:

    1--- pulsadores
    5--- color grb led
    10-- byte automatico_1
    11-- tiempos extractor automatico
    20-- guardar cambios
    21-- cargar configuracion
    """


    try:
        if puerto_serie_on==True:
            if boton_pulsado==1:    #apagar todas
                direccion_tx="1"
                dato1_tx='1'
                #dato2_tx
                #dato3_tx
            
            if boton_pulsado==2:    #luces izquierda
                direccion_tx="1"
                dato1_tx='2'
                #dato2_tx
                #dato3_tx
            
            if boton_pulsado==3:    #luces derecha
                direccion_tx="1"
                dato1_tx='3'
                #dato2_tx
                #dato3_tx
            
            if boton_pulsado==4:    #luz trastero
                direccion_tx="1"
                dato1_tx='4'
                #dato2_tx
                #dato3_tx

            if boton_pulsado==5:    #foco exterior
                direccion_tx="1"
                dato1_tx='5'
                #dato2_tx
                #dato3_tx

            if boton_pulsado==6:   #pulsador extractor
                direccion_tx="1"
                dato1_tx='6'
                #dato2_tx
                #dato3_tx
            
            if boton_pulsado==7:    #pulsador rgb led
                direccion_tx='1'
                dato1_tx='7'
                #dato2_tx
                #dato3_tx
            
            if boton_pulsado==8:    #pulsador rgb mas
                direccion_tx='1'
                dato1_tx='8'
                #dato2_tx
                #dato3_tx

            if boton_pulsado==9:    #pulsador rgb menos
                direccion_tx='1'
                dato1_tx='9'
                #dato2_tx
                #dato3_tx
                
            if boton_pulsado==10:   #extractor automatico
                direccion_tx="10"
                dato1_tx='0'        #posicion bit automatico_1
                dato2_tx='1'        
                #dato3_tx=''
            
            if boton_pulsado==11:   #extractor manual
                direccion_tx="10"
                dato1_tx='0'        #posicion bit automatico_1
                dato2_tx='0'
                #dato3_tx='0'

            if boton_pulsado==12:   #extractor apagado temporizado
                direccion_tx="10"
                dato1_tx='1'        #posicion bit automatico_1        
                dato2_tx='1'
                #dato3_tx='0'

            if boton_pulsado==13:   #extractor encedido y apagado auto
                direccion_tx="10"
                dato1_tx='1'        #posicion bit automatico_1     
                dato2_tx='0'
                #dato3_tx='0'
            
            if boton_pulsado==14:   #tiempos de extractor automatico
                direccion_tx="11"
                dato1_tx=t_extractor_temp_off            
                dato2_tx=t_extractor_auto_on
                dato3_tx=t_extractor_auto_off

            if boton_pulsado==15:   #color rgb led
                direccion_tx="5"
                dato1_tx=rgb_red             
                dato2_tx=rgb_green
                dato3_tx=rgb_blue
            
            if boton_pulsado==16:   #guardar cambios
                direccion_tx="20"
                dato1_tx=dato_guardado            
                #dato2_tx='0'
                #dato3_tx='0'
            
            if boton_pulsado==17:   #cargar configuración
                direccion_tx='21'
                dato1_tx=dato_cargado
                dato2_tx='0'
                dato3_tx='0'

            if boton_pulsado==18:   #tiempos de foco exterior automatico on
                direccion_tx="12"
                dato1_tx=t_foco_ext_auto_on_h            
                dato2_tx=t_foco_ext_auto_on_m
                #dato3_tx=

            if boton_pulsado==19:   #tiempos de foco exterior automatico off
                direccion_tx="13"
                dato1_tx=t_foco_ext_auto_off_h        
                dato2_tx=t_foco_ext_auto_off_m 
                #dato3_tx=
            
            if boton_pulsado==20:   #foco exterior automatico
                direccion_tx="10"
                dato1_tx='6'        #posicion bit automatico_1
                dato2_tx='1'        
                #dato3_tx=''
            
            if boton_pulsado==21:   #foco exterior manual
                direccion_tx="10"
                dato1_tx='6'        #posicion bit automatico_1
                dato2_tx='0'        
                #dato3_tx=''
            
            if boton_pulsado==22:   #cartel luminoso automatico
                direccion_tx="10"
                dato1_tx='7'        #posicion bit automatico_1
                dato2_tx='1'        
                #dato3_tx=''
            
            if boton_pulsado==23:   #cartel luminoso manual
                direccion_tx="10"
                dato1_tx='7'        #posicion bit automatico_1
                dato2_tx='0'        
                #dato3_tx=''
        

            mensaje = principio_tx + direccion_tx + separador_tx + dato1_tx + separador_tx + dato2_tx + separador_tx + dato3_tx + final_tx
            puerto_serie.write(mensaje.encode())
            direccion_tx="0"
            dato1_tx='0'
            dato2_tx='0'
            dato3_tx='0'
    
    except serial.serialutil.PortNotOpenError:
        messagebox.showerror(title="Error", message="Fallo en el envio de datos")
    

def recibir_arduino():
    global checksun_rx
    global direccion_rx
    global dato1_rx
    global dato2_rx
    global dato3_rx
    global dato4_rx
    global dato5_rx
    global dato6_rx
    global lectura_rx
        
    arduino=str(puerto_serie.readline())
    print(arduino)
    dato_rx=arduino[2:] 
    dato_rx=dato_rx.split('@')
    print(dato_rx)
        
    try:
        if len(dato_rx) == 8:     
            direccion_rx=int(dato_rx[0])
            dato1_rx=int(dato_rx[1])
            dato2_rx=int(dato_rx[2])
            dato3_rx=int(dato_rx[3])
            dato4_rx=int(dato_rx[4])
            dato5_rx=int(dato_rx[5])
            dato6_rx=int(dato_rx[6])
            checksun_rx=dato_rx[7]
            checksun_rx=int(checksun_rx[:checksun_rx.find('\\')])
            lectura_rx=True
            
    except ValueError:
        print("\n---FALLO COMUNICACION--- ValueError\n")
        estado_com=False
    except TypeError:
        print("\n---FALLO COMUNICACION--- TypeError\n")
        estado_com=False
    except NameError:
        print("\n---FALLO COMUNICACION--- NameError\n")
        estado_com=False


    if lectura_rx==True and checksun_rx==direccion_rx+dato1_rx:
        print("direccion: " ,direccion_rx)
        print("dato1: " ,dato1_rx)
        print("dato2: " ,dato2_rx)
        print("dato3: " ,dato3_rx)
        print("dato4: " ,dato4_rx)
        print("dato5: " ,dato5_rx)
        print("dato6: " ,dato6_rx)
        print("checksun: " ,checksun_rx)
        print("")
            
        checksun_rx=2000
        lectura_rx=False
        estado_com=True
        if direccion_rx==1:
            t_sala.set("Temperatura sala :       {} º".format(dato5_rx))
            t_ext.set("Temperatura exterior : {} º".format(dato6_rx))
            etiqueta_1.configure(textvariable=t_sala)
            etiqueta_2.configure(textvariable=t_ext)
            decimal_binaio(1, dato4_rx) #automatico_1
            decimal_binaio(2, dato5_rx) #entradas_1
            decimal_binaio(3, dato6_rx) #salidas_1
        
        if direccion_rx==2:
            lista_desp_3.set("{} minutos".format(dato1_rx))
            lista_desp_4.set(dato2_rx)
            lista_desp_5.set(dato3_rx)
        
        if direccion_rx==3:
            global rgb_red
            global rgb_green
            global rgb_blue
            i_tira_led.set("Intensidad:  {} %".format(dato4_rx))
            etiqueta_10.configure(textvariable=i_tira_led)
            lectura_color_tira_led(dato1_rx, dato2_rx, dato3_rx)
            rgb_red=dato1_rx
            rgb_green=dato2_rx
            rgb_blue=dato3_rx
            rgb_intensidad_led=dato4_rx
            decimal_binaio(3, dato6_rx) #salidas_1
            direccion_rx=1
        
        if direccion_rx==4:
            if dato1_rx<10:
                lista_desp_6.set("0{}".format(dato1_rx))
            else:
                lista_desp_6.set("{}".format(dato1_rx))
            if dato2_rx<10:
                lista_desp_7.set("0{}".format(dato2_rx))
            else:
                lista_desp_7.set("{}".format(dato2_rx))
            if dato3_rx<10:
                lista_desp_8.set("0{}".format(dato3_rx))
            else:
                lista_desp_8.set("{}".format(dato3_rx))
            if dato4_rx<10:
                lista_desp_9.set("0{}".format(dato4_rx))
            else:
                lista_desp_9.set("{}".format(dato4_rx))

            decimal_binaio(1, dato5_rx) #automatico_1
            decimal_binaio(3, dato6_rx) #salidas_1
            direccion_rx=1

            
        comando_recivido_centralita(direccion_rx)
        direccion_rx=1000
    else:
        print("\nFALLO EN LECTURA DATOS RX\n")


def decimal_binaio(pos,decimal):
    """
    Funcion para pasra numero decimal a numero binario.
    pos=indica donde vamos a guardar el numero binario obtenido
    decimal=indica el numero decimal que vamos a convertir a vinario
    """
    global automatico_1
    global salidas_1

    cont_pos=8  
    lista_bin = [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0]

    while decimal > 0:                  #el bucle se repite si numero decimal es mayor de 0
        cont_pos-=1                     #en cada vuelta del bucle se resta uno a la posicion
        residuo = int(decimal % 2)      #se almacena 0 o 1 en la variable residuo
        decimal = int(decimal / 2)      #se divide el numero decimal entre dos hasta que sea 0
        lista_bin[cont_pos] = residuo   #se añade la variable residuo(0 o 1) a la lista en la posicion(cont_pos)

    if pos==1:
        automatico_1 = lista_bin
        print(automatico_1)
    if pos==2:
        entradas_1 = lista_bin
        print(entradas_1)
    if pos==3:
        salidas_1 = lista_bin
        print(salidas_1)

"""
Nota: la posicion de los bit de cada byte esta invertido respecto a la posicion que tiene el la centralita
automatico_1:
0   cartel luminoso.
1   foco exterior.
2   libre.
3   libre.
4   libre.
5   libre.
6   extrator tipo auto.
7   extractor aire.

entradas_1:
0
1
2
3
4
5
6
7

salidas_1:
0   libre.
1   tira rgb led.
2   cartel luminoso
3   foco exterior
4   luz trastero.
5   luz derecha.
6   luz izquierda.
7   extractor aire.

"""

def lectura_color_tira_led(c1, c2, c3):
    """
    Funcion para converir valores rgb a hexadecimal.
    Primero. Pasamos los valores a hexadecimal.
    Segundo. Descartamos los dos primeros caracteres que crea en la conversion.
    Tercero. Añade un cero al numero exacedicmal si es menos de 16 (15=f) (16=10) para obtener el fomato de dos digitos.
    Cuarto. Añade el simbolo '#' al numero para obtener el formato correcto.
    """
    nr=hex(c1)
    ng=hex(c2)
    nb=hex(c3)
    
    nr=nr[2:]
    ng=ng[2:]
    nb=nb[2:]

    if c1<16:
        nr="0"+nr
    
    if c2<16:
        ng="0"+ng
    
    if c3<16:
        nb="0"+nb

    color_tira_led_hex="#"+nr+ng+nb
    cuadro_color.config(background=color_tira_led_hex)


def comando_recivido_centralita(v_direccion):
    global automatico_1
    global salidas_1

    if v_direccion==1:
        if salidas_1[7]:
            boton_10.config(image=imagen3)
        else:
            boton_10.config(image=imagen2)

        if salidas_1[6]:
            boton_2.configure(style="estilo_2.TButton")
        else:
            boton_2.configure(style="estilo_1.TButton")
        
        if salidas_1[5]:
            boton_3.configure(style="estilo_2.TButton")
        else:
            boton_3.configure(style="estilo_1.TButton")
        
        if salidas_1[4]:
            boton_4.configure(style="estilo_2.TButton")
        else:
            boton_4.configure(style="estilo_1.TButton")
        
        if salidas_1[3]:
            boton_5.configure(style="estilo_2.TButton")
        else:
            boton_5.configure(style="estilo_1.TButton")
        
        if salidas_1[1]:
            boton_6.configure(text="Apagar", background="#33f537")
        else:
            boton_6.configure(text="Encender", background="white")
        
        if automatico_1[0]:
            cartel_auto.set(1)
        else:
            cartel_auto.set(2)
        
        if automatico_1[1]:
            foco_auto.set(1)
        else:
            foco_auto.set(2)
        
        if automatico_1[6]:
            auto_selec.set(1)
        else:
            auto_selec.set(2)
        
        if automatico_1[7]:
            auto_man.set(1)
        else:
            auto_man.set(2)
    

def cerrar_programa():
    v_cerrar=messagebox.askquestion("Salir app", "¿Desea salir de la aplicación?")
    if v_cerrar=="yes":
        puerto_serie.close()
        raiz.destroy()


def licencia():
    messagebox.showinfo("Licencia", "Reservado derechos de autor \n       --USO CON LICENCIA--")


def acerca_de():
    messagebox.showinfo("Información", "Version 1.0 \n-Control sala LIS-")
        

def SM_1():
    fecha.set("{}:{}:{}".format(dt.strftime("%H"), dt.strftime("%M"), dt.strftime("%S")))
    etiqueta_hora.configure(textvariable=fecha)


def selec_lista_1(event):
    print(lista_desp_1.get())


def selec_lista_2(event):
    print(lista_desp_2.get())


def selec_tiempos_extractor(event):   #tiempo automatico extractor (listas deplegables)
    global t_extractor_temp_off #tiempo apagado temporizado extractor
    global t_extractor_auto_on  #tiempo encendido auto extractor
    global t_extractor_auto_off #tiempo pagado auto extractor

    t_extractor_temp_off=lista_desp_3.get()[:lista_desp_3.get().find(" ")] #coger de la cadena hasta el espacio en blanco(los numeros)
    t_extractor_auto_on=lista_desp_4.get()  
    t_extractor_auto_off=lista_desp_5.get() 
    enviar_arduino(14)


def selec_tiempos_on_foco(event):
    global t_foco_ext_auto_on_h
    global t_foco_ext_auto_on_m
   
    t_foco_ext_auto_on_h=lista_desp_6.get()         #guardamos en la variable los datos de la lista desplegable 6
    comprobacion=t_foco_ext_auto_on_h.find("0")      #guardamos la posicion de '0' en la varible comporbacion
    if comprobacion==0:                             
        t_foco_ext_auto_on_h=t_foco_ext_auto_on_h[1]    #si la posicion de 0 en la cadena es 0 (01, 02, ...), cogemos solo el carater de la posicion 1
    
    t_foco_ext_auto_on_m=lista_desp_7.get()         
    comprobacion=t_foco_ext_auto_on_m.find("0")   
    if comprobacion==0:                             
        t_foco_ext_auto_on_m=t_foco_ext_auto_on_m[1]

    enviar_arduino(18)
    
    
def selec_tiempos_off_foco(event):
    global t_foco_ext_auto_off_h
    global t_foco_ext_auto_off_m

    t_foco_ext_auto_off_h=lista_desp_8.get()         
    comprobacion=t_foco_ext_auto_off_h.find("0")   
    if comprobacion==0:                             
        t_foco_ext_auto_off_h=t_foco_ext_auto_off_h[1]

    t_foco_ext_auto_off_m=lista_desp_9.get()         
    comprobacion=t_foco_ext_auto_off_m.find("0")   
    if comprobacion==0:                             
        t_foco_ext_auto_off_m=t_foco_ext_auto_off_m[1]

    enviar_arduino(19)


def seleccion_color():
    global rgb_red
    global rgb_green
    global rgb_blue
    
    v_color=colorchooser.askcolor(title="Seleccion color", color="black") 
    #title -nombre qu aparece en la ventana
    #color -especifica el color de partida
    #devueve una lisata con dos objetos. [0]tupla con los colores rgb en binario. [1]color elegido en hexadecimal

    v_color_bin=v_color[0]

    rgb_red=v_color_bin[0]
    rgb_green=v_color_bin[1]
    rgb_blue=v_color_bin[2]
    
    #pasamos los valores con coma a numeros enteros
    rgb_red=int(rgb_red)
    rgb_green=int(rgb_green)
    rgb_blue=int(rgb_blue)

    #pasamos los valores enteros a string para enviarlos a centralita
    rgb_red=str(rgb_red)
    rgb_green=str(rgb_green)
    rgb_blue=str(rgb_blue)
    
    enviar_arduino(15)

def guardar_cambios(g):
    global dato_guardado

    if g==1: 
        valor=messagebox.askquestion("Guardar cambios", "¿Guardar todos los cambios?")
        #ventana de pregunta con icono de interrogante y botones Yes y No.
        #devuelve el texto yes si pulsas el boton de Yes
        #devuelvo el texto no si pulsas el boton de No
        #primer texto: nombre que aparece en la ventana
        #segundo texto: texto que aparece dentro de la ventana

        dato_guardado=str(g)

    if g==2: 
        valor=messagebox.askquestion("Guardar cambios", "¿Guardar cabios en ventilacion sala?")
        dato_guardado=str(g)
    
    if g==3: 
        valor=messagebox.askquestion("Guardar cambios", "¿Guardar cabios en tira led RGB?")
        dato_guardado=str(g)
    
    if g==4: 
        valor=messagebox.askquestion("Guardar cambios", "¿Guardar cabios en foco exterior?")
        dato_guardado=str(g)

    if valor=="yes":
        enviar_arduino(16)

def cargar_datos(c):
    global dato_cargado

    if c==1: 
        valor=messagebox.askquestion("Cargar configuración", "¿Cargar configuración general?")
        #ventana de pregunta con icono de interrogante y botones Yes y No.
        #devuelve el texto yes si pulsas el boton de Yes
        #devuelvo el texto no si pulsas el boton de No
        #primer texto: nombre que aparece en la ventana
        #segundo texto: texto que aparece dentro de la ventana

        dato_cargado=str(c)

    if c==2: 
        valor=messagebox.askquestion("Cargar configuración", "¿Cargar configuración ventilación sala?")
        dato_cargado=str(c)
    
    if c==3: 
        valor=messagebox.askquestion("Cargar configuración", "¿Cargar configuración tira led RGB?")
        dato_cargado=str(c)
    
    if c==4: 
        valor=messagebox.askquestion("Cargar configuración", "¿Cargar configuración foco exterior?")
        dato_cargado=str(c)

    if valor=="yes":
        enviar_arduino(17)


# HILO 2 ----------------------------------------------------------------------------------------
def hilo2():
    while True:
        global dt
        global segundos
        global tiempo
        global v_tiempo
        dt = datetime.now()
       
        
        if segundos < dt.second or segundos==59 and dt.second==0:
            segundos=dt.second
            SM_1()
        

        if v_tiempo != dt.microsecond // 100000:
            v_tiempo=dt.microsecond // 100000
            #pulso cada 200 milisegundos
            if puerto_serie_on==True:
                recibir_arduino()




# FRAMES ---------------------------------------------------------------------------------------
frame1=Frame(raiz) #Cuadro izquierda. Botones de alumbrado.
frame1.pack(side="left", fill="y", expand=0)
frame1.config(width="300", height="720", bg="#78637C", highlightbackground="#5E595F", highlightcolor="#5E595F", highlightthickness=10)

frame2=Frame(raiz) #Cuadro derecha. Contenedor de frame3, frame4, frame5.
frame2.pack(side="right", anchor="n", fill="both", expand="true")
frame2.config(width="980", height="720", bg="#5E595F", relief="groove")

frame3=Frame(frame2) #Cuadro arriba dentro de frame2. Informacion.
frame3.pack(side="top", anchor="n", fill="x", expand="true")
frame3.config(width="980", height="120", bg="#78637C", highlightbackground="#5E595F", highlightcolor="red", highlightthickness=10)
#borde frame3.config(relief="groove", bd=10)

frame4=Frame(frame2) #Cuadro central dentro de frame2. Extractor y configuracion.
frame4.pack(fill="both", expand="true")
frame4.config(width="980", height="480", bg="#78637C", highlightbackground="#5E595F", highlightcolor="#5E595F", highlightthickness=10)

frame5=Frame(frame2) #Cuadro abajo dentro de frame2. Tira de le RGB
frame5.pack(side="bottom", anchor="s", fill="x", expand="true")
frame5.config(width="980", height="120", bg="#78637C", highlightbackground="#5E595F", highlightcolor="red", highlightthickness=10)


#imagen logo ojo
imagen1=PhotoImage(file="control_lis\imagenes\png\ojo_300_fondo.png")
fondo=Label(frame1, image=imagen1)
fondo.place(x=0, rely=0.59, relwidth=1, height=287)

#Barra de tareas -------------------------------------------------------------------------------------------------------------
barra_menu=Menu(raiz)
raiz.config(menu=barra_menu, width=300, height=600)

Archivo_menu=Menu(barra_menu, tearoff=0)
Archivo_menu.add_command(label="Conectar", command=conectar)
Archivo_menu.add_command(label="Crear tabla")
Archivo_menu.add_command(label="Salir", command=cerrar_programa) 

guardar_menu=Menu(barra_menu, tearoff=0)
guardar_menu.add_command(label="Guardar todo", command=lambda:guardar_cambios(1))
guardar_menu.add_separator() #creamos una barra separadora en menu guardar
guardar_menu.add_command(label="Ventilación sala", command=lambda:guardar_cambios(2))
guardar_menu.add_command(label="Tira led", command=lambda:guardar_cambios(3))
guardar_menu.add_separator()
guardar_menu.add_command(label="Foco exterior", command=lambda:guardar_cambios(4))

cargar_menu=Menu(barra_menu, tearoff=0)
cargar_menu.add_command(label="Configuración general", command=lambda:cargar_datos(1))
cargar_menu.add_separator() #creamos una barra separadora en menu guardar
cargar_menu.add_command(label="Configuración ventilación sala", command=lambda:cargar_datos(2))
cargar_menu.add_command(label="Configuración tira led", command=lambda:cargar_datos(3))
cargar_menu.add_separator()
cargar_menu.add_command(label="Configuración foco exterior", command=lambda:cargar_datos(4))

ayuda_menu=Menu(barra_menu, tearoff=0)
ayuda_menu.add_command(label="Licencia", command=licencia)
ayuda_menu.add_command(label="Acerca de...", command=acerca_de)

barra_menu.add_cascade(label="Archivo", menu=Archivo_menu)
barra_menu.add_cascade(label="Guardar",menu=guardar_menu)
barra_menu.add_cascade(label="Cargar",menu=cargar_menu)
barra_menu.add_cascade(label="Ayuda",menu=ayuda_menu)

# BOTONES ---------------------------------------------------------------------------------------

boton_1=ttk.Button(frame1, text="Apagar todas")
boton_1.place(x=0, y=0, relwidth=1, height=60)
boton_1.configure(style="estilo_1.TButton", command=lambda:enviar_arduino(1))

boton_2=ttk.Button(frame1, text="Luces izquierda")
boton_2.place(x=0, y=60, relwidth=1, height=60)
boton_2.configure(style="estilo_1.TButton", command=lambda:enviar_arduino(2))

boton_3=ttk.Button(frame1, text="Luces derecha")
boton_3.place(x=0, y=120, relwidth=1, height=60)
boton_3.configure(style="estilo_1.TButton", command=lambda:enviar_arduino(3))

boton_4=ttk.Button(frame1, text="Luz trastero")
boton_4.place(x=0, y=180, relwidth=1, height=60)
boton_4.configure(style="estilo_1.TButton", command=lambda:enviar_arduino(4))

boton_5=ttk.Button(frame1, text="Foco exterior")
boton_5.place(x=0, y=240, relwidth=1, height=60)
boton_5.configure(style="estilo_1.TButton", command=lambda:enviar_arduino(5))


boton_6=Button(frame5, text="Encender")
boton_6.place(relx=0.05, rely=0.35, relwidth=0.15, relheight=0.35)
boton_6.config(activeforeground="#F50743", command=lambda:enviar_arduino(7))

boton_7=Button(frame5, text="Color")
boton_7.place(relx=0.25, rely=0.35, relwidth=0.15, relheight=0.35)
boton_7.config(activeforeground="#F50743", command=lambda:seleccion_color())

boton_8=Button(frame5, text="Más intesidad")
boton_8.place(relx=0.45, rely=0.35, relwidth=0.15, relheight=0.35)
boton_8.config(activeforeground="#F50743", command=lambda:enviar_arduino(8))

boton_9=Button(frame5, text="Menos intensidad")
boton_9.place(relx=0.65, rely=0.35, relwidth=0.15, relheight=0.35)
boton_9.config(activeforeground="#F50743", command=lambda:enviar_arduino(9))


imagen2=PhotoImage(file="control_lis\imagenes\png\extractor_0_1.png")
imagen3=PhotoImage(file="control_lis\imagenes\png\extractor_1_5.png")
#fondo2=Label(frame4, image=imagen2)
#fondo2=Label(frame4, image=imagen2)
#fondo2.place(x=20, y=110)
boton_10=Button(frame4, image=imagen2)
boton_10.place(x=20, y=110)
boton_10.config(background='#5E595F', activebackground='green', command=lambda:enviar_arduino(6))

boton_11=Button(frame4, text="CONECTAR", command=conectar)
boton_11.place(x=730, y=200, width=160, height=40)
boton_11.config(activeforeground="#30F705")


# ETIQUETAS ---------------------------------------------------------------------------------------
etiqueta_hora=ttk.Label(frame3, text="Hora")
etiqueta_hora.place(relx=0.02, rely=0.05, width=320, height=75)
etiqueta_hora.configure(style="estilo_6.TLabel")

etiqueta_1=ttk.Label(frame3, text="Temperatura sala :       ? º")
etiqueta_1.place(relx=0.75, rely=0.15, width=230, height=35)
etiqueta_1.configure(style="estilo_5.TLabel")

etiqueta_2=ttk.Label(frame3, text="Temperatura exterior : ? º")
etiqueta_2.place(relx=0.75, rely=0.55, width=230, height=35)
etiqueta_2.configure(style="estilo_5.TLabel")

etiqueta_3=ttk.Label(frame4, text="VENTILACIÓN SALA")
etiqueta_3.place(x=65, y=20, width=230, height=35)
etiqueta_3.configure(style="estilo_2.TLabel")

etiqueta_4=ttk.Label(frame4, text="COMUNICACIÓN")
etiqueta_4.place(x=730, y=20, width=230, height=35)
etiqueta_4.configure(style="estilo_2.TLabel")

etiqueta_5=ttk.Label(frame4, text="PUERTO:")
etiqueta_5.place(x=680, y=80)
etiqueta_5.configure(style="estilo_1.TLabel")

etiqueta_5=ttk.Label(frame4, text="VELOCIDAD:")
etiqueta_5.place(x=680, y=120)
etiqueta_5.configure(style="estilo_1.TLabel")

etiqueta_6=ttk.Label(frame4, text="ESTADO:")
etiqueta_6.place(x=680, y=160)
etiqueta_6.configure(style="estilo_1.TLabel")

etiqueta_7=ttk.Label(frame4, text="DESCONECTADO")
etiqueta_7.place(x=810, y=160)
etiqueta_7.configure(style="estilo_1.TLabel", background="red")

etiqueta_8=ttk.Label(frame4, text="Minuto inicio:")
etiqueta_8.place(x=20, y=405)
etiqueta_8.configure(style="estilo_1.TLabel")

etiqueta_9=ttk.Label(frame4, text="Minuto final:")
etiqueta_9.place(x=170, y=405)
etiqueta_9.configure(style="estilo_1.TLabel")

etiqueta_10=ttk.Label(frame5, text="Intensidad: --")
etiqueta_10.place(relx=0.85, rely=0.2)
etiqueta_10.configure(style="estilo_1.TLabel")

etiqueta_11=ttk.Label(frame5, text="Color:")
etiqueta_11.place(relx=0.85, rely=0.6)
etiqueta_11.configure(style="estilo_1.TLabel")

etiqueta_12=ttk.Label(frame4, text="ALUMBRADO")
etiqueta_12.place(x=425, y=20, width=230, height=35)
etiqueta_12.configure(style="estilo_2.TLabel")

etiqueta_13=ttk.Label(frame4, text="FOCO EXTERIOR:")
etiqueta_13.place(x=355, y=80)
etiqueta_13.configure(style="estilo_1.TLabel")

etiqueta_14=ttk.Label(frame4, text="Hora on")
etiqueta_14.place(x=380, y=145)
etiqueta_14.configure(style="estilo_1.TLabel")

etiqueta_15=ttk.Label(frame4, text="Hora off")
etiqueta_15.place(x=540, y=145)
etiqueta_15.configure(style="estilo_1.TLabel")

cuadro_color=tk.Canvas(frame5, width=45, height=20, background="black")
cuadro_color.place(relx=0.92, rely=0.58)


# BARRAS SEPRADORAS --------------------------------------------------------------------------------
separador_1=ttk.Separator(frame4, orient=VERTICAL)
separador_1.place(x=20, y=285, width=280, height=2)
separador_1.configure(style="separador_1.TSeparator")

separador_5=ttk.Separator(frame4, orient=VERTICAL)
separador_5.place(x=20, y=340, width=280, height=2)
separador_5.configure(style="separador_1.TSeparator")

separador_2=ttk.Separator(frame4, orient=HORIZONTAL)
separador_2.place(x=325, y=25, width=7, relheight=0.9)
separador_2.configure(style="separador_1.TSeparator")

separador_3=ttk.Separator(frame4, orient=HORIZONTAL)
separador_3.place(x=650, y=25, width=7, relheight=0.9)
separador_3.configure(style="separador_1.TSeparator")

separador_4=ttk.Separator(frame4, orient=VERTICAL)
separador_4.place(x=350, y=210, width=280, height=2)
separador_4.configure(style="separador_1.TSeparator")



# RADIOBUTONS --------------------------------------------------------------------------------------
boton_radio_1=Radiobutton(frame4, text="Automatico", variable=auto_man, value=1)
boton_radio_1.place(x=180, y=110)
boton_radio_1.config(background="#78637C", activebackground="#78637C", font=('Helvetica', 13), command=lambda:enviar_arduino(10))

boton_radio_2=Radiobutton(frame4, text="Manual", variable=auto_man, value=2)
boton_radio_2.place(x=180, y=140)
boton_radio_2.config(background="#78637C", activebackground="#78637C", font=('Helvetica', 13), command=lambda:enviar_arduino(11))

boton_radio_4=Radiobutton(frame4, text="Apagado auto", variable=auto_selec, value=1)
boton_radio_4.place(x=20, y=300)
boton_radio_4.config(background="#78637C", activebackground="#78637C", font=('Helvetica', 13), command=lambda:enviar_arduino(12))

boton_radio_5=Radiobutton(frame4, text="Función auto", variable=auto_selec, value=2)
boton_radio_5.place(x=20, y=355)
boton_radio_5.config(background="#78637C", activebackground="#78637C", font=('Helvetica', 13), command=lambda:enviar_arduino(13))

boton_radio_6=Radiobutton(frame4, text="Automatico", variable=foco_auto, value=1)
boton_radio_6.place(x=500, y=75)
boton_radio_6.config(background="#78637C", activebackground="#78637C", font=('Helvetica', 13), command=lambda:enviar_arduino(20))

boton_radio_7=Radiobutton(frame4, text="Manual", variable=foco_auto, value=2)
boton_radio_7.place(x=500, y=105)
boton_radio_7.config(background="#78637C", activebackground="#78637C", font=('Helvetica', 13), command=lambda:enviar_arduino(21))

boton_radio_8=Radiobutton(frame4, text="Automatico", variable=cartel_auto, value=1)
boton_radio_8.place(x=500, y=400)
boton_radio_8.config(background="#78637C", activebackground="#78637C", font=('Helvetica', 13), command=lambda:enviar_arduino(22))

boton_radio_9=Radiobutton(frame4, text="Manual", variable=cartel_auto, value=2)
boton_radio_9.place(x=500, y=430)
boton_radio_9.config(background="#78637C", activebackground="#78637C", font=('Helvetica', 13), command=lambda:enviar_arduino(23))


# COMBOBOX -----------------------------------------------------------------------------------------
lista_desp_1=ttk.Combobox(frame4, text="puerto", state="readonly")
lista_desp_1.place(x=810, y=80, width=100)
lista_desp_1['values']=('COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'COM10')
lista_desp_1.current(5) #con esto empieza en la posicion asignada
lista_desp_1.bind("<<ComboboxSelected>>", selec_lista_1) #crea una llamada a la funcion selec_lista_1 despues de selecionar una opción de la lista


lista_desp_2=ttk.Combobox(frame4, text="velocidad", state="readonly")
lista_desp_2.place(x=810, y=120, width=100)
lista_desp_2['values']=(2400, 4800, 9600, 19200)
lista_desp_2.current(2) #con esto empieza en la posicion asignada
lista_desp_2.bind("<<ComboboxSelected>>", selec_lista_2)


lista_desp_3=ttk.Combobox(frame4, text="tiempo_on", state="readonly")
lista_desp_3.place(x=210, y=303, width=90)
lista_desp_3['values']=(
    '1 minuto', '2 minutos', '3 minutos', '4 minutos', '5 minutos', '6 minutos', '7 minutos', '8 minutos', '9 minutos', '10 minutos', 
    '11 minutos', '12 minutos', '13 minutos', '14 minutos', '15 minutos', '16 minutos', '17 minutos', '18 minutos', '19 minutos', '20 minutos', 
    '21 minutos', '22 minutos', '23 minutos', '24 minutos', '25 minutos', '26 minutos', '27 minutos', '28 minutos', '29 minutos', '30 minutos',
    '31 minutos', '32 minutos', '33 minutos', '34 minutos', '35 minutos', '36 minutos', '37 minutos', '38 minutos', '39 minutos', '40 minutos',
    '41 minutos', '42 minutos', '43 minutos', '44 minutos', '45 minutos', '46 minutos', '47 minutos', '48 minutos', '49 minutos', '50 minutos',
    '51 minutos', '52 minutos', '53 minutos', '54 minutos', '55 minutos', '56 minutos', '57 minutos', '58 minutos', '59 minutos'
    )
lista_desp_3.current(4) #con esto empieza en la posicion asignada
lista_desp_3.bind("<<ComboboxSelected>>", selec_tiempos_extractor)


lista_desp_4=ttk.Combobox(frame4, text="m_inicio", state="readonly")
lista_desp_4.place(x=120, y=402, width=40)
lista_desp_4['values']=(
    '1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10 ', 
    '11 ', '12 ', '13 ', '14 ', '15 ', '16 ', '17 ', '18 ', '19 ', '20 ', 
    '21 ', '22 ', '23 ', '24 ', '25 ', '26 ', '27 ', '28 ', '29 ', '30 ',
    '31 ', '32 ', '33 ', '34 ', '35 ', '36 ', '37 ', '38 ', '39 ', '40 ',
    '41 ', '42 ', '43 ', '44 ', '45 ', '46 ', '47 ', '48 ', '49 ', '50 ',
    '51 ', '52 ', '53 ', '54 ', '55 ', '56 ', '57 ', '58 ', '59 '
    )
lista_desp_4.current(0) #con esto empieza en la posicion asignada
lista_desp_4.bind("<<ComboboxSelected>>", selec_tiempos_extractor)


lista_desp_5=ttk.Combobox(frame4, text="m_final", state="readonly")
lista_desp_5.place(x=260, y=402, width=40)
lista_desp_5['values']=(
    '1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10 ', 
    '11 ', '12 ', '13 ', '14 ', '15 ', '16 ', '17 ', '18 ', '19 ', '20 ', 
    '21 ', '22 ', '23 ', '24 ', '25 ', '26 ', '27 ', '28 ', '29 ', '30 ',
    '31 ', '32 ', '33 ', '34 ', '35 ', '36 ', '37 ', '38 ', '39 ', '40 ',
    '41 ', '42 ', '43 ', '44 ', '45 ', '46 ', '47 ', '48 ', '49 ', '50 ',
    '51 ', '52 ', '53 ', '54 ', '55 ', '56 ', '57 ', '58 ', '59 '
    )  
lista_desp_5.current(9) #con esto empieza en la posicion asignada
lista_desp_5.bind("<<ComboboxSelected>>", selec_tiempos_extractor)


lista_desp_6=ttk.Combobox(frame4, text="hora_on_foco", state="readonly")
lista_desp_6.place(x=360, y=170, width=40)
lista_desp_6['values']=(
    '00 ',
    '01 ', '02 ', '03 ', '04 ', '05 ', '06 ', '07 ', '08 ', '09 ', '10 ', 
    '11 ', '12 ', '13 ', '14 ', '15 ', '16 ', '17 ', '18 ', '19 ', '20 ', 
    '21 ', '22 ', '23 '
    )  
lista_desp_6.current(20) #con esto empieza en la posicion asignada
lista_desp_6.bind("<<ComboboxSelected>>", selec_tiempos_on_foco)


lista_desp_7=ttk.Combobox(frame4, text="minuto_on_foco", state="readonly")
lista_desp_7.place(x=420, y=170, width=40)
lista_desp_7['values']=(
    '00 ',
    '01 ', '02 ', '03 ', '04 ', '05 ', '06 ', '07 ', '08 ', '09 ', '10 ', 
    '11 ', '12 ', '13 ', '14 ', '15 ', '16 ', '17 ', '18 ', '19 ', '20 ', 
    '21 ', '22 ', '23 ', '24 ', '25 ', '26 ', '27 ', '28 ', '29 ', '30 ',
    '31 ', '32 ', '33 ', '34 ', '35 ', '36 ', '37 ', '38 ', '39 ', '40 ',
    '41 ', '42 ', '43 ', '44 ', '45 ', '46 ', '47 ', '48 ', '49 ', '50 ',
    '51 ', '52 ', '53 ', '54 ', '55 ', '56 ', '57 ', '58 ', '59 '
    )  
lista_desp_7.current(0) #con esto empieza en la posicion asignada
lista_desp_7.bind("<<ComboboxSelected>>", selec_tiempos_on_foco)


lista_desp_8=ttk.Combobox(frame4, text="hora_off_foco", state="readonly")
lista_desp_8.place(x=520, y=170, width=40)
lista_desp_8['values']=(
    '00 ',
    '01 ', '02 ', '03 ', '04 ', '05 ', '06 ', '07 ', '08 ', '09 ', '10 ', 
    '11 ', '12 ', '13 ', '14 ', '15 ', '16 ', '17 ', '18 ', '19 ', '20 ', 
    '21 ', '22 ', '23 '
    )  
lista_desp_8.current(23) #con esto empieza en la posicion asignada
lista_desp_8.bind("<<ComboboxSelected>>", selec_tiempos_off_foco)


lista_desp_9=ttk.Combobox(frame4, text="minuto_off_foco", state="readonly")
lista_desp_9.place(x=580, y=170, width=40)
lista_desp_9['values']=(
    '00 ',
    '01 ', '02 ', '03 ', '04 ', '05 ', '06 ', '07 ', '08 ', '09 ', '10 ', 
    '11 ', '12 ', '13 ', '14 ', '15 ', '16 ', '17 ', '18 ', '19 ', '20 ', 
    '21 ', '22 ', '23 ', '24 ', '25 ', '26 ', '27 ', '28 ', '29 ', '30 ',
    '31 ', '32 ', '33 ', '34 ', '35 ', '36 ', '37 ', '38 ', '39 ', '40 ',
    '41 ', '42 ', '43 ', '44 ', '45 ', '46 ', '47 ', '48 ', '49 ', '50 ',
    '51 ', '52 ', '53 ', '54 ', '55 ', '56 ', '57 ', '58 ', '59 '
    )  
lista_desp_9.current(30) #con esto empieza en la posicion asignada
lista_desp_9.bind("<<ComboboxSelected>>", selec_tiempos_off_foco)




#----------------------------------------------------------------------------------------------------
t = threading.Thread(target = hilo2)
t.start()
raiz.mainloop()