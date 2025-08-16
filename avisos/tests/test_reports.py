# archivo: avisos/tests/test_reports.py
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from avisos.models import User, Student, ResponsibleStudent, LateArrival


class BaseReportSetup(TestCase):
    def setUp(self):
        # Usuarios
        self.school = User.objects.create_user(
            id_number="11111111", full_name="Escuela Uno", email="escuela@ccm.test", password="pass", is_school_staff=True
        )
        self.resp_a = User.objects.create_user(
            id_number="22222222", full_name="Padre A", email="a@test.com", password="pass"
        )
        self.resp_b = User.objects.create_user(
            id_number="33333333", full_name="Padre B", email="b@test.com", password="pass"
        )

        # Alumnos
        self.st_a1 = Student.objects.create(first_name="Ana", last_name="Alvarez", level="Primaria", grade="6", active=True)
        self.st_a2 = Student.objects.create(first_name="Axel", last_name="Alvarez", level="Primaria", grade="3", active=True)
        self.st_b1 = Student.objects.create(first_name="Beto", last_name="Bruno", level="Secundaria", grade="1", active=True)

        # Vinculación responsables
        ResponsibleStudent.objects.create(responsible=self.resp_a, student=self.st_a1)
        ResponsibleStudent.objects.create(responsible=self.resp_a, student=self.st_a2)
        ResponsibleStudent.objects.create(responsible=self.resp_b, student=self.st_b1)

        # Llegadas tarde
        now = timezone.now()
        # A1: 2 dentro de 30 días, 1 fuera (31 días)
        LateArrival.objects.create(responsible=self.resp_a, student=self.st_a1, reason="Demora tránsito", reported_at=now - timedelta(days=5))
        LateArrival.objects.create(responsible=self.resp_a, student=self.st_a1, reason="Dormido", reported_at=now - timedelta(days=10))
        LateArrival.objects.create(responsible=self.resp_a, student=self.st_a1, reason="Viejo", reported_at=now - timedelta(days=31))
        # A2: 1 dentro de 30 días
        LateArrival.objects.create(responsible=self.resp_a, student=self.st_a2, reason="Médico", reported_at=now - timedelta(days=2))
        # B1: 3 dentro de 30 días
        LateArrival.objects.create(responsible=self.resp_b, student=self.st_b1, reason="Colectivo", reported_at=now - timedelta(days=1))
        LateArrival.objects.create(responsible=self.resp_b, student=self.st_b1, reason="Trámite", reported_at=now - timedelta(days=7))
        LateArrival.objects.create(responsible=self.resp_b, student=self.st_b1, reason="Llueve", reported_at=now - timedelta(days=10))

        self.url_detalle = reverse("report_lates_detailed")
        self.url_agg = reverse("report_lates_aggregated")

    def login(self, user):
        ok = self.client.login(username=user.id_number, password="pass")
        self.assertTrue(ok, "No pudo loguear el usuario de prueba")


class TestDetailedReport(BaseReportSetup):
    def test_responsable_ve_solo_sus_registros(self):
        self.login(self.resp_a)
        # rango amplio para incluir todo
        d1 = (timezone.now() - timedelta(days=365)).date().isoformat()
        d2 = timezone.now().date().isoformat()
        resp = self.client.get(self.url_detalle, {"date_from": d1, "date_to": d2})
        self.assertEqual(resp.status_code, 200)
        rows = list(resp.context["rows"])
        # Solo registros de resp_a (A1 y A2)
        self.assertTrue(all(r.responsible_id == self.resp_a.id for r in rows))
        # Conteo exacto: A1 (3) + A2 (1) = 4
        self.assertEqual(len(rows), 4)

    def test_school_ve_todo(self):
        self.login(self.school)
        d1 = (timezone.now() - timedelta(days=365)).date().isoformat()
        d2 = timezone.now().date().isoformat()
        resp = self.client.get(self.url_detalle, {"date_from": d1, "date_to": d2})
        self.assertEqual(resp.status_code, 200)
        rows = list(resp.context["rows"])
        # Total creados: 7
        self.assertEqual(len(rows), 7)

    def test_filtro_rango_fechas(self):
        self.login(self.school)
        # elegir un rango que solo capture los últimos 10 días
        d1 = (timezone.now() - timedelta(days=10)).date().isoformat()
        d2 = timezone.now().date().isoformat()
        resp = self.client.get(self.url_detalle, {"date_from": d1, "date_to": d2})
        self.assertEqual(resp.status_code, 200)
        rows = list(resp.context["rows"])
        # Dentro de 10 días: A1 (2: 5 y 10 días), A2 (1: 2 días), B1 (3: 1,7,10 días) = 6
        self.assertEqual(len(rows), 6)

    def test_export_excel(self):
        self.login(self.school)
        d1 = (timezone.now() - timedelta(days=365)).date().isoformat()
        d2 = timezone.now().date().isoformat()
        resp = self.client.get(self.url_detalle, {"date_from": d1, "date_to": d2, "export": "1"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        # XLSX es un zip: debería iniciar con 'PK'
        self.assertTrue(resp.content[:2] == b"PK")


class TestAggregatedReport(BaseReportSetup):
    def test_aggregated_counts_school(self):
        self.login(self.school)
        resp = self.client.get(self.url_agg)
        self.assertEqual(resp.status_code, 200)
        rows = list(resp.context["rows"])

        # Mapear por alumno para chequear conteos
        by_student = { (r["student__last_name"], r["student__first_name"]): r for r in rows }

        # A1: total 3, last30 2
        a1 = by_student[("Alvarez", "Ana")]
        self.assertEqual(a1["total"], 3)
        self.assertEqual(a1["last30"], 2)

        # A2: total 1, last30 1
        a2 = by_student[("Alvarez", "Axel")]
        self.assertEqual(a2["total"], 1)
        self.assertEqual(a2["last30"], 1)

        # B1: total 3, last30 3
        b1 = by_student[("Bruno", "Beto")]
        self.assertEqual(b1["total"], 3)
        self.assertEqual(b1["last30"], 3)

    def test_aggregated_scope_responsable(self):
        self.login(self.resp_a)
        resp = self.client.get(self.url_agg)
        rows = list(resp.context["rows"])
        # Solo alumnos de resp_a (A1/A2)
        apellidos = { (r["student__last_name"], r["student__first_name"]) for r in rows }
        self.assertTrue(("Alvarez", "Ana") in apellidos and ("Alvarez", "Axel") in apellidos)
        self.assertFalse(("Bruno", "Beto") in apellidos)

    def test_aggregated_search_q(self):
        self.login(self.school)
        # buscar 'Brun' debe traer solo Beto Bruno
        resp = self.client.get(self.url_agg, {"q": "Brun"})
        rows = list(resp.context["rows"])
        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertEqual(r["student__last_name"], "Bruno")
        self.assertEqual(r["student__first_name"], "Beto")
        self.assertEqual(r["total"], 3)
        self.assertEqual(r["last30"], 3)
