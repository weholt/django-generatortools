#!/usr/bin/env python
__version__ = "0.1.0"

import os

import click as click

from generatortools.utils import (
    camelcase2snakecase,
    configure_django_environ,
    create_content,
    getdataclassfieldtype,
    getdbfieldtype,
)


@click.argument("model_name")
@click.argument("app_name")
@click.option("--field", "-f", multiple=True)
@click.command()
def main(app_name, model_name, field=None):
    """
    Will create a model, including views, templates and urlpatterns, for a given app.
    """
    generatortools_path = os.sep.join(__file__.split(os.sep)[:-2])
    configure_django_environ(os.getcwd())
    from django.apps import apps

    snake_case_model_name = camelcase2snakecase(model_name)
    fields = []
    for f in field:
        name, value = [k.strip() for k in f.split(":")]
        fields.append(
            {
                "name": name,
                "type": value,
                "db_fieldtype": getdbfieldtype(value),
                "dataclass_attribute": getdataclassfieldtype(value),
            }
        )

    date_hierarchy_field = next(
        (
            x["name"]
            for x in fields
            if x["type"] in ["date", "datetime", "auto_now_add", "auto_now"]
        ),
        None,
    )

    searchable_fields = [f["name"] for f in fields if f["type"] == "str"]
    filter_fields = [f["name"] for f in fields if f["type"] == "bool"]

    context = {
        "custom_id": "id" in fields,
        "app_name": app_name,
        "model_name": model_name,
        "snake_case_model_name": snake_case_model_name,
        "fields": fields,
        "date_hierarchy_field": date_hierarchy_field,
        "searchable_fields": searchable_fields,
        "filter_fields": filter_fields,
    }

    if not model_name.isalnum():
        raise SystemError("Model names can only be alphanumeric characters.")

    existing_app = [app for app in apps.get_app_configs() if app.name == app_name]
    if not existing_app:
        raise SystemError("No app called %s" % app_name)

    app = existing_app[0]
    if model_name in [model.__name__ for model in app.get_models()]:
        raise SystemError(f"App {app_name} allready has a model called {model_name}.")

    models_folder = os.path.join(app.path, "models")
    if not os.path.exists(models_folder):
        raise SystemError(
            f"{app_name} does not have a models package. This is required."
        )

    model_file = os.path.join(models_folder, snake_case_model_name, ".py")
    if os.path.exists(model_file):
        raise SystemError(f"{app_name} allready has a model file for {model_name}.")

    views_folder = os.path.join(app.path, "views")
    if not os.path.exists(views_folder):
        raise SystemError(
            f"{app_name} does not have a views package. This is required."
        )

    view_file = os.path.join(views_folder, snake_case_model_name, ".py")
    if os.path.exists(view_file):
        raise SystemError(f"{app_name} allready has a view file for {model_name}.")

    urls_file = os.path.join(app.path, "urls.py")
    if not os.path.exists(urls_file):
        raise SystemError(f"{app_name} does not have a urls.py file. This is required.")

    admin_file = os.path.join(app.path, "admin.py")
    if not os.path.exists(admin_file):
        raise SystemError(
            f"{app_name} does not have a admin.py file. This is required."
        )

    template_folder = os.path.join(app.path, "templates", app_name)
    if os.path.exists(template_folder):
        raise SystemError(
            f"{app_name} allready has a folder for templates called {model_name}"
        )

    stubbs_folder = os.path.join(generatortools_path, "stubbs", "default")

    if not os.path.exists(stubbs_folder):
        raise SystemError("Missing expected subbs-folder at %s" % stubbs_folder)

    model_stubb = open(os.path.join(stubbs_folder, "model.py")).read()
    create_content(
        model_stubb,
        os.path.join(models_folder, "%s.py" % snake_case_model_name),
        context,
    )

    view_stubb = open(os.path.join(stubbs_folder, "views.py")).read()
    create_content(
        view_stubb,
        os.path.join(views_folder, "%s.py" % snake_case_model_name),
        context,
    )

    url_stubb = open(os.path.join(stubbs_folder, "urls.py")).read()
    create_content(url_stubb, urls_file, context, append=True)

    admin_stubb = open(os.path.join(stubbs_folder, "admin.py")).read()
    create_content(admin_stubb, admin_file, context, append=True)

    api_folder = os.path.join(app.path, "api")
    if os.path.exists(api_folder):
        api_stubb = open(os.path.join(stubbs_folder, "api.py")).read()
        create_content(
            api_stubb,
            os.path.join(api_folder, "%s.py" % snake_case_model_name),
            context,
        )

    import pprint

    pprint.pprint(context)

    os.system("black %s" % app.path)
    os.system("isort --atomic %s" % app.path)


if __name__ == "__main__":
    main()
