# Día 11: Estrategia de Migraciones

La creación manual de tablas en una base de datos mediante el cliente SQL (`pgAdmin`, `DBeaver` o terminal) es un antipatrón en proyectos modernos orientados a producción. Las bases de datos deben mantenerse mediante secuencias de código controladas, de forma que cualquier desarrollador pueda replicarlas al 100% y los servidores de CI/CD puedan desplegarlas.

A esta estrategia se le conoce como **Database Migrations** o Infraestructura como Código (IaC) para Bases de Datos.

## ¿Qué es una migración?
Una migración es un script (usualmente un archivo SQL o Python) que transiciona el esquema de tu base de datos del Estado A al Estado B. Por ejemplo:
- `0001_init.sql`: Crea las tablas `users` e `items`.
- `0002_add_email_to_users.sql`: Modifica la tabla `users` añadiendo una columna `email`.

Herramientas populares:
- **Golang-Migrate**: Herramienta agnóstica basada puramente en CLI usando archivos `.sql`.
- **Alembic**: La más popular en Python, muy acoplada a *SQLAlchemy*.
- **Yoyo-Migrations**: La que elegimos en este proyecto, basada en Python pero que permite usar scripts `raw SQL` sin casarte con un ORM.

## Configuración en el Proyecto

En lugar de usar `golang-migrate` como ejecutable en Windows, usamos **`yoyo-migrations`** a través de `pip` dado tu stack en Python. 

1. **Configuración (`yoyo.ini`)**: Definimos la URI hacia tu contenedor local de PostgreSQL (`postgresql://myuser:superseguro123@localhost:5432/mydb`).
2. **Carpeta `migrations`**: Almacena todos los archivos `.sql`.  Aquí es donde reside el archivo `0001_init_schema.sql` con las sentencias `CREATE TABLE IF NOT EXISTS...`.

## Cómo Ejecutar

Para crear tus tablas de una forma segura y reproducible:

1. Asegúrate de tener tu contenedor Docker corriendo y el puerto 5432 mapeado.
2. Instala la dependencia:
```bash
pip install yoyo-migrations
```
3. Ejecuta el plan:
```bash
yoyo apply
```
La herramienta conectará y creará una tabla interna secreta (`_yoyo_migration`) para llevar cuenta de qué archivos ya se corrieron y no volverlos a correr en el futuro.
