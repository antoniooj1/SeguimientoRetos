from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Avance, Microaccion, Reto, TareaSemanal
from .plan_rescate import exigir_semana_abierta, resumir_plan
from .semanas import crear_tareas_semanales
from .serializers import AvanceSerializer, MicroaccionSerializer, PlanRescateSerializer, RetoSerializer, TareaSemanalSerializer


class RetoViewSet(viewsets.ModelViewSet):
    """Listar, crear, consultar, modificar y eliminar retos."""

    queryset = Reto.objects.all()
    serializer_class = RetoSerializer
    filterset_fields = ['estado']
    search_fields = ['titulo', 'descripcion']
    ordering_fields = ['fecha_inicio', 'titulo', 'estado']

    def perform_create(self, serializer):
        reto = serializer.save()
        crear_tareas_semanales(reto)

    @action(detail=True, methods=['post'], url_path='generar-semanas')
    def generar_semanas(self, request, pk=None):
        """Crea las semanas que falten (útil para retos creados antes de esta guía)."""
        creadas = crear_tareas_semanales(self.get_object())
        return Response({'creadas': creadas}, status=status.HTTP_200_OK)


class AvanceViewSet(viewsets.ModelViewSet):
    """Listar, crear, consultar, modificar y eliminar avances."""

    queryset = Avance.objects.select_related('reto')
    serializer_class = AvanceSerializer
    filterset_fields = ['reto']
    ordering_fields = ['fecha', 'porcentaje']


class TareaSemanalViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Consultar y actualizar tareas semanales. Se crean solas; no se borran."""

    queryset = TareaSemanal.objects.select_related('reto')
    serializer_class = TareaSemanalSerializer
    filterset_fields = ['reto', 'semana']
    ordering_fields = ['semana']
    pagination_class = None

    @extend_schema(responses=PlanRescateSerializer)
    @action(detail=True, methods=['get'], url_path='plan-rescate')
    def plan_rescate(self, request, pk=None):
        """Meta diaria sugerida y lista persistente de microacciones de la semana."""
        return Response(PlanRescateSerializer(resumir_plan(self.get_object())).data)


class MicroaccionViewSet(viewsets.ModelViewSet):
    """Planificar, editar, completar o eliminar acciones únicamente en semanas abiertas."""

    queryset = Microaccion.objects.select_related('tarea', 'tarea__reto')
    serializer_class = MicroaccionSerializer
    filterset_fields = ['tarea', 'completada']
    pagination_class = None

    def perform_destroy(self, instance):
        exigir_semana_abierta(instance.tarea)
        instance.delete()
