from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

id8_validator = RegexValidator(regex=r"^\d{8}$", message="Debe ser un número de 8 dígitos.")

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, id_number, full_name, email=None, password=None, **extra_fields):
        if not id_number:
            raise ValueError("El usuario debe tener un número de identificación (id_number).")
        email = self.normalize_email(email)
        user = self.model(
            id_number=id_number,
            full_name=full_name,
            email=email,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id_number, full_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser debe tener is_superuser=True.")
        return self.create_user(id_number, full_name, email, password, **extra_fields)


class User(AbstractUser):
    # quitamos 'username' y usamos id_number como identificador
    username = None
    id_number = models.CharField("Documento", max_length=10, unique=True, validators=[id8_validator])
    full_name = models.CharField("Nombre completo", max_length=150)
    email = models.EmailField("Email", unique=True)
    is_school_staff = models.BooleanField("Es personal de escuela", default=False)

    USERNAME_FIELD = "id_number"
    REQUIRED_FIELDS = ["full_name", "email"]

    objects = UserManager()  # 👈 usar nuestro manager

    def __str__(self):
        return f"{self.full_name} ({self.id_number})"

class Student(models.Model):
    LEVEL_CHOICES = [("INICIAL", "INICIAL"), ("PRIMARIA", "PRIMARIA"), ("SECUNDARIA", "SECUNDARIA")]
    first_name = models.CharField("Nombre", max_length=100)
    last_name = models.CharField("Apellido", max_length=100)
    level = models.CharField("Nivel", max_length=12, choices=LEVEL_CHOICES)
    grade = models.PositiveSmallIntegerField("Grado/Año")
    active = models.BooleanField(default=True)
    responsibles = models.ManyToManyField("User", through="ResponsibleStudent", related_name="students")
    def __str__(self):
        return f"{self.last_name}, {self.first_name} - {self.level} {self.grade}"

class ResponsibleStudent(models.Model):
    responsible = models.ForeignKey("User", on_delete=models.CASCADE)
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    class Meta:
        unique_together = ("responsible", "student")

class LateArrival(models.Model):
    responsible = models.ForeignKey("User", on_delete=models.CASCADE)
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    reason = models.TextField(max_length=500)
    reported_at = models.DateTimeField(default=timezone.now)
    reviewed_by = models.ForeignKey(
        "User", null=True, blank=True, on_delete=models.SET_NULL, related_name="reviewed_late_arrivals"
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
