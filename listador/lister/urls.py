from django.urls import path
from .views import lista, Detalles, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('ingresar/', CustomLoginView.as_view(), name='ingresar'),
    path('salir/', LogoutView.as_view(next_page='ingresar'), name='salir'),
    path('registro/', RegisterPage.as_view(), name='registro' ),

    path('', lista.as_view(), name="tareas"),
    path('task/<int:pk>/', Detalles.as_view(), name="tarea"),
    path('task-create/', TaskCreate.as_view(), name="task-create"),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name="task-update"),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name="task-delete"),
]