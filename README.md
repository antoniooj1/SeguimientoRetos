# Seguimiento de Retos

Aplicación de las guías 02, 03 y 04: Django 5.2 + DRF + MySQL 8.4, Angular 22 + Ionic 9 y Capacitor 8.

## Iniciar en macOS

Desde la raíz, en dos terminales:

```sh
./scripts/iniciar-backend.sh
```

```sh
./scripts/iniciar-frontend.sh
```

- Web: http://localhost:8100
- API: http://127.0.0.1:8001/api/
- Swagger: http://127.0.0.1:8001/api/docs/
- Administrador: http://127.0.0.1:8001/admin/
- Android: http://10.0.2.2:8001/api/

Se usa 8001 porque CiudadanIA ya ocupa 8000. MySQL mantiene 3307.

## Estructura

- backend/config: configuración Django.
- backend/retos: modelos Reto, Avance, TareaSemanal; API, calendario, administrador y pruebas.
- frontend/src/app/core: API, modelos, seguimiento RxJS y reglas del semáforo.
- frontend/src/app/paginas: lista, creación, detalle y alertas.
- documentacion: guías del profesor e informes.

## Pruebas

```sh
cd backend
.venv/bin/python manage.py test retos
cd ../frontend
npm test -- --watch=false
npm run build
```

## Android

```sh
cd frontend
npm run build
npx cap sync android
npx cap open android
cd android
./gradlew assembleDebug
```

El JDK debe ser Eclipse Temurin 21. La APK queda en frontend/android/app/build/outputs/apk/debug/app-debug.apk.

Credenciales administrativas locales: `.local/django-admin.env`. Variables del backend: `backend/.env`. Ambos están excluidos de Git; nunca los adjuntes a una entrega.

El reto «Demostración de semáforos» contiene datos de prueba para mostrar los colores y el riesgo; no representa actividad real del estudiante.
