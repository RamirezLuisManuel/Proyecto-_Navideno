import network   # Para conectar a internet
from umqtt.simple import MQTTClient  # Para usar protocolo MQTT
from machine import Pin
import time
from time import sleep
import _thread

# Propiedades para conectar a un cliente MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "ESP32_Device_1"
MQTT_TOPIC_MAIN = "gds0643/lmrr/main"
MQTT_TOPIC_LDS = "gds0643/lmrr/lds"
MQTT_TOPIC_MOV = "gds0643/lmrr/mov"  # Nuevo tópico para activar/desactivar el sensor PIR
MQTT_PORT = 1883

# Función para conectar a WiFi
def conectar_wifi():
    print("Conectando...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('UTNG_GUEST', 'R3d1nv1t4d0s#UT')  # Cambia el SSID y contraseña
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.3)
    print("WiFi Conectada!")

# Variables globales
sensor_activado = False  # Variable para habilitar/deshabilitar el sensor PIR (inicia desactivado)

# Configurar el sensor PIR
pir_sensor = Pin(16, Pin.IN)

# Configurar pines de los LEDs secundarios
ledR1 = Pin(12, Pin.OUT)
ledR2 = Pin(33, Pin.OUT)

# Configurar LEDs principales
led_pins = [
    Pin(14, Pin.OUT),
    Pin(26, Pin.OUT),
    Pin(32, Pin.OUT),
    Pin(25, Pin.OUT),
]

###############################################################################
                            ## MOTOR A PASOS ##
# Configuración del motor paso a paso
IN1 = Pin(5, Pin.OUT)
IN2 = Pin(18, Pin.OUT)
IN3 = Pin(19, Pin.OUT)
IN4 = Pin(21, Pin.OUT)

# Secuencia de pasos para el motor 28BYJ-48
sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

def mover_motor(pasos, direccion):
    """
    Mueve el motor una cantidad específica de pasos.
    :param pasos: Número de pasos a mover.
    :param direccion: "adelante" para movimiento hacia adelante, "atras" para movimiento inverso.
    """
    if direccion == "adelante":
        secuencia = sequence
    elif direccion == "atras":
        secuencia = list(reversed(sequence))
    else:
        raise ValueError("Dirección debe ser 'adelante' o 'atras'.")
    
    for _ in range(pasos):
        for step in secuencia:
            for i in range(4):
                [IN1, IN2, IN3, IN4][i].value(step[i])
            time.sleep(0.002)  # Ajusta este valor para controlar la velocidad del motor
    
    # Apagar todas las bobinas para evitar calentamiento
    for pin in [IN1, IN2, IN3, IN4]:
        pin.value(0)

def motor_continuo():
    """
    Mantiene el motor en movimiento continuo.
    """
    pasos_180 = 180  # Aproximadamente 180 grados
    while True:
        mover_motor(pasos_180, "adelante")
        time.sleep(1)
        mover_motor(pasos_180, "atras")
        time.sleep(1)

# Hilo para motor continuo
def iniciar_motor_continuo():
    _thread.start_new_thread(motor_continuo, ())

###############################################################################

# Ciclo de LEDs principal (siempre activo)
def led_pulse_pattern():
    """
    Ciclo continuo del patrón principal de LEDs.
    """
    while True:
        for led in led_pins:
            # Apagar todos los LEDs
            for other_led in led_pins:
                other_led.off()
            # Encender el LED actual
            led.on()
            time.sleep(0.2)

# Hilo para manejar el patrón de LEDs siempre activo
def iniciar_led_principal():
    _thread.start_new_thread(led_pulse_pattern, ())

# Patrones para LEDs secundarios (activados por el sensor PIR)
def sensor_led_pattern():
    """
    Activa un patrón especial para los LEDs secundarios cuando el sensor PIR detecta movimiento.
    """
    while True:
        if sensor_activado and pir_sensor.value():
            print("Sensor PIR activado - Inicia patrón de LEDs secundarios")
            for _ in range(10):  # Repite el patrón 10 veces
                ledR1.value(1)
                ledR2.value(0)
                time.sleep(0.2)
                ledR1.value(0)
                ledR2.value(1)
                time.sleep(0.2)
            # Apagar LEDs secundarios después del patrón
            ledR1.value(0)
            ledR2.value(0)
        time.sleep(0.1)  # Pausa para evitar saturar el procesador

# Hilo para el patrón de LEDs secundarios
def iniciar_led_sensor():
    _thread.start_new_thread(sensor_led_pattern, ())

###############################################################################

# Función para manejar mensajes MQTT
def llegada_mensaje(topic, msg):
    global sensor_activado
    print(f"Mensaje recibido en {topic.decode()}: {msg.decode()}")
    if topic == b'gds0643/lmrr/mov':  # Control del sensor PIR
        if msg == b'true':
            print("Activando sensor PIR por MQTT")
            sensor_activado = True
        elif msg == b'false':
            print("Desactivando sensor PIR por MQTT")
            sensor_activado = False

# Función para subscribir al broker MQTT
def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                        user=MQTT_USER, password=MQTT_PASSWORD, keepalive=0)
    client.set_callback(llegada_mensaje)
    client.connect()
    client.subscribe(MQTT_TOPIC_MOV)  # Suscribirse al nuevo tópico
    print("Conectado a MQTT broker y suscrito a los tópicos.")
    return client

###############################################################################

# Configuración inicial
conectar_wifi()
client = subscribir()

# Inicia el patrón principal de LEDs, el motor continuo, y el patrón activado por sensor
iniciar_led_principal()
iniciar_motor_continuo()
iniciar_led_sensor()

# Loop principal para manejar MQTT
while True:
    try:
        client.check_msg()  # Procesa mensajes MQTT
    except OSError as e:
        print(f"Error de conexión MQTT: {e}")
        client = subscribir()  # Reintenta la conexión al broker MQTT
    time.sleep(0.1)

