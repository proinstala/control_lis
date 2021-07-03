
//funciona con python lis_aplicacion_com_1_5_beta8.py



/*
-----------byte enviados comunicacion pantalla-------------------------------
Nota: la posicion de los bit de cada byte esta invertido respecto a la posicion que tiene en lis_aplicacion
byte salidas_1:
0. extractor aire.
1. luz izquierda.
2. luz derecha.
3. luz trastero.
4. foco exterior
5. cartel luminoso
6. tira rgb led
7. libre.

byte automatico_1:
0. extractor aire.
1. extrator tipo auto.
2. libre.
3. libre.
4. libre.
5. libre.
6. foco exterior.
7. cartel luminoso.

 */

#include <EEPROM.h>
byte memo0 = 0; //automatico_1
byte memo1 = 1; //rgb_intensidad_led
byte memo2 = 2; //rgb_red
byte memo3 = 3; //rgb_green
byte memo4 = 4; //rgb_blue
byte memo5 = 5; //t_extractor_temp_off
byte memo6 = 6; //t_extractor_auto_on
byte memo7 = 7; //t_extractor_auto_off
byte memo8 = 8; //t_foco_ext_auto_on_h 
byte memo9 = 9; //t_foco_ext_auto_on_m
byte memo10 = 10; //t_foco_ext_auto_off_h 
byte memo11 = 11; //t_foco_ext_auto_off_m 
byte memo12 = 12; // libre 
byte memo13 = 13; // libre 
byte memo14 = 14; // libre 
byte memo15 = 15; // libre 


String msg;
String dato_rx;
String dato;
String dato1_rx;
String dato2_rx;
String dato3_rx;
String dato4_rx;

int direccion_rx;
int dato1;
int dato2;
int dato3;

byte direccion_guardado;
byte inicio_conexion_control_lis;

byte libre;

int direccion_tx = 1;
int checksun_tx;

float tiempo;
float crono1;
float crono2;
byte sm_01;
byte sm_02;
int cont1;
int cont2;

int temperatura1;
int temperatura2;
int temperatura3;
int entradas;

byte temperatura_sala;
byte temperatura_ext;

byte entradas_1;
byte salidas_1;
byte automatico_1;

byte t_extractor_temp_off;
byte t_extractor_auto_on;
byte t_extractor_auto_off;

byte t_foco_ext_auto_on_h;
byte t_foco_ext_auto_on_m;
byte t_foco_ext_auto_off_h;
byte t_foco_ext_auto_off_m;

byte rgb_red;             
byte rgb_green;
byte rgb_blue;
byte rgb_intensidad_led;

byte valor_rojo;        //valor mapeado
byte valor_verde;       //valor mapeado
byte valor_azul;        //valor mapeado
byte valor_intensidad;  //valor mapeado

byte estado_salida_extractor = false;
byte estado_salida_luz_izquierda = false;
byte estado_salida_luz_derecha = false;
byte estado_salida_luz_trastero = false;
byte estado_salida_foco_exterior = false;
byte estado_salida_cartel_luminoso = false;
byte estado_salida_rgb_led = false;


byte py_pulsador_extractor = false;
byte py_pulsador_extractor_auto = false;
byte py_pulsador_luz_izquierda = false;
byte py_pulsador_luz_derecha = false;
byte py_pulsador_luz_trastero = false;
byte py_pulsador_foco_exterior = false;
byte py_pulsador_cartel_luminoso = false;
byte py_pulsador_apagar_todas = false;
byte py_pulsador_rgb_led = false;
byte py_pulsador_rgb_mas = false;
byte py_pulsador_rgb_menos = false;


//-------------------------- entradas / salidas -----------------------------------------

#define extractor_aire 3
#define luz_izquierda 4
#define luz_derecha 5
#define luz_trastero 7
#define foco_exterior 8
#define tira_rgb_led 6
#define led_red 9
#define led_green 10
#define led_blue 11


