from datetime import date, timedelta

from django.test import override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Microaccion, Reto, TareaSemanal

HOY = timezone.localdate()


class RetoApiTests(APITestCase):
    def test_crear_y_listar_reto(self):
        url = reverse('reto-list')
        datos = {'titulo': 'Leer 10 libros', 'fecha_inicio': '2026-11-18'}

        respuesta = self.client.post(url, datos, format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reto.objects.count(), 1)

        respuesta = self.client.get(url)
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.assertEqual(respuesta.data['count'], 1)

    def test_rechaza_fecha_fin_anterior_a_inicio(self):
        datos = {'titulo': 'Fechas', 'fecha_inicio': '2026-11-18', 'fecha_fin': '2026-11-01'}
        respuesta = self.client.post(reverse('reto-list'), datos, format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('fecha_fin', respuesta.data)

    def test_rechaza_porcentaje_mayor_a_100(self):
        reto = Reto.objects.create(titulo='Correr', fecha_inicio=date(2026, 11, 18))
        datos = {'reto': reto.id, 'fecha': '2026-11-18', 'descripcion': 'Prueba', 'porcentaje': 150}
        respuesta = self.client.post(reverse('avance-list'), datos, format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('porcentaje', respuesta.data)


# Hoy se simula como semana 7, sea cual sea la fecha real en que se ejecute la prueba.
@override_settings(SEMESTRE_INICIO=HOY - timedelta(weeks=6), SEMANA_DESDE=7, SEMANA_HASTA=15)
class TareaSemanalTests(APITestCase):
    def test_crear_reto_genera_semanas_7_a_15(self):
        datos = {'titulo': 'Reto semanal', 'fecha_inicio': str(HOY)}
        respuesta = self.client.post(reverse('reto-list'), datos, format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)
        semanas = list(
            TareaSemanal.objects.filter(reto_id=respuesta.data['id'])
            .values_list('semana', flat=True)
        )
        self.assertEqual(semanas, list(range(7, 16)))

    def test_semana_cerrada_no_se_puede_modificar(self):
        reto = Reto.objects.create(titulo='Cerrado', fecha_inicio=HOY)
        tarea = TareaSemanal.objects.create(
            reto=reto, semana=6,
            fecha_inicio=HOY - timedelta(days=13), fecha_fin=HOY - timedelta(days=7),
        )
        url = reverse('tareasemanal-detail', args=[tarea.id])
        respuesta = self.client.patch(url, {'porcentaje': 100}, format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)


class PlanRescateTests(APITestCase):
    def setUp(self):
        self.hoy = timezone.localdate()
        self.reto = Reto.objects.create(titulo='Preparar examen', fecha_inicio=self.hoy)
        self.tarea = TareaSemanal.objects.create(
            reto=self.reto, semana=8, porcentaje=40,
            fecha_inicio=self.hoy - timedelta(days=1), fecha_fin=self.hoy + timedelta(days=2),
        )
        self.datos = {'tarea': self.tarea.id, 'titulo': 'Resolver dos ejercicios',
                      'fecha_objetivo': str(self.hoy), 'minutos_estimados': 25}

    def test_meta_diaria_incluye_hoy(self):
        r = self.client.get(reverse('tareasemanal-plan-rescate', args=[self.tarea.id]))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['dias_restantes'], 3)
        self.assertEqual(r.data['faltante'], 60)
        self.assertEqual(r.data['meta_diaria'], 20)

    def test_crear_completar_y_consultar_no_inventa_avance(self):
        r = self.client.post(reverse('microaccion-list'), self.datos, format='json')
        self.assertEqual(r.status_code, 201)
        url = reverse('microaccion-detail', args=[r.data['id']])
        self.assertEqual(self.client.patch(url, {'completada': True}, format='json').status_code, 200)
        plan = self.client.get(reverse('tareasemanal-plan-rescate', args=[self.tarea.id])).data
        self.assertEqual(plan['completadas'], 1)
        self.assertEqual(plan['progreso_acciones'], 100)
        self.assertEqual(plan['minutos_pendientes'], 0)
        self.tarea.refresh_from_db()
        self.assertEqual(self.tarea.porcentaje, 40)

    def test_rechaza_fecha_fuera_de_la_semana(self):
        self.datos['fecha_objetivo'] = str(self.tarea.fecha_fin + timedelta(days=1))
        r = self.client.post(reverse('microaccion-list'), self.datos, format='json')
        self.assertEqual(r.status_code, 400)
        self.assertIn('fecha_objetivo', r.data)

    def test_rechaza_minutos_invalidos(self):
        for minutos in [0, 241]:
            self.datos['minutos_estimados'] = minutos
            self.assertEqual(self.client.post(reverse('microaccion-list'), self.datos, format='json').status_code, 400)

    def test_semana_cerrada_bloquea_creacion_edicion_y_borrado(self):
        accion = Microaccion.objects.create(tarea=self.tarea, titulo='Paso anterior', fecha_objetivo=self.hoy, minutos_estimados=20)
        self.tarea.fecha_inicio = self.hoy - timedelta(days=7)
        self.tarea.fecha_fin = self.hoy - timedelta(days=1)
        self.tarea.save()
        url = reverse('microaccion-detail', args=[accion.id])
        self.assertEqual(self.client.post(reverse('microaccion-list'), self.datos, format='json').status_code, 400)
        self.assertEqual(self.client.patch(url, {'completada': True}, format='json').status_code, 400)
        self.assertEqual(self.client.delete(url).status_code, 400)
        plan = self.client.get(reverse('tareasemanal-plan-rescate', args=[self.tarea.id])).data
        self.assertFalse(plan['editable'])
        self.assertIsNone(plan['meta_diaria'])

    def test_no_planificar_una_semana_futura(self):
        self.tarea.fecha_inicio = self.hoy + timedelta(days=1)
        self.tarea.fecha_fin = self.hoy + timedelta(days=7)
        self.tarea.save()
        self.assertEqual(self.client.post(reverse('microaccion-list'), self.datos, format='json').status_code, 400)

    def test_no_mover_una_accion_a_otra_semana(self):
        accion = Microaccion.objects.create(tarea=self.tarea, titulo='Paso', fecha_objetivo=self.hoy, minutos_estimados=20)
        otra = TareaSemanal.objects.create(reto=self.reto, semana=9, fecha_inicio=self.hoy, fecha_fin=self.hoy + timedelta(days=6))
        r = self.client.patch(reverse('microaccion-detail', args=[accion.id]), {'tarea': otra.id}, format='json')
        self.assertEqual(r.status_code, 400)
