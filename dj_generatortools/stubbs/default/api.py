from typing import List
from uuid import uuid4

from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema
from {{app_name}}.models.{{snake_case_model_name}} import {{model_name}}

api = NinjaAPI()

class {{model_name}}In(Schema):
    {% for field in fields %}{{field.name}}: {{field.dataclass_attribute}}
    {% endfor %}


class {{model_name}}Out(Schema):
    {% if not custom_id %}id: int{% endif %}
    {% for field in fields %}{{field.name}}: {{field.dataclass_attribute}}
    {% endfor %}


@api.post("/{{snake_case_model_name}}s")
def create_{{snake_case_model_name}}(request, payload: {{model_name}}In):
    {{snake_case_model_name}} = {{model_name}}.objects.create(**payload.dict())
    return {"id": {{snake_case_model_name}}.id}


@api.get("/{{snake_case_model_name}}s/[[{{snake_case_model_name}}_id]]", response={{model_name}}Out)
def get_{{snake_case_model_name}}(request, {{snake_case_model_name}}_id: int):
    {{snake_case_model_name}} = get_object_or_404({{model_name}}, id={{snake_case_model_name}}_id)
    return {{snake_case_model_name}}


@api.get("/{{snake_case_model_name}}s", response=List[{{model_name}}Out])
def list_{{snake_case_model_name}}s(request):
    qs = {{model_name}}.objects.all()
    return qs


@api.put("/{{snake_case_model_name}}s/[[{{snake_case_model_name}}_id]]")
def update_{{snake_case_model_name}}(request, {{snake_case_model_name}}_id: int, payload: {{model_name}}In):
    {{snake_case_model_name}} = get_object_or_404({{model_name}}, id={{snake_case_model_name}}_id)
    for attr, value in payload.dict().items():
        setattr({{snake_case_model_name}}, attr, value)
    {{snake_case_model_name}}.save()
    return {"success": True}


@api.delete("/{{snake_case_model_name}}s/[[{{snake_case_model_name}}_id]]")
def delete_{{snake_case_model_name}}(request, {{snake_case_model_name}}_id: int):
    {{snake_case_model_name}} = get_object_or_404({{model_name}}, id={{snake_case_model_name}}_id)
    {{snake_case_model_name}}.delete()
    return {"success": True}