void setup(){
  Serial.begin(9600);

  pinMode(extractor_aire, OUTPUT);
  pinMode(luz_izquierda, OUTPUT);
  pinMode(luz_derecha, OUTPUT);
  pinMode(luz_trastero, OUTPUT);
  pinMode(foco_exterior, OUTPUT);
  pinMode(tira_rgb_led, OUTPUT);
  pinMode(led_red, OUTPUT);
  pinMode(led_green, OUTPUT);
  pinMode(led_blue, OUTPUT);

  automatico_1 = EEPROM.read(memo0);
  rgb_intensidad_led = EEPROM.read(memo1);
  rgb_red = EEPROM.read(memo2);
  rgb_green = EEPROM.read(memo3);
  rgb_blue = EEPROM.read(memo4);
  t_extractor_temp_off = EEPROM.read(memo5);
  t_extractor_auto_on = EEPROM.read(memo6);
  t_extractor_auto_off = EEPROM.read(memo7);
  t_foco_ext_auto_on_h = EEPROM.read(memo8);
  t_foco_ext_auto_on_m = EEPROM.read(memo9);
  t_foco_ext_auto_off_h = EEPROM.read(memo10);
  t_foco_ext_auto_off_m = EEPROM.read(memo11);
}

void loop(){
  tiempo = millis();
  tiempo = tiempo / 1000;

  sm_01 = false;
  if(tiempo >= crono1 +0.1){
    sm_01 = true;
    crono1 = tiempo;
    cont1++;
  }
   
  sm_02 = false;
  if(tiempo >= crono2 +0.2){
    sm_02 = true;
    crono2 = tiempo;
    cont2++;
  }

//------- CONTROL SALIDAS-----------------------------------

  //EXTRACTOR DE AIRE
  if(estado_salida_extractor == false && py_pulsador_extractor == true){
    digitalWrite(extractor_aire, HIGH);
    estado_salida_extractor = true;
    py_pulsador_extractor = false;
    bitWrite(salidas_1, 0, 1);
  }
  if(estado_salida_extractor == true && py_pulsador_extractor == true){
    digitalWrite(extractor_aire, LOW);
    estado_salida_extractor = false;
    py_pulsador_extractor = false;
    bitWrite(salidas_1, 0, 0);
  }

  //LUZ IZQUIERDA
  if(estado_salida_luz_izquierda == false && py_pulsador_luz_izquierda == true){
    digitalWrite(luz_izquierda, HIGH);
    estado_salida_luz_izquierda = true;
    py_pulsador_luz_izquierda = false;
    bitWrite(salidas_1, 1, 1);
  }
  if(estado_salida_luz_izquierda == true && py_pulsador_luz_izquierda == true){
    digitalWrite(luz_izquierda, LOW);
    estado_salida_luz_izquierda = false;
    py_pulsador_luz_izquierda = false;
    bitWrite(salidas_1, 1, 0);
  }
  
  //LUZ DERECHA
  if(estado_salida_luz_derecha == false && py_pulsador_luz_derecha == true){
    digitalWrite(luz_derecha, HIGH);
    estado_salida_luz_derecha = true;
    py_pulsador_luz_derecha = false;
    bitWrite(salidas_1, 2, 1);
  }
  if(estado_salida_luz_derecha == true && py_pulsador_luz_derecha == true){
    digitalWrite(luz_derecha, LOW);
    estado_salida_luz_derecha = false;
    py_pulsador_luz_derecha = false;
    bitWrite(salidas_1, 2, 0);
  }

  //LUZ TRASTERO
  if(estado_salida_luz_trastero == false && py_pulsador_luz_trastero == true){
    digitalWrite(luz_trastero, HIGH);
    estado_salida_luz_trastero = true;
    py_pulsador_luz_trastero = false;
    bitWrite(salidas_1, 3, 1);
  }
  if(estado_salida_luz_trastero == true && py_pulsador_luz_trastero == true){
    digitalWrite(luz_trastero, LOW);
    estado_salida_luz_trastero = false;
    py_pulsador_luz_trastero = false;
    bitWrite(salidas_1, 3, 0);
  }

  //FOCO EXTERIOR
  if(estado_salida_foco_exterior == false && py_pulsador_foco_exterior == true){
    digitalWrite(foco_exterior, HIGH);
    estado_salida_foco_exterior = true;
    py_pulsador_foco_exterior = false;
    bitWrite(salidas_1, 4, 1);
  }
  if(estado_salida_foco_exterior == true && py_pulsador_foco_exterior == true){
    digitalWrite(foco_exterior, LOW);
    estado_salida_foco_exterior = false;
    py_pulsador_foco_exterior = false;
    bitWrite(salidas_1, 4, 0);
  }

  //TIRA LED RGB
  if(estado_salida_rgb_led == false && py_pulsador_rgb_led == true){
    valor_intensidad = map(rgb_intensidad_led, 0, 100, 0, 255);
    valor_rojo = map(rgb_red, 0, 100, 0, 255);
    valor_verde = map(rgb_green, 0, 100, 0, 255);
    valor_azul = map(rgb_blue, 0, 100, 0, 255);
    
    analogWrite(tira_rgb_led, valor_intensidad); //intensidad tira rgb led
    analogWrite(led_red, valor_rojo); //led rojo
    analogWrite(led_green, valor_verde); //led verde
    analogWrite(led_blue, valor_azul); //led azul
    
    estado_salida_rgb_led = true;
    py_pulsador_rgb_led = false;
    bitWrite(salidas_1, 6, 1);
  }
  if(estado_salida_rgb_led == true && py_pulsador_rgb_led == true){
    analogWrite(tira_rgb_led, 0); //intensidad tira rgb led
    analogWrite(led_red, 0); //led rojo
    analogWrite(led_green, 0); //led verde
    analogWrite(led_blue, 0); //led azul
    
    estado_salida_rgb_led = false;
    py_pulsador_rgb_led = false;
    bitWrite(salidas_1, 6, 0);
  }

  if(py_pulsador_rgb_mas == true){
    if(rgb_intensidad_led < 100) rgb_intensidad_led = rgb_intensidad_led +5;
    py_pulsador_rgb_mas = false;
  }
  if(py_pulsador_rgb_menos == true){
    if(rgb_intensidad_led > 0) rgb_intensidad_led = rgb_intensidad_led -5;
    py_pulsador_rgb_menos = false;
  }



  //ENVIAR Y RECIVIR DATOS
  if(sm_02 == true){
    enviar_datos();
    
    if(inicio_conexion_control_lis == false){ //barrido por todas las direcciones al inicio de la conexion con programa control sala lis
      direccion_tx ++;
      if(direccion_tx == 4) inicio_conexion_control_lis = true;
    }
  }

  if(sm_01 == true){
    recivir_datos();
  }

  
}//fin void loop -------------------------------------------------------------------

