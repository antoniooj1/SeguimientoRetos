"""Meta diaria orientativa y resumen del plan; no cambia porcentajes históricos."""
from math import ceil

from django.utils import timezone
from rest_framework.exceptions import ValidationError


def exigir_semana_abierta(tarea, hoy=None):
    hoy = hoy or timezone.localdate()
    if hoy > tarea.fecha_fin:
        raise ValidationError(f'La semana {tarea.semana} ya está cerrada; su plan es de solo lectura.')
    if hoy < tarea.fecha_inicio:
        raise ValidationError(f'La semana {tarea.semana} todavía no ha comenzado.')


def resumir_plan(tarea, hoy=None):
    hoy = hoy or timezone.localdate()
    acciones = list(tarea.microacciones.all())
    pendientes = [a for a in acciones if not a.completada]
    editable = tarea.fecha_inicio <= hoy <= tarea.fecha_fin
    dias = max(0, (tarea.fecha_fin - hoy).days + 1) if editable else 0
    faltante = max(0, 100 - tarea.porcentaje)
    hechas = len(acciones) - len(pendientes)
    return {
        'tarea': tarea.id, 'reto': tarea.reto_id, 'reto_titulo': tarea.reto.titulo,
        'semana': tarea.semana, 'hoy': hoy, 'fecha_fin': tarea.fecha_fin,
        'editable': editable, 'porcentaje': tarea.porcentaje, 'faltante': faltante,
        'dias_restantes': dias, 'meta_diaria': ceil(faltante / dias) if dias else None,
        'total_acciones': len(acciones), 'completadas': hechas,
        'progreso_acciones': round(100 * hechas / len(acciones)) if acciones else 0,
        'minutos_pendientes': sum(a.minutos_estimados for a in pendientes),
        'vencidas': sum(a.fecha_objetivo < hoy for a in pendientes),
        'acciones': acciones,
    }
