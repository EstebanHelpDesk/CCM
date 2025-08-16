from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy

urlpatterns = [
    path(
        "ack/<int:pk>/eliminar/",
        views.LateArrivalDeleteView.as_view(),
        name="notification_delete",
    ),
    path("pibes/", views.StudentsListView.as_view(), name="students_list"),
    path("pibes/nuevo/", views.StudentCreateView.as_view(), name="student_create"),
    path(
        "pibes/<int:pk>/editar/",
        views.StudentUpdateView.as_view(),
        name="student_update",
    ),
    path(
        "pibes/<int:pk>/eliminar/",
        views.StudentDeleteView.as_view(),
        name="student_delete",
    ),
    path("miperfil/", views.ProfileView.as_view(), name="profile"),
    path(
        "pibes/registrar/",
        views.RegisterStudentsView.as_view(),
        name="register_students",
    ),
    path("ack-late/", views.NotifyLateView.as_view(), name="notify_late"),
    path("ack/", views.NotificationsListView.as_view(), name="notifications_list"),
    path("ccm/hoy/", views.SchoolTodayLatesView.as_view(), name="school_today_lates"),
    path(
        "ccm/asignar/",
        views.SchoolStaffAssignView.as_view(),
        name="school_staff_assign",
    ),
    path(
        "pibes/<int:student_id>/historial/",
        views.StudentLateHistoryView.as_view(),
        name="student_late_history",
    ),
    path(
        "rpt/llegadas/",
        views.LateArrivalReportView.as_view(),
        name="report_lates_detailed",
    ),
    path(
        "rpt/llegadas-totalizado/",
        views.LateArrivalAggregatedView.as_view(),
        name="report_lates_aggregated",
    ),
    path(
        "a/password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="auth/password_reset.html",
            email_template_name="auth/password_reset_email.txt",
            subject_template_name="auth/password_reset_subject.txt",
            success_url=reverse_lazy("password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "a/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "a/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "a/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]