void guardado_eeprom(byte direccion_guardado){
  if(direccion_guardado == 1){
    EEPROM.write(memo0, automatico_1); 
    EEPROM.write(memo1, rgb_intensidad_led);
    EEPROM.write(memo2, rgb_red);
    EEPROM.write(memo3, rgb_green);
    EEPROM.write(memo4, rgb_blue);
    EEPROM.write(memo5, t_extractor_temp_off);
    EEPROM.write(memo6, t_extractor_auto_on);
    EEPROM.write(memo7, t_extractor_auto_off);
    EEPROM.write(memo8, t_foco_ext_auto_on_h);
    EEPROM.write(memo9, t_foco_ext_auto_on_m);
    EEPROM.write(memo10, t_foco_ext_auto_off_h);
    EEPROM.write(memo11, t_foco_ext_auto_off_m);
  }

  if(direccion_guardado == 2){
    EEPROM.write(memo5, t_extractor_temp_off);
    EEPROM.write(memo6, t_extractor_auto_on);
    EEPROM.write(memo7, t_extractor_auto_off);
  }

  if(direccion_guardado == 3){
    EEPROM.write(memo1, rgb_intensidad_led);
    EEPROM.write(memo2, rgb_red);
    EEPROM.write(memo3, rgb_green);
    EEPROM.write(memo4, rgb_blue);
  }

  if(direccion_guardado == 4){
    EEPROM.write(memo8, t_foco_ext_auto_on_h);
    EEPROM.write(memo9, t_foco_ext_auto_on_m);
    EEPROM.write(memo10, t_foco_ext_auto_off_h);
    EEPROM.write(memo11, t_foco_ext_auto_off_m);
  }
  
}

