from django.contrib import admin

#se importan los modelos del directorio actual
from . import models

#se registran los modelos en el admin de django
admin.site.register(models.Producto)
admin.site.register(models.Product)
admin.site.register(models.Bowl)
admin.site.register(models.ProteinaBowl)
admin.site.register(models.BaseBowl)
admin.site.register(models.ExtraBowl)
admin.site.register(models.SalsaBowl)
admin.site.register(models.Handroll)
admin.site.register(models.ProteinaHandroll)
admin.site.register(models.VegetalesHandroll)
admin.site.register(models.HandrollReady)
admin.site.register(models.Kai)
admin.site.register(models.CorteKai)
admin.site.register(models.ExtraKai)
admin.site.register(models.Selladitas)
admin.site.register(models.VegetalesDesayuno)
admin.site.register(models.ProteinaDesayuno)
admin.site.register(models.QuesoDesayuno)
admin.site.register(models.Desayuno)
admin.site.register(models.Almuerzo)
admin.site.register(models.AgregadoAlmuerzo)
admin.site.register(models.ProteinaAlmuerzo)
admin.site.register(models.Comanda)
admin.site.register(models.Article)
