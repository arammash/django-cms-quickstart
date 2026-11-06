from urllib.parse import urlencode

from django.http import HttpResponseRedirect
from django.urls import reverse


class FrontendEditModeMiddleware:
    session_key = "frontend_edit_mode"
    permissions = ("exhibitions.change_project", "exhibitions.change_artist")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "edit" in request.GET:
            if request.GET["edit"].lower() == "off":
                request.session.pop(self.session_key, None)
                query = request.GET.copy()
                query.pop("edit", None)
                url = request.path
                if query:
                    url = f"{url}?{query.urlencode()}"
                return HttpResponseRedirect(url)

            if not request.user.is_authenticated:
                login_url = reverse("admin:login")
                query = urlencode({"next": request.get_full_path()})
                return HttpResponseRedirect(f"{login_url}?{query}")

            if request.user.is_staff and any(
                request.user.has_perm(permission) for permission in self.permissions
            ):
                request.session[self.session_key] = True
            else:
                request.session.pop(self.session_key, None)

        can_edit = request.user.is_authenticated and request.user.is_staff and any(
            request.user.has_perm(permission) for permission in self.permissions
        )
        request.frontend_edit_mode = bool(
            request.session.get(self.session_key) and can_edit
        )
        return self.get_response(request)
