
from {{app_name}}.views.{{snake_case_model_name}} import (
    {{model_name}}CreateView, {{model_name}}DeleteView,
    {{model_name}}DetailView, {{model_name}}ListView, {{model_name}}UpdateView)

app_name = '{{app_name}}'


urlpatterns = [
    path('{{snake_case_model_name}}/', {{model_name}}ListView.as_view(), name='{{snake_case_model_name}}-list'),
    path('{{snake_case_model_name}}/create', {{model_name}}CreateView.as_view(), name='{{snake_case_model_name}}-create'),    
    path('{{snake_case_model_name}}/<{% if custom_id %}uuid{% else %}int{% endif %}:pk>', {{model_name}}DetailView.as_view(), name='{{snake_case_model_name}}-detail'),
    path('{{snake_case_model_name}}/<{% if custom_id %}uuid{% else %}int{% endif %}:pk>/update', {{model_name}}UpdateView.as_view(), name='{{snake_case_model_name}}-update'),
    path('{{snake_case_model_name}}/<{% if custom_id %}uuid{% else %}int{% endif %}:pk>/delete', {{model_name}}DeleteView.as_view(), name='{{snake_case_model_name}}-delete')
]
