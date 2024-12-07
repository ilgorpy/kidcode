from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden

class RoleRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("У вас нет прав для доступа к этой странице.")
        return super().dispatch(request, *args, **kwargs)