void leer_eeprom(byte direccion_carga){
  if(direccion_carga == 1){
    automatico_1 = EEPROM.read(memo0);
    rgb_intensidad_led = EEPROM.read(memo1);
    rgb_red = EEPROM.read(memo2);
    rgb_green = EEPROM.read(memo3);
    rgb_blue = EEPROM.read(memo4);
    t_extractor_temp_off = EEPROM.read(memo5);
    t_extractor_auto_on = EEPROM.read(memo6);
    t_extractor_auto_off = EEPROM.read(memo7);
    t_foco_ext_auto_on_h = EEPROM.read(memo8);
    t_foco_ext_auto_on_m = EEPROM.read(memo9);
    t_foco_ext_auto_off_h = EEPROM.read(memo10);
    t_foco_ext_auto_off_m = EEPROM.read(memo11);
  }

  if(direccion_carga == 2){
    t_extractor_temp_off = EEPROM.read(memo5);
    t_extractor_auto_on = EEPROM.read(memo6);
    t_extractor_auto_off = EEPROM.read(memo7);
  }

  if(direccion_carga == 3){
    rgb_intensidad_led = EEPROM.read(memo1);
    rgb_red = EEPROM.read(memo2);
    rgb_green = EEPROM.read(memo3);
    rgb_blue = EEPROM.read(memo4);
  }

  if(direccion_carga == 4){
    t_foco_ext_auto_on_h = EEPROM.read(memo8);
    t_foco_ext_auto_on_m = EEPROM.read(memo9);
    t_foco_ext_auto_off_h = EEPROM.read(memo10);
    t_foco_ext_auto_off_m = EEPROM.read(memo11);
  }

  inicio_conexion_control_lis = false;
  
}




void recivir_datos(){
  msg = "";
  if(Serial.available()){
    delay(15); //intentar bajar esto
    while(Serial.available() > 0){
      msg += (char)Serial.read();
    }
    dato_rx = msg;   
  }
  
  if(dato_rx.startsWith("#@99@", 0) && dato_rx.endsWith("$")){
    dato = dato_rx.substring(5);
    dato1_rx = dato.substring(0,dato.indexOf("@")); //direccion
    dato = dato.substring(dato.indexOf("@")+1);
    dato2_rx = dato.substring(0,dato.indexOf("@")); //dato1
    dato = dato.substring(dato.indexOf("@")+1);
    dato3_rx = dato.substring(0,dato.indexOf("@")); //dato2
    dato = dato.substring(dato.indexOf("@")+1);
    dato4_rx = dato.substring(0,dato.indexOf("$")); //dato3

    direccion_rx = dato1_rx.toInt();
    dato1 = dato2_rx.toInt();
    dato2 = dato3_rx.toInt();
    dato3 = dato4_rx.toInt();
    dato_rx = "0";
  }

  if(direccion_rx == 1){ //pulsadores
    if(dato1 == 1) py_pulsador_apagar_todas = true;
    if(dato1 == 2) py_pulsador_luz_izquierda = true;
    if(dato1 == 3) py_pulsador_luz_derecha = true;
    if(dato1 == 4) py_pulsador_luz_trastero = true;
    if(dato1 == 5) py_pulsador_foco_exterior = true;
    if(dato1 == 6) py_pulsador_extractor = true;
    if(dato1 == 7){py_pulsador_rgb_led = true; direccion_tx=3;}
    if(dato1 == 8){py_pulsador_rgb_mas = true; direccion_tx=3;}
    if(dato1 == 9){py_pulsador_rgb_menos = true; direccion_tx=3;}
  }

  if(direccion_rx == 5){
    rgb_red = dato1;
    rgb_green = dato2;
    rgb_blue = dato3;
    
    direccion_tx=3;
  }
  
  if(direccion_rx == 10){ //byte automatico_1
    bitWrite(automatico_1, dato1, dato2); 
  }

  if(direccion_rx == 11){ //tiempos extractor automatico
    t_extractor_temp_off=dato1;
    t_extractor_auto_on=dato2;
    t_extractor_auto_off=dato3;

    direccion_tx=2;
  }

  if(direccion_rx == 12){ //tiempos foco exterior automatico on
    t_foco_ext_auto_on_h=dato1;
    t_foco_ext_auto_on_m=dato2;

    direccion_tx=4;
  }

  if(direccion_rx == 13){ //tiempos foco exterior automatico off
    t_foco_ext_auto_off_h=dato1;
    t_foco_ext_auto_off_m=dato2;

    direccion_tx=4;
  }
  
  if(direccion_rx == 20){
    guardado_eeprom(dato1);
  }

  if(direccion_rx == 21){
    leer_eeprom(dato1);
  }
  
  direccion_rx = 0;
  dato1 = 0;
  dato2 = 0;
  dato3 = 0;
}


