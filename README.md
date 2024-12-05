# Personaje Navideño
## Nombre del Personaje
### Lock
<img width="300" src="https://github.com/RamirezLuisManuel/Proyecto-_Navideno/blob/main/Evidencias/Fotos%20y%20videos%20de%20Funcionamiento/Lock_1.png?raw=true"/><br>

## Integrantes
### Grupo: GDS0643
|Nombres|Apellido Materno| Apellido Paterno|
|Cesar Abraham|López |Aguilar|


### Descripción
#### Nombre de personaje: Lock
#### Atuendo: Pantalón, camisa roja y mascara de diablito
#### Escenario: Bañera decorada con escarcha y leds
#### Funcionalidad:
El sensor ultrasónico, acciona un patrón de movimientos de los servos así como una melodía en el zumbador, esto ocurre cuando un individuo se coloca a un metro o menos de distancia del personaje.
El sensor Pir, acciona 2 leds que se encuentran en las manos del personaje.
Los leds que decoran la bañera tienen un patrón donde encienden y apagan uno tras otro independiente de la demás funcionalidad.
El motor a pasos gira la cabeza un aproximado de 180 grados, esta acción se ejecuta todo el tiempo independientemente de las demás funciones.

## Materiales utilizados
|Software|Versión|
|--|--|--|--|
|Thonny|4.1.6|


## Software a utilizar
|Software|Versión|
|--|--|
|Thonny|4.1.6|
|Node-Red|4.0.5|



#### Video de funcionalidad.
#### [Codigo fuente.](https://github.com/RamirezLuisManuel/Proyecto-_Navideno/tree/main/Codigo)

### Bocetaje en dibujo.
<img width="600" src="https://github.com/RamirezLuisManuel/Proyecto-_Navideno/blob/main/Evidencias/Fotos%20y%20videos%20de%20Elaboracion/boceto.jpg?raw=true"/><br>


## Arquitectura.
Por la cantidad de componentes que implementamos, una sola tarjeta ESP32 no soportaba así que dividimos los componentes entre dos ESP32.

### Primer tarjeta:
En la primer ESP32, conectamos un sensor HSCR-04, 2 servomotores y un zumbador, inicialmente esto no seria así, pero por falta de potencia tuvimos que separar los servomotores del motor a pasos.
El sensor va conectado a los pines 15(trigger), 4(echo) y para corriente va a negativo y 3V
El zumbador va conectado al pin 19 y para corriente va a negativo y 3V.
Los servomotores van a al pin 5, y 18 así como también a negativo y 3V.

<img width="500" src="https://github.com/RamirezLuisManuel/Proyecto-_Navideno/blob/main/Arquitectura_tarjeta_1.png?raw=true"/><br>
### Segunda tarjeta:
En la segunda ESP32, conectamos un sensor Pir, un motor a pasos y 6 leds.
El sensor Pir va al pin 16, así como a negativo y 3V.
Los leds van a los pines 12, 33, 14, 26, 32, 25.
El motor va a los pines IN1: 5, IN2: 18, IN3: 19, IN4: 21 además va a negativo y 5V.

<img width="500" src="https://github.com/RamirezLuisManuel/Proyecto-_Navideno/blob/main/Arquitectura_tarjeta_2.png?raw=true"/><br>


## [Flujo de Node-red.](https://github.com/RamirezLuisManuel/Proyecto-_Navideno/tree/main/Flujo%20Node_Red)
Consta de dos botones switch en node-red , uno para accionar el sensor ultrasónico, y el otro botón para accionar el sensor Pir.

<img width="500" src="https://github.com/RamirezLuisManuel/Proyecto-_Navideno/blob/main/Flujo_node.png?raw=true"/><br>

<img width="500" src="https://github.com/RamirezLuisManuel/Proyecto-_Navideno/blob/main/Botones_node.png?raw=true"/><br>
  
## [Curso JavaScript NetAcad.](https://github.com/RamirezLuisManuel/Proyecto-_Navideno/tree/main/Curso%20JavaScript%20NetAcad)
A lo largo de este curso, he experimentado un crecimiento exponencial en mis habilidades de programación con JavaScript. Los ejercicios realizados me han ayudado a conoer los conceptos teóricos, y también desarrollar un pensamiento lógico y algorítmico más sólido. Estoy seguro de que los conocimientos adquiridos me brindarán una ventaja competitiva en el ámbito laboral, permitiéndome abordar desafíos complejos y proponer soluciones innovadoras.

## Coevaluación de mi compañero.
De manera general mi compañero, a sido un gran compañero de trabajo ya que nos comunicamos muy bien y trabajamos bien en equipo, pero aun así hay cosas que se podrían mejorar, ya que en ocasiones, ambos podemos estar en desacuerdo en alguno aspectos, y a mi compañero le gusta que se haga lo que él dice, además, de que si es bueno para la escuela, es decir que si es inteligente y dedicado, a veces carga mucho el trabajo a los demás, o en este caso a mi, con esto no me refiero a que el no haya hecho nada, al contrario el trabajo muy duro, pero creo que en algunas ocasiones, a mi en lo personal me ocurrieron situaciones que no tenia previstas y  me hubiera gustado recibir un mayor apoyo con mi compañero para poder solucionar esos asuntos ya que si me tomaron bastante tiempo, aun asi estoy satisfecho con el trabajo de mi compañero.

En cuanto a puntualidad responsabilidad y demás cosas mi compañero, siempre mostro compromiso con el proyecto qya que por lo regular si cumplía con lo decía que iba hacer. 

