import os
import re
import sys

import django
from django.template import Context, Template


def camelcase2snakecase(s: str) -> str:
    "Converts CamelCase to snake-case, ie. CamelCase -> camel_case"
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()


def find_files(folder: str, extensions=None):
    "Finds files in a given folder, including subfolders, according to a list of file extensions"
    if not extensions:
        extensions = []
    for root, _, files in os.walk(folder):
        for file in files:
            if not extensions or os.path.splitext(file)[-1].lower() in extensions:
                return os.path.join(root, file)


def content_replacement(filename, context=None):
    template = Template(open(filename).read())
    open(filename, "w").write(template.render(Context(context or {})))


def render_template(template_as_string: str, context) -> str:
    return (
        Template(template_as_string)
        .render(Context(context or {}))
        .replace("[[", "{")
        .replace("]]", "}")
    )


def create_content(template_as_string, filename, context=None, append=False):
    open(filename, append and "a" or "w").write(
        render_template(template_as_string, context or {})
    )


def getdbfieldtype(simple_type: str) -> str:
    "Maps a simple type description to a django database field."
    defs = {
        "id": "models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)",
        "str": "models.CharField(max_length=50)",
        "int": "models.IntegerField()",
        "bool": "models.BooleanField(default=False)",
        "date": "models.DateField()",
        "datetime": "models.DateTimeField()",
        "email": "models.EmailField()",
        "url": "models.URLField()",
        "float": "models.FloatField()",
        "auto_now_add": "models.DateTimeField(auto_now_add=True)",
        "auto_now": "models.DateTimeField(auto_now=True)",
        "text": "models.TextField(null=True, blank=True)",
        "file": "models.FileField(upload_to='uploads/%Y/%m/%d/')",
        "image": "models.ImageField(upload_to='uploads/%Y/%m/%d/')",
        "slug": "models.SlugField()",
        "time": "models.TimeField(auto_now=False, auto_now_add=False)",
    }

    if simple_type in defs:
        return defs[simple_type]

    raise SystemError("%s not supported as field type." % simple_type)


def getdataclassfieldtype(simple_type: str) -> str:
    "Maps a simple type description to a dataclass attribute type."
    defs = {
        "id": "uuid.uuid4",
        "str": "str",
        "int": "int",
        "bool": "bool",
        "date": "datetime.date",
        "datetime": "datetime.datetime",
        "email": "str",
        "url": "str",
        "float": "float",
        "auto_now_add": "datetime.datetime = datetime.datetime.today()",
        "auto_now": "datetime.datetime = datetime.datetime.today()",
        "text": "str",
        "file": "BinaryIO # from typing import BinaryIO/TextIO",
        "image": "Image",
        "slug": "str",
        "time": "datetime.time",
    }

    if simple_type in defs:
        return defs[simple_type]

    raise SystemError("%s not supported as field type." % simple_type)


def configure_django_environ(folder):
    "Configures the django environment based on the location of the manage.py file."
    manage_py_file = os.path.join(folder, "manage.py")
    if not os.path.exists(manage_py_file):
        raise SystemError("Manage.py was not found in the current folder")

    correct_line = next(
        (
            (
                line
                for line in open(manage_py_file).readlines()
                if "os.environ.setdefault" in line
            )
        ),
        None,
    )

    if not correct_line:
        raise SystemError(
            "Could not parse manage.py to find correct django environment."
        )

    settings_folder = (
        correct_line.strip()
        .replace("os.environ.setdefault('DJANGO_SETTINGS_MODULE', '", "")
        .replace(".settings')", "")
    )

    sys.path.append(folder)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings" % settings_folder)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    django.setup()


class Field:
    "A special kind of field, representing both a database model and a dataclass"

    def __init__(self, init_string: str):
        self.name, value = [k.strip() for k in init_string.split(":")]
        self.type = value
        self.db_fieldtype = getdbfieldtype(value)
        self.dataclass_attribute = getdataclassfieldtype(value)
        self.searchable = self.type == "str"
        self.filter_field = self.type == "bool"
        self.date_field = value in ["date", "datetime", "auto_now", "auto_now_add"]
        self.editable = value not in ["auto_now", "auto_now_add"]

    def __str__(self):
        return f"<{self.name} ({self.type})>"

    def __repr__(self):
        return f"<{self.name} ({self.type})>"

    def dump(self):
        return f"""
Name: {self.name}
Type: {self.type}
Database fieldtype: {self.db_fieldtype}
Dataclass fieldtype: {self.dataclass_attribute}
Searchable: {self.searchable}
Filter field: {self.filter_field}
Date field: {self.date_field}
"""