void enviar_datos() {
  checksun_tx = direccion_tx + temperatura_sala;
  if(direccion_tx==1){
    Serial.print(direccion_tx);
    Serial.print("@");
    Serial.print(temperatura_sala);
    Serial.print("@");
    Serial.print(temperatura_ext);
    Serial.print("@");
    Serial.print(libre);
    Serial.print("@");
    Serial.print(automatico_1);
    Serial.print("@");
    Serial.print(entradas_1);
    Serial.print("@");
    Serial.print(salidas_1);
    Serial.print("@");
    Serial.println(checksun_tx);
  }

  checksun_tx = direccion_tx + t_extractor_temp_off;
  if(direccion_tx==2){
    Serial.print(direccion_tx);
    Serial.print("@");
    Serial.print(t_extractor_temp_off);
    Serial.print("@");
    Serial.print(t_extractor_auto_on);
    Serial.print("@");
    Serial.print(t_extractor_auto_off);
    Serial.print("@");
    Serial.print(libre);
    Serial.print("@");
    Serial.print(libre);
    Serial.print("@");
    Serial.print(libre);
    Serial.print("@");
    Serial.println(checksun_tx);
  }

  checksun_tx = direccion_tx + rgb_red;
  if(direccion_tx==3){
    Serial.print(direccion_tx);
    Serial.print("@");
    Serial.print(rgb_red);
    Serial.print("@");
    Serial.print(rgb_green);
    Serial.print("@");
    Serial.print(rgb_blue);
    Serial.print("@");
    Serial.print(rgb_intensidad_led);
    Serial.print("@");
    Serial.print(libre);
    Serial.print("@");
    Serial.print(salidas_1);
    Serial.print("@");
    Serial.println(checksun_tx);
  }

  checksun_tx = direccion_tx + t_foco_ext_auto_on_h;
  if(direccion_tx==4){
    Serial.print(direccion_tx);
    Serial.print("@");
    Serial.print(t_foco_ext_auto_on_h);
    Serial.print("@");
    Serial.print(t_foco_ext_auto_on_m);
    Serial.print("@");
    Serial.print(t_foco_ext_auto_off_h);
    Serial.print("@");
    Serial.print(t_foco_ext_auto_off_m);
    Serial.print("@");
    Serial.print(automatico_1);
    Serial.print("@");
    Serial.print(salidas_1);
    Serial.print("@");
    Serial.println(checksun_tx);
  }

  //direccion por defecto despues del barrido de direcciones al inicio de conexion con control_sala_lis
  if(inicio_conexion_control_lis == true) direccion_tx = 1; 
  
  checksun_tx = 0;
  
}
