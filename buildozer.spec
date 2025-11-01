[app]

# (OBLIGATORIO) Título de la aplicación, como aparecerá en el teléfono.
title = Gestion de Inventario

# (OBLIGATORIO) Nombre del paquete, usa solo letras minúsculas y sin espacios.
package.name = gestioninventario

# (OBLIGATORIO) Dominio de tu paquete, usa tu nombre de usuario de GitHub al revés para que sea único.
package.domain = com.nosferatus74.gestioninventario

# (OBLIGATORIO) Nombre del archivo principal de Python.
source.main = main.py

# Directorios a incluir o excluir
source.dir = .
source.exclude_dirs = .buildozer, .git

# Versión de la aplicación
version = 1.0.0

# (CLAVE) Lista de requerimientos (librerías que usa tu código).
# Kivy es esencial, y AGREGAMOS sqlite3.
requirements = python3, kivy==2.3.0, sqlite3

# Icono de la aplicación (descomentá y reemplazá si tenés un archivo .png)
# icon.filename = %(source.dir)s/icon.png

# Orientación por defecto: 'all', 'landscape', 'portrait'
orientation = portrait

# Modo de pantalla completa
fullscreen = 0

# -----------------
# Android
# -----------------

# (NUEVA LÍNEA CLAVE) ¡SOLUCIÓN! Acepta automáticamente las licencias del SDK/NDK
android.accept_sdk_licenses = True

# (CLAVE) Nivel API de destino (Android 7.0 - Nougat es ultra-estable)
android.api = 24

# Nivel API mínimo soportado por la app (Android 5.0 - Lollipop)
android.minapi = 21

# Usar el SDK de Buildozer
android.archs = arm64-v8a, armeabi-v7a

# Versión mínima de Kivy (sugerida para estabilidad)
android.new_buildozer = True

# -----------------
# Otros
# -----------------

# Buildozer siempre debe limpiar los archivos temporales de compilación.
allow_storage = True
