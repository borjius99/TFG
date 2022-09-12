## Datos

Título: Trazabilidad de Fake News y Deepfakes a través de Blockchain y contratos inteligentes
Estudiante: Borja Alonso Sobral
Dirección: Tiago M. Fernández Caramés, Paula Fraga Lamas


## RESUMEN

El código ubicado en este repositorio es el perteneciente a la aplicación web del TFG. En él se encuentra: el manejo de usuarios, creación de publicaciones, el HTML de las vistas correspondientes y los diferentes sistemas de reputación y votación mencionados en la memoria. Toda la implementación explicada en ella, se encuentra en los diferentes archivos del repositorio.

## Estructura de carpetas

 - FakeNews: Carpeta del proyecto.
	 - FakeApp: Carpeta de la App.
	 - FakeNews: Carpeta con archivos de configuración del proyecto.
	 - FakeApp_userprofile
	 - compiled_code.json: Fichero creado al compilar el contrato.
	 - db.sqlite3: Base de datos.
	 - manage.py: Script para la creación de aplicaciones, trabajar con bases de datos y empezar el desarrollo del servidor web.
	 - pushContract.py: Script para desplegar el contrato
	 - script.sh: Script para la creación del usuario administrador de la aplicación


Dentro de la carpeta FakeApp se encuentran los ficheros y carpetas correspondientes a la aplicación, entre ellos se puede destacar:

	- templates: carpeta en la que se ubican los HTMLs de las vistas
	- static: carpeta donde se ubica el CSS utilizado
	- contract.sol: contrato utilizado en la aplicación
	- forms.py: formularios utilzados para Iniciar Sesión y Registrarse
	- functions.py: funciones auxiliares utilizadas en las vistas
	- models.py: modelos utilizados para la base de datos
	- views.py vistas pertenecientes a la aplicación

## USO

1.- Primeramente, hay que crear un usuario utilizando "script.sh" que se encuentra en el directorio "/FakeNews", cambiando los valores ('Email', 'Nombre_Usuario', 'URL', 'Wallet','Contraseña') por los suyos. Lo importante en este caso es el Email y la contraseña para poder iniciar sesión.

2.- Antes de iniciar el servidor, asegurarse de que esté instalado python3 junto con las librerías utilizadas en el código: web3,
	json, solcx, pandas, string, jsonfield, re, datetime.

2.- Instalar Ganache y desplegar una blockchain.

3.- En el fichero /FakeNews/pushContract.py, introducir en las variables "private_key" y "admin_address", la clave privada y la dirección de una cuentra registrada en la blockchain, será la cuenta administradora. La clave debe empezar por '0x'. Luego ejecutar en el directorio "/FakeNews" para desplegar el contrato:


	python3 pushContract.py


4.- Para iniciar el servidor, en el fichero /FakeNews/FakeApp/views.py introducir las variables "private_key", "admin_address" y "contract_address". Las dos primeras se corresponden a las mencionadas anteriormente, y la última a la dirección del contrato desplegado. Una vez hecho esto, ejecutar en el directorio "/FakeNews":


	python3 manage.py runserver



5.- La URL de la página web se encuentra en "http://127.0.0.1:8000/FakeApp/"

6.- Una vez hecho esto, si todo fue bien, se puede empezar a registrar usuarios, siempre y cuando su dirección sea una de las proporcionadas por Ganacge, y crear publicaciones.

## Reinicio

Si en algún momento se necesita reiniar el sistema para volver a empezar.

	1.- Se borra la blockchain y se crea otra en Ganache
	2.- Se ejecuta el "script.sh"
	3.- Se despliega el contrato

## Pruebas

Los ficheros pruebaNews.py y pruebaOrg.py son los utilizados en la explicación de la memoria para comprobar las funciones del contrato.
