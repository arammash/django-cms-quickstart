from django.contrib import admin

# Register your models here.
from .models import Artist, Exhibition, ExhibitionImage

class ExhibitionImageInline(admin.TabularInline):
    model = ExhibitionImage
    extra = 1

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ExhibitionImageInline]