from django.contrib import admin

from .models import Ingredient, Recipe, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "measurement_unit",
    )
    search_fields = ("name",)
    empty_value_display = "-пусто-"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "color",
        "slug",
    )
    search_fields = ("name",)
    list_filter = (
        "name",
        "slug",
    )
    empty_value_display = "-пусто-"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "author",
        "text",
        "pub_date",
    )
    search_fields = ("name",)
    # list_filter = (
    #     "ingredients",
    #     "tags",
    # )
    empty_value_display = "-пусто-"
