from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Student

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("id_number", "full_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # clases y atributos base para inputs
        for name, field in self.fields.items():
            widget = field.widget
            # clases base
            base_class = "form-control"
            if hasattr(widget, "input_type") and widget.input_type == "password":
                base_class = "form-control"
            widget.attrs["class"] = (widget.attrs.get("class", "") + " " + base_class).strip()

            # autocompletes
            if name == "id_number":
                widget.attrs["autocomplete"] = "username"
                widget.attrs["placeholder"] = "Documento (8 dígitos)"
                widget.attrs["inputmode"] = "numeric"
            elif name == "full_name":
                widget.attrs["autocomplete"] = "name"
                widget.attrs["placeholder"] = "Nombre completo"
            elif name == "email":
                widget.attrs["autocomplete"] = "email"
                widget.attrs["placeholder"] = "email@dominio.com"
            elif name == "password1":
                widget.attrs["autocomplete"] = "new-password"
                widget.attrs["placeholder"] = "Contraseña"
            elif name == "password2":
                widget.attrs["autocomplete"] = "new-password"
                widget.attrs["placeholder"] = "Repetir contraseña"

        # si el form está ligado y hay errores, marcar los campos con is-invalid
        if self.is_bound:
            for name, field in self.fields.items():
                if self.errors.get(name):
                    cls = field.widget.attrs.get("class", "")
                    field.widget.attrs["class"] = (cls + " is-invalid").strip()

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("full_name", "email", "id_number")  # agrega "id_number" si lo dejás editable

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # clases y atributos base para inputs
        for name, field in self.fields.items():
            widget = field.widget
            widget.attrs["class"] = (widget.attrs.get("class", "") + " form-control").strip()

            # autocompletes/placeholders opcionales
            if name == "full_name":
                widget.attrs.setdefault("autocomplete", "name")
                widget.attrs.setdefault("placeholder", "Nombre completo")
            elif name == "email":
                widget.attrs.setdefault("autocomplete", "email")
                widget.attrs.setdefault("placeholder", "email@dominio.com")
            elif name == "id_number":
                widget.attrs.setdefault("autocomplete", "username")
                widget.attrs.setdefault("inputmode", "numeric")
                widget.attrs.setdefault("placeholder", "Documento")

        # si el form está ligado y hay errores, marcar los campos con is-invalid
        if self.is_bound:
            for name in self.fields:
                if self.errors.get(name):
                    cls = self.fields[name].widget.attrs.get("class", "")
                    self.fields[name].widget.attrs["class"] = (cls + " is-invalid").strip()

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ("first_name", "last_name", "level", "grade", "active")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            css_class = "form-control"
            if visible.field.widget.__class__.__name__ in ["CheckboxInput"]:
                css_class = "form-check-input"
            visible.field.widget.attrs["class"] = css_class

class NotifyLateForm(forms.Form):
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.none(), widget=forms.CheckboxSelectMultiple)
    reason = forms.CharField(widget=forms.Textarea, max_length=500)
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["students"].queryset = user.students.filter(active=True)

class SchoolStaffToggleForm(forms.Form):
    id_number = forms.CharField(label="Documento", max_length=10)
    is_school_staff = forms.BooleanField(label="Es personal de escuela", required=False)

    def clean_id_number(self):
        v = self.cleaned_data["id_number"].strip()
        if not v.isdigit():
            raise forms.ValidationError("El documento debe ser numérico.")
        return v
    
class LateArrivalReportFilterForm(forms.Form):
    date_from = forms.DateField(label="Desde", widget=forms.DateInput(attrs={"type": "date"}))
    date_to   = forms.DateField(label="Hasta", widget=forms.DateInput(attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs["class"] = (f.widget.attrs.get("class", "") + " form-control").strip()

class LateArrivalAggregatedFilterForm(forms.Form):
    q = forms.CharField(
        label="Buscar alumno",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Apellido o nombre"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["q"].widget.attrs["class"] = "form-control"




class BootstrapAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # checkbox (recordarme) si lo habilitás:
            if field.widget.__class__.__name__ == "CheckboxInput":
                base = "form-check-input"
            else:
                base = "form-control"
            field.widget.attrs["class"] = (field.widget.attrs.get("class", "") + " " + base).strip()