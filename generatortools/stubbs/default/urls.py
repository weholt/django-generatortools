
from .views.{{snake_case_model_name}} import ({{model_name}}CreateView,
                                              {{model_name}}DeleteView,
                                              {{model_name}}DetailView,
                                              {{model_name}}ListView,
                                              {{model_name}}UpdateView)

urlpatterns = [
    path('{{snake_case_model_name}}/', {{model_name}}ListView.as_view(), name='{{snake_case_model_name}}_list'),
    path('{{snake_case_model_name}}/create', {{model_name}}CreateView.as_view(), name='{{snake_case_model_name}}_create'),    
    path('{{snake_case_model_name}}/<uuid:pk>', {{model_name}}DetailView.as_view(), name='{{snake_case_model_name}}_detail'),
    path('{{snake_case_model_name}}/<uuid:pk>/update', {{model_name}}UpdateView.as_view(), name='{{snake_case_model_name}}_update'),
    path('{{snake_case_model_name}}/<uuid:pk>/delete', {{model_name}}DeleteView.as_view(), name='{{snake_case_model_name}}_delete')
]
