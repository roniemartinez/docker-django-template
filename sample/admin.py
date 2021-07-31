from django.contrib import admin
from django.contrib.sites.models import Site

admin.site.unregister(Site)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    fields = ("id", "name", "domain")
    readonly_fields = ("id",)
    list_display = ("id", "name", "domain")
    list_display_links = ("name",)
    search_fields = ("name", "domain")
