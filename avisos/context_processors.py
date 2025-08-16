from .models import Student

def ui_flags(request):
    if not request.user.is_authenticated:
        return {"has_active_students": False, "is_school_staff": False}
    return {
        "has_active_students": Student.objects.filter(
            responsiblestudent__responsible=request.user, active=True
        ).exists(),
        "is_school_staff": getattr(request.user, "is_school_staff", False) or request.user.is_superuser,
    }