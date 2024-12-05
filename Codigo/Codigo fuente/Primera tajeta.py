import network   # Para conectar a internet
from umqtt.simple import MQTTClient  # Para usar protocolo MQTT
from machine import Pin, PWM
from time import sleep
import time
import _thread
from hcsr04 import HCSR04 

# Propiedades para conectar a un cliente MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC_SEN = "gds0643/lmrr/sen" 
MQTT_PORT = 1883

# Función para conectar a WiFi
def conectar_wifi():
    print("Conectando...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('UTNG_GUEST', 'R3d1nv1t4d0s#UT')  # Cambia a el SID de la red (SSID, PASSWORD)
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("WiFi Conectada!")

# Variables globales
distancia_activa = False  # Control para el monitoreo de distancia

# Configuración del sensor ultrasónico, LEDs y buzzer
sensor = HCSR04(trigger_pin=15, echo_pin=4)
buzzer = PWM(Pin(19))
buzzer.duty(0)

# Crear objeto servo
servo = PWM(Pin(5))
servo2 = PWM(Pin(18))
servo.freq(50)
servo2.freq(50)

def set_servo_angle(angle):
    min_duty = 1638    
    max_duty = 8192    
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)

def set_servo_angle2(angle):
    min_duty = 1638    
    max_duty = 8192    
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo2.duty_u16(duty)

# Frecuencias de las notas para el tema de Mario (Hz)
NOTAS = {
    'do4': 262, 'do#4': 277, 're4': 294, 're#4': 311,
    'mi4': 330, 'fa4': 349, 'fa#4': 370, 'sol4': 392,
    'sol#4': 415, 'la4': 440, 'la#4': 466, 'si4': 494,
    'do5': 523, 'silencio': 0
}

# Duraciones de las notas (ms)
DURACION = {
    'negra': 200, 'corchea': 100, 'semicorchea': 50,
    'sil': 30, 'silg': 500
}


def emitir_nota(frecuencia, duracion, volumen=512):
    try:
        if frecuencia == 0:
            buzzer.duty(0)
        else:
            buzzer.freq(frecuencia)
            buzzer.duty(volumen)
        time.sleep_ms(duracion)
    finally:
        buzzer.duty(0)
        time.sleep_ms(DURACION['sil'])

def tocar_tema_subterraneo():
    secuencia = [
        (NOTAS['do4'], DURACION['corchea']), (NOTAS['do5'], DURACION['corchea']),
        (NOTAS['la4'], DURACION['corchea']), (NOTAS['la4'], DURACION['corchea']),
        (NOTAS['la#4'], DURACION['corchea']), (NOTAS['la#4'], DURACION['corchea']),
        (NOTAS['la4'], DURACION['corchea']), (NOTAS['la4'], DURACION['corchea']),
        (NOTAS['sol4'], DURACION['corchea']), (NOTAS['sol4'], DURACION['corchea']),
        (NOTAS['fa4'], DURACION['corchea']), (NOTAS['fa4'], DURACION['corchea']),
        (NOTAS['sol4'], DURACION['corchea']), (NOTAS['silencio'], DURACION['corchea']),
        (NOTAS['do4'], DURACION['corchea']), (NOTAS['do4'], DURACION['corchea']),
    ]
    for nota, dur in secuencia:
        emitir_nota(nota, dur)
    time.sleep_ms(DURACION['silg'])

def tocar_en_loop(veces=2):
    try:
        for _ in range(veces):
            tocar_tema_subterraneo()
            time.sleep_ms(500)
    finally:
        buzzer.duty(0)
# Monitorear distancia y controlar motor y sonidos
def monitorear_distancia():
    global distancia_activa
    
    while distancia_activa:
        try:
            distancia = sensor.distance_cm()  # Obtener la distancia en cm
            print(f"Distancia del Objeto: {distancia} cm")  # Imprimir la distancia en consola
            
            if distancia < 100:  # Si se detecta un objeto cercano
                # Mover los servos repetidamente
                for _ in range(5):  # Número de ciclos de movimiento
                    set_servo_angle(90)  # Mover el servo 1
                    set_servo_angle2(90)  # Mover el servo 2
                    time.sleep(0.5)  # Espera 0.5 segundos con los servos en esa posición
                    set_servo_angle(0)  # Mover el servo 1 a la posición inicial
                    set_servo_angle2(0)  # Mover el servo 2 a la posición inicial
                    time.sleep(0.5)  # Espera 0.5 segundos en la posición inicial
                tocar_en_loop()  # Emitir la melodía con el buzzer
                time.sleep(1)  # Espera de 1 segundo para estabilizar
            else:
                buzzer.duty(0)  # Detener el buzzer
                set_servo_angle(0)  # Detener el servo 1
                set_servo_angle2(0)  # Detener el servo 2
            sleep(0.1)
        except Exception as e:
            print("Error:", e)
            buzzer.duty(0)
            set_servo_angle(0)  # Detener servos si hay un error
            set_servo_angle2(0)
            sleep(0.1)


# Función para actualizar el estado del sensor
def llegada_mensaje(topic, msg):
    global distancia_activa
    print("Mensaje:", msg)
    if topic == b'gds0643/lmrr/sen':
        if msg == b'true':
            print("Activando sensor")
            distancia_activa = True
            _thread.start_new_thread(monitorear_distancia, ())
        elif msg == b'false':
            print("Desactivando sensor")
            distancia_activa = False

# Función para subscribir al broker y al topic
def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                        user=MQTT_USER, password=MQTT_PASSWORD, keepalive=0)
    client.set_callback(llegada_mensaje)
    client.connect()
    client.subscribe(MQTT_TOPIC_SEN)
    print("Conectado a %s, al topico %s" % (MQTT_BROKER, MQTT_TOPIC_SEN))
    return client

# Conectar a WiFi
conectar_wifi()
 
# Subscripción a un broker MQTT
client = subscribir()

while True:
    client.check_msg()  # Procesar mensajes MQTT
    sleep(0.1)


