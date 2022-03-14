import uuid

from django.db import models


class {{model_name}}Manager(models.Manager):
    """ """

    def get_queryset(self):
        return super().get_queryset()


class {{model_name}}(models.Model):
    """ """

    {% for field in fields %}{{field.name}} = {{field.db_fieldtype}}
    {% endfor %}

    objects = {{model_name}}Manager()
    
    class Meta:
        verbose_name = '{{model_name|lower}}'
        verbose_name_plural = '{{model_name|lower}}s'
