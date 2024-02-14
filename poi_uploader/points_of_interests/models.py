from django.db import models
from django.contrib.postgres import fields


class Poi(models.Model):
    """Point of Interest - represent a place in the world"""
    internal_id = models.AutoField(primary_key=True, db_index=True)
    external_id = models.CharField(max_length=254, db_index=True)
    name = models.CharField(max_length=254)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    category = models.ForeignKey('Category', on_delete=models.RESTRICT)
    ratings = fields.ArrayField(models.FloatField(), default=list)
    # TODO: add avg_rating field as computational field
    description = models.TextField(blank=True, null=True)


class Category(models.Model):
    """Category - represent a category for a point of interest"""
    name = models.CharField(max_length=254, unique=True, db_index=True)
