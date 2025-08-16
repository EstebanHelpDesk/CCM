from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy

urlpatterns = [
    path("avisos/<int:pk>/eliminar/", views.LateArrivalDeleteView.as_view(), name="notification_delete"),
    path("alumnos/", views.StudentsListView.as_view(), name="students_list"),
    path("alumnos/nuevo/", views.StudentCreateView.as_view(), name="student_create"),
    path("alumnos/<int:pk>/editar/", views.StudentUpdateView.as_view(), name="student_update"),
    path("alumnos/<int:pk>/eliminar/", views.StudentDeleteView.as_view(), name="student_delete"),
    path("perfil/", views.ProfileView.as_view(), name="profile"),
    path("alumnos/registrar/", views.RegisterStudentsView.as_view(), name="register_students"),
    path("avisar-tarde/", views.NotifyLateView.as_view(), name="notify_late"),
    path("avisos/", views.NotificationsListView.as_view(), name="notifications_list"),
    path("escuela/hoy/", views.SchoolTodayLatesView.as_view(), name="school_today_lates"),
    path("escuela/asignar/", views.SchoolStaffAssignView.as_view(), name="school_staff_assign"),
    path("alumnos/<int:student_id>/historial/", views.StudentLateHistoryView.as_view(), name="student_late_history"),
    path("reportes/llegadas/", views.LateArrivalReportView.as_view(), name="report_lates_detailed"),
    path("reportes/llegadas-totalizado/", views.LateArrivalAggregatedView.as_view(), name="report_lates_aggregated"),
    path(
        "accounts/password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="auth/password_reset.html",
            email_template_name="auth/password_reset_email.txt",
            subject_template_name="auth/password_reset_subject.txt",
            success_url=reverse_lazy("password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "accounts/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),


]
