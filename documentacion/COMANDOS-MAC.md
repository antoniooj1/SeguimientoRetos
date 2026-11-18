# Seguimiento de Retos — comandos para macOS

Proyecto: `~/proyectos/SeguimientoRetos`.

## Backend

```sh
cd ~/proyectos/SeguimientoRetos/backend
source .venv/bin/activate
python --version
python -m django --version
python -m pip check
```

Las credenciales de la aplicación están en `backend/.env`. La clave administrativa de la instancia independiente está en `.local/mysql-admin.env`. Ambos archivos son privados y están excluidos de Git. No los adjuntes al informe.

MySQL 8.4 inicia con tu sesión de macOS mediante `local.seguimientoretos.mysql84`. Usa únicamente `127.0.0.1:3307`. Su directorio de datos está en `.local/mysql/data`; la instalación anterior de MySQL se conserva.

## Web

```sh
cd ~/proyectos/SeguimientoRetos/frontend
ionic serve --project=frontend --port=8100
```

Abre http://localhost:8100 y detén el servidor con Ctrl+C cuando termines.

## Android y APK

Abre una terminal nueva para cargar JAVA_HOME y ANDROID_HOME.

```sh
java -version
adb devices
cd ~/proyectos/SeguimientoRetos/frontend
npm run build
npx cap sync android
npx cap open android
cd android
./gradlew assembleDebug
```

APK: `frontend/android/app/build/outputs/apk/debug/app-debug.apk`.

En Android Studio, el proyecto usa `GRADLE_LOCAL_JAVA_HOME` y `.gradle/config.properties` apunta al JDK 21. Si se solicita seleccionar Gradle JDK, usa `/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home`.

## Reproducir dependencias

```sh
cd ~/proyectos/SeguimientoRetos/backend
source .venv/bin/activate
python -m pip install -r requirements.txt
cd ../frontend
npm ci
```

## Paso 12

Es solo referencia para la próxima etapa. No se crea ni ejecuta todavía el backend Django; no se necesita `manage.py` ni abrir el puerto 8000.

- Navegador en la Mac: http://localhost:8000/api/
- Emulador: http://10.0.2.2:8000/api/
- Teléfono: http://IP_LOCAL_DE_LA_MAC:8000/api/
