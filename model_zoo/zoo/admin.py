from django.contrib import admin

from .models import ModelCV, RequestCV


class ModelCVAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'content')


class RequestCVVAdmin(admin.ModelAdmin):
    list_display = ('id', 'input_img', 'response', 'created_at', 'model')
    list_display_links = ('id',)
    search_fields = ('id', 'content')


admin.site.register(ModelCV, ModelCVAdmin)
admin.site.register(RequestCV, RequestCVVAdmin)
