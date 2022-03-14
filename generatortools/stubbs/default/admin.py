
from {{app_name}}.models.{{snake_case_model_name}} import {{model_name}}


@admin.register({{model_name}})
class {{model_name}}Admin(admin.ModelAdmin):
    """
    The admin model for {{model_name}}.
    """
    list_display = ({% for field in fields %}'{{field.name}}', {% endfor %} )
    {% if filter_fields %}list_filter = ({% for field in filter_fields %}'{{field}}', {% endfor %} ){% endif %}
    {% if searchable_fields %}search_fields = ({% for field in searchable_fields %}'{{field}}', {% endfor %} ){% endif %}
    {% if date_hierarchy_field %}date_hierarchy = '{{date_hierarchy_field}}'{% endif %}

    #def save_model(self, request, obj, form, change):
    #    obj.user = request.user
    #    super().save_model(request, obj, form, change)
