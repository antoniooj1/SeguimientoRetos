# Evidencias de Seguimiento de Retos

Fecha de verificación: 25/11/2026. Las capturas y registros corresponden a comprobaciones reales del entorno local.

| Evidencia | Archivos | Resultado |
| --- | --- | --- |
| 1. Backend y MySQL | E1_check.txt, E1_pruebas_guia.txt, E1_migracion_microacciones.txt | Comprobación sin incidencias, cinco pruebas originales OK y migración aplicada |
| 2. Compilación y pruebas web | E2_build_web.txt, E2_pruebas_frontend.txt | Build correcto y ocho pruebas superadas |
| 3. Flujos web | E2_lista_web.png, E2_busqueda_web.png, E2_validacion_fechas.png, E2_avance_web.png, E3_semanas_web.png | Lista, búsqueda, validación, avance y seguimiento semanal |
| 4. Android | E4_build_android.txt, E4_semana_guardada_android.png | APK generada, instalada y porcentaje semanal guardado |
| 5. Cierre de semana | E3_alertas_web.png, E5_aviso_android.png, E5_alertas_android.png, E5_PATCH_400.txt | Aviso rojo, alertas y rechazo HTTP 400 al editar semana cerrada |
| 6. Plan de rescate | E6_plan_web.png, E6_plan_cerrado.png, E6_plan_api.json, E6_pruebas_backend.txt | Plan persistente, microacciones completadas y bloqueo histórico; 12 pruebas backend OK |

## Alcance de la comprobación de Android

Se comprobó el acceso a la pantalla del plan y su cálculo de 10 puntos por día con 50 % pendiente y cinco días disponibles. La prueba de creación de microacciones en Android se interrumpió a petición del usuario; no se presenta como superada. La función de crear y completar acciones sí se verificó en la web y en las pruebas de la API.

## Problemas encontrados y solución

- El README conservaba el puerto 8001 de una ejecución anterior. Se unificaron el backend, la web y el emulador en 8000 (Android usa 10.0.2.2).
- Las semanas antiguas aparecen cerradas al cambiar la fecha real. Se conservó el calendario y se verificó que el servidor rechaza cambios con HTTP 400.
- Android Studio utiliza un Java diferente al requerido por Capacitor. La compilación se ejecutó con Temurin 21 y terminó con BUILD SUCCESSFUL.

La APK se genera en `frontend/android/app/build/outputs/apk/debug/app-debug.apk`; los binarios de compilación y las credenciales se excluyen del repositorio.
