# Entrega: puntos 9, 10 y 11

Fecha: 18 de noviembre de 2026. Estudiante: Antonio Ojeda.
Equipo: Mac con Apple Silicon. Los comandos de Windows se adaptaron a macOS.

## Punto 9 — Android Studio, Java y emulador

- Android Studio Rabbit 2 2026.2.2 Patch 1 instalado.
- SDK Platform 36, Build-Tools 36.0.0, Platform-Tools, Command-line Tools y Emulator instalados.
- Eclipse Temurin JDK 21.0.13+9 instalado. JAVA_HOME y ANDROID_HOME persistentes en .zprofile y .zshrc.
- Android Studio usa GRADLE_LOCAL_JAVA_HOME; android/.gradle/config.properties apunta a Temurin 21.
- Emulador Retos_API_36: Pixel 7, Google APIs, arm64-v8a, Android API 36.
- adb detecta emulator-5556 como device. El número 5556 es el puerto asignado al emulador y cumple la misma función que el 5554 del ejemplo.

## Punto 10 — Capacitor y APK

Capacitor core, android y cli de la rama 8 instalados localmente en frontend. Se conserva la inicialización existente y la plataforma Android existente, ya que cap init y cap add android se ejecutan una sola vez.

webDir: dist/frontend/browser. npm run build, cap sync android y cap doctor comprobados. Se ejecutaron ./gradlew --stop y ./gradlew assembleDebug con Temurin 21.

APK: /Users/antoniojoseojeda/proyectos/SeguimientoRetos/frontend/android/app/build/outputs/apk/debug/app-debug.apk

Se adjuntan la APK, el registro real de compilación y una captura de la aplicación abierta en el emulador.

## Punto 11 — Git

Commit original: a8c6ea1 — Prepara el entorno de desarrollo web y Android.

El repositorio conserva .gitignore, backend/requirements.txt, frontend/package-lock.json y los archivos de Android. Se verificó que backend/.env, backend/.venv y .local están excluidos. Ninguna contraseña se incluye en esta entrega.

## Problemas encontrados y soluciones

1. Java ejecutaba la versión 8 y JAVA_HOME apuntaba a Java 25. Se instaló Java 21, se corrigieron JAVA_HOME y PATH y se seleccionó el JDK 21 para Gradle. Finalmente se ajustó el proveedor a Eclipse Temurin, tal como pide la consigna.
2. El SDK existente tenía Platform 37, pero faltaba Platform 36 y Command-line Tools. Se instalaron los paquetes requeridos y se creó el dispositivo Retos_API_36.
3. El proyecto no tenía inicialmente plataforma Android ni APK. Se inicializó Capacitor una sola vez, se configuró webDir y se compiló la web antes de añadir y sincronizar Android.
4. Las terminales abiertas conservaban variables anteriores. Las variables se hicieron persistentes y se recargaron en las verificaciones.
5. La primera compilación descargó Gradle y dependencias; se esperó a BUILD SUCCESSFUL antes de instalar la APK.

Observación: npm reporta 12 alertas altas en herramientas de desarrollo/dependencias transitivas y scripts de instalación bloqueados. No se usó --force ni --legacy-peer-deps. Build, pruebas, sincronización y aplicación funcionaron. Esta observación no implica que la compilación haya fallado.

No se observaron los errores "Unsupported class file major version 69", "could not determine executable to run" ni "Cannot run init" durante esta verificación. No se inventan mensajes de error que no ocurrieron.
