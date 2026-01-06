# Tarea Planner

## Índice

## Introducción

Aplicación web desarrollada con Django para la gestión de tareas. Permite la creación de tareas, asignación a usuarios, trabajar en ellas, editarlas, entregarlas y evaluarlas.

Estas acciones dependen del tipo de usuario, distinguiendo profesores y alumnos.

## Arquitectura

El proyecto se divide en dos aplicaciones, config y 

## Modelado de datos

En este punto se definen los modelos utilizados en la aplicación, justificando las decisiones tomadas.

### User

El modelo de usuario hereda de AbstractUser, el modelo estándar de Django, lo que permite utilizar funcionalidades nativas como la autenticación, los permisos o la gestión de la sesión del usuario.

Se ha optado por no utilizar el campo username y en su lugar utilizar el correo electrónico como identificador único del usuario. Esta decisión está basada en el análisis del caso de uso de los usuarios, ya que los profesores o alumnos pueden compartir un mismo nombre y esta solución permite evitar el uso de formatos especiales como "{nombre}{1ª letra apellido 1}".

Para ello, se ha implementado un UserManager personalizado, que permite la correcta creación de usuarios al utilizar el email como identificador principal.

La clave primaria de este modelo es un identificador de tipo UUID, lo que mejora la seguridad con respecto a ids secuenciales y permite exponer estos identificadores en las urls de forma segura.

La distinción entre profesores y alumnos se hace a través de un parámetro, denominado "role". No es necesario crear distintos modelos para cada uno de estos roles debido a que no tienen propiedades distintas y las diferencias de comportamiento se gestionan a nivel de lógica de aplicación. 

### Task

En la aplicación se utiliza un único modelo de tarea. Después de estudiar los requerimientos técnicos a fondo (tareas individuales o grupales, evaluables y no evaluables) no se encontró una necesidad real que justifique la creación de modelos distintos, ya que habría compartido atributos y comportamiento. El uso de varios modelos habría introducido complejidad innecesaria, duplicidad de código y dificultad de mantenimiento, lo que se evita con un único modelo.

La clave principal de este modelo es también un campo UUID, por los mismos motivos listados anteriormente. Además, las tareas tienen una relación M2M con los usuarios, atrevés de la propiedad "assigned_to". Esto permite, al mismo tiempo, crear una tarea individual (relacionada con un único usuario) y grupal (relacionada con varios usuarios).

También tienen otra relación con la tabla de usuarios, ya que se guarda una referencia al usuario creador con la propiedad "created_by". Este campo, definido como FK, tiene el atributo de "on_delete=CASCADE", de modo que si se borra el usuario creador de la base de datos, se eliminan también sus tareas.

Un aspecto interesante de este modelo es la definición de propiedades adicionale mediante el uso de la etiqueta @property. Estas propiedades son inferidas a partir de otras, por ejemplo, una tarea es grupal si tiene más de un usuario asignado (la validación de esta propiedad se hace mediante la lógica de la aplicación en el momento de creación/edición). Estas propiedades son útiles en las vistas y formularios, pero no resulta necesario guardarlas en la base de datos.

## Base de datos

La base de datos utilizada en este proyecto es PostgreSQL. A continuación se detallan las caracteristicas de la misma.

### Psycopg2-binary

La conexión con la base de datos se hace mediante el paquete psycopg2-binary. La utilización del paquete *-binary permite evitar la compilación o uso de librerías adicionales, ya que está listo para ser usado. Esta versión de la librería se recomienda para el desarrollo y el testing, pero su uso se desaconseja en un entorno de producción, en el que se debería usar el paquete original.

Puedes leer más sobre las características y diferencias aquí https://pypi.org/project/psycopg2-binary/

### Configuración PostgreSQL

La configuración se detalla en el archivo settings.py, en el que se define la base de datos utilizada ("django.db.backends.postgresql") y los distintos parámetros para la conexión, como el nombre, usuario, contraseña o puerto. 

Los valores de estas propiedades se guardan en un archivo .env para evitar la exposición de datos sensibles, utilizando el paquete dotenv y la función load_dotenv. También sería válida la utilización de variables del sistema o del entorno.

## Migraciones



## Gitignore

El archivo .gitignore utilizado en este proyecto ha sido extraído de gitignore.io, configuradon específicamente para django.

## Créditos

El icono que se utiliza como logo/favicon en la aplicación está basado en 
<a href="https://www.flaticon.es/icono-gratis/agenda_16096501?term=agenda&page=1&position=56&origin=style&related_id=16096501" title="icono agenda">este icono creado por susannanovaIDR - Flaticon</a>.