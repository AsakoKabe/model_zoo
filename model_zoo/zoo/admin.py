from django.contrib import admin

from .models import ModelCV, RequestCV


@admin.register(ModelCV)
class ModelCVAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'content')


@admin.register(RequestCV)
class RequestCVVAdmin(admin.ModelAdmin):
    list_display = ('id', 'input_img', 'output_img', 'created_at', 'model')
    list_display_links = ('id',)
    search_fields = ('id', 'content')
