# python-proyecto-1

# Diseño de un programa de pedido para Pizzerías.

## DataBase:
! [DataBase Image](https://raw.githubusercontent.com/AndresRCA/python-proyecto-1/master/DB/DB_Schema.png)

En la figura anterior se puede observar las tablas que componen la base de datos a usar en
el programa, se trato de mantener la separación de datos y relaciones entre tablas, se
crearon las relaciones a través de llaves foráneas para mantener una relación segura y sin
errores al momento de realizar una operación de inserción o actualización en las tablas.

## Clases:

Se crearon dos clases llamadas Pizza y Order que sirven como modelos de sus tablas
respectivas en la base de datos. 


## Main.py:

En el programa principal se tiene un menú con tres opciones:
### Cargar ordenes.
### Generar resumen.
### Salir.

## excepciones y validación de datos:

Las excepciones son enteramente manejadas por la base de datos SQLite, con el uso de
llaves foráneas y restricciones tales como valores no nulos dentro de una columna, se puede
cancelar una orden o pizza que contenga algún valor invalido al momento de insertar
registros en la base de datos.
