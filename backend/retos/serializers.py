from django.utils import timezone
from rest_framework import serializers

from .models import Avance, Microaccion, Reto, TareaSemanal
from .plan_rescate import exigir_semana_abierta


class AvanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avance
        fields = ['id', 'reto', 'fecha', 'descripcion', 'porcentaje', 'creado']
        read_only_fields = ['creado']


class RetoSerializer(serializers.ModelSerializer):
    total_avances = serializers.IntegerField(source='avances.count', read_only=True)

    class Meta:
        model = Reto
        fields = [
            'id', 'titulo', 'descripcion', 'fecha_inicio', 'fecha_fin',
            'estado', 'total_avances', 'creado', 'actualizado',
        ]
        read_only_fields = ['creado', 'actualizado']

    def validate(self, datos):
        inicio = datos.get('fecha_inicio', getattr(self.instance, 'fecha_inicio', None))
        fin = datos.get('fecha_fin', getattr(self.instance, 'fecha_fin', None))
        if inicio and fin and fin < inicio:
            raise serializers.ValidationError(
                {'fecha_fin': 'La fecha de fin no puede ser anterior a la fecha de inicio.'}
            )
        return datos


class TareaSemanalSerializer(serializers.ModelSerializer):
    reto_titulo = serializers.CharField(source='reto.titulo', read_only=True)

    class Meta:
        model = TareaSemanal
        fields = [
            'id', 'reto', 'reto_titulo', 'semana', 'fecha_inicio', 'fecha_fin',
            'descripcion', 'porcentaje', 'actualizado',
        ]
        read_only_fields = ['reto', 'semana', 'fecha_inicio', 'fecha_fin', 'actualizado']

    def validate(self, datos):
        tarea = self.instance
        hoy = timezone.localdate()
        if tarea is not None:
            if hoy > tarea.fecha_fin:
                raise serializers.ValidationError(
                    f'La semana {tarea.semana} ya está cerrada; no se puede modificar.'
                )
            if hoy < tarea.fecha_inicio:
                raise serializers.ValidationError(
                    f'La semana {tarea.semana} todavía no ha comenzado.'
                )
        return datos


class MicroaccionSerializer(serializers.ModelSerializer):
    vencida = serializers.SerializerMethodField()

    class Meta:
        model = Microaccion
        fields = ['id', 'tarea', 'titulo', 'fecha_objetivo', 'minutos_estimados', 'completada', 'creado', 'vencida']
        read_only_fields = ['creado']

    def get_vencida(self, obj) -> bool:
        return not obj.completada and obj.fecha_objetivo < timezone.localdate()

    def validate(self, datos):
        tarea = self.instance.tarea if self.instance else datos['tarea']
        if self.instance and datos.get('tarea', tarea) != tarea:
            raise serializers.ValidationError({'tarea': 'Una microacción no se puede mover a otra semana.'})
        exigir_semana_abierta(tarea)
        fecha = datos.get('fecha_objetivo', getattr(self.instance, 'fecha_objetivo', None))
        if fecha is not None and not tarea.fecha_inicio <= fecha <= tarea.fecha_fin:
            raise serializers.ValidationError({'fecha_objetivo': 'La fecha debe estar dentro de la semana.'})
        if (self.instance is None or 'fecha_objetivo' in datos) and fecha < timezone.localdate():
            raise serializers.ValidationError({'fecha_objetivo': 'Elige hoy o un día posterior de esta semana.'})
        return datos


class PlanRescateSerializer(serializers.Serializer):
    tarea = serializers.IntegerField()
    reto = serializers.IntegerField()
    reto_titulo = serializers.CharField()
    semana = serializers.IntegerField()
    hoy = serializers.DateField()
    fecha_fin = serializers.DateField()
    editable = serializers.BooleanField()
    porcentaje = serializers.IntegerField()
    faltante = serializers.IntegerField()
    dias_restantes = serializers.IntegerField()
    meta_diaria = serializers.IntegerField(allow_null=True)
    total_acciones = serializers.IntegerField()
    completadas = serializers.IntegerField()
    progreso_acciones = serializers.IntegerField()
    minutos_pendientes = serializers.IntegerField()
    vencidas = serializers.IntegerField()
    acciones = MicroaccionSerializer(many=True)
