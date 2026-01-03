from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model

User = get_user_model()

class ListadoUsuariosView(LoginRequiredMixin, View):

    def get(self, request):
        usuarios = User.objects.all()
        return render(request, "usuarios/listado_usuarios.html", {"usuarios": usuarios, "page_title": "Listado de Usuarios"})

class PerfilUsuarioView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "usuarios/perfil_usuario.html"
    context_object_name = "usuario"
    pk_url_kwarg = "user_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Perfil de {self.object.get_full_name()}"
        return context