from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from {{app_name}}.models.{{snake_case_model_name}} import {{model_name}}


@method_decorator(login_required, name="dispatch")
class {{model_name}}ListView(ListView):

    model = {{model_name}}
    template_name = "{{app_name}}/{{snake_case_model_name}}/list.html"
    context_object_name = "{{snake_case_model_name}}s"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = self.get_queryset()
        page = self.request.GET.get("page")
        paginator = Paginator(object_list, self.paginate_by)
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        context[self.context_object_name] = object_list
        return context



@method_decorator(login_required, name='dispatch')
class {{model_name}}CreateView(CreateView):
    model = {{model_name}}
    template_name = '{{app_name}}/{{snake_case_model_name}}/create.html'
    fields = ({% for field in fields %}{% if field.editable %}'{{field.name}}',{% endif %}{% endfor %} )
    success_url = reverse_lazy('{{app_name}}:{{snake_case_model_name}}-list')


@method_decorator(login_required, name='dispatch')
class {{model_name}}DetailView(DetailView):
    model = {{model_name}}
    template_name = '{{app_name}}/{{snake_case_model_name}}/detail.html'
    context_object_name = '{{snake_case_model_name}}'



@method_decorator(login_required, name='dispatch')
class {{model_name}}UpdateView(UpdateView):
    model = {{model_name}}
    template_name = '{{app_name}}/{{snake_case_model_name}}/update.html'
    context_object_name = '{{snake_case_model_name}}'
    fields = ({% for field in fields %}{% if field.editable %}'{{field.name}}',{% endif %}{% endfor %} )

    def get_success_url(self):
        return reverse_lazy('{{app_name}}:{{snake_case_model_name}}-list')
        #return reverse_lazy('{{app_name}}:{{snake_case_model_name}}-detail', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class {{model_name}}DeleteView(DeleteView):
    model = {{model_name}}
    template_name = '{{app_name}}/{{snake_case_model_name}}/delete.html'
    success_url = reverse_lazy('{{app_name}}:{{snake_case_model_name}}-list')
