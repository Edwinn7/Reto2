# Reto2
Reto 2 - Talento B

Este proyecto es una aplicación web simple que permite a los usuarios crear y administrar cuentas bancarias. Está construido utilizando el marco web Flask y la base de datos MySQL.

## Características

- Los usuarios pueden crear una nueva cuenta bancaria.
- Los usuarios pueden ver el saldo de sus cuentas bancarias.
- Los usuarios pueden transferir dinero entre sus cuentas bancarias.
- Los usuarios pueden cancelar sus cuentas bancarias.

## Tecnologías utilizadas

- Flask
- MySQL

## Pasos para la ejecución

Sigue los siguientes pasos para ejecutar el proyecto:

1. Abre una terminal o línea de comandos en tu sistema operativo y navega hasta la carpeta raíz del proyecto.
2. Ejecuta el siguiente comando para crear un entorno virtual (virtual environment):
   - En Windows:
     ```
     python -m venv venv
     ```
   - En macOS/Linux:
     ```
     python3 -m venv venv
     ```
3. Activa el entorno virtual:
   - En Windows:
     ```
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```
     source venv/bin/activate
     ```
4. Instala las dependencias del proyecto ejecutando el siguiente comando en la ruta raíz del proyecto:
   ```
   pip install -r requirements.txt
   ```
5. Crea la base de datos utilizando el archivo `bancodb_.txt` y establece los parámetros de conexión en el archivo `app.py`.
6. Después de instalar las dependencias y configurar la base de datos, ejecuta la aplicación con el siguiente comando:
   ```
   python app.py
     ```
