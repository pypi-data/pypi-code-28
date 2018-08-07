from django.contrib import admin


class RaceRatingAdmin(admin.ModelAdmin):
    autocomplete_fields = ('race', )
    search_fields = ('race__label', )
    list_display = ('race', 'category', 'created_date')
    ordering = ('race__office__label', 'created_date')
