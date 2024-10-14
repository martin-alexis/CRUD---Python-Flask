# Aplicación CRUD con Python y Flask

Esta es una aplicación CRUD (Create, Read, Update, Delete) desarrollada con Python y Flask. La aplicación consta de dos tablas principales:

### PERSONAS
- **Descripción**: Almacena los registros de las personas.

### USUARIOS
- **Descripción**: Almacena los usuarios que pueden obtener el token de acceso a los endpoints.

## Documentación en Postman

La documentación de la API está disponible en Postman, donde puedes probar todos los endpoints de la aplicación y la instrucciones para su uso.

[Documentación de la API en Postman](https://documenter.getpostman.com/view/38249888/2sAXxTbq5z)

# Guía de Implementación de la Aplicación CRUD

## Pasos de Implementación

1. **Instalación de dependencias**
   ```
   pip install -r requirements.txt
   ```

2. **Configuración del archivo .env**
   Cree un archivo `.env` en el directorio raíz del proyecto con los siguientes datos:
   ```
   SQLALCHEMY_DATABASE_URI=mysql://usuario:contraseña@host:puerto/nombre_base_datos
   TOKEN_SECRET='Agregar token'
   SECRET_KEY='Agregar key'
   ```

3. **Creación de la base de datos**
   Abra MySQL y cree la base de datos utilizando el archivo `.sql` proporcionado.

4. **Creación del token Bearer**
   - Vaya al endpoint `generate_token` en Postman.
   - En el cuerpo de la solicitud, agregue el username y password de un usuario registrado en la base de datos.
   - Alternativamente, puede crear un nuevo usuario utilizando el endpoint `insert_usuarios` y luego editar su rol a 'administrador' en MySQL para permitir la generación del token.

5. **Configuración del token en la aplicación**
   Una vez obtenido el token, vaya al archivo `app.js` y péguelo en el localStorage:
   ```javascript
   localStorage.setItem('token', '<!-- Ingresar token -->');
   ```
   > **Nota:** El token caducará 24 horas después de su creación.

6. **Ejecución de la aplicación**
   - Ejecute el archivo `run.py`.
   - Abra un navegador y vaya a la URL: http://127.0.0.1:5000/ para probar el funcionamiento de la aplicación.

## Imagen de la aplicación web
![Diagrama de Base de Datos](https://github.com/user-attachments/assets/3a58677f-f4bb-4e6e-aee2-601992eedd3e)
