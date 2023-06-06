# -*- coding: utf-8 -*-
from django.contrib import admin
from worker.provider import WorkPublisher
from .models import Site, SiteCookie, SiteAccessRecord
from .providers.auto_login import AutoLoginProvider


class CookiesInline(admin.TabularInline):
    model = SiteCookie
    fields = ('key', 'value', 'domain', 'expiry')
    extra = 1


class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'created_at', 'updated_at')
    inlines = (CookiesInline,)
    search_fields = ('name', 'url')

    def automate_sites(self, request, queryset):
        publisher = WorkPublisher()
        p = AutoLoginProvider(lazy=True)
        site_id_list = [site.id for site in queryset]

        options = dict()
        kwargs = dict(
            site_id_list=site_id_list,
            shutdown_on_finish=True
        )

        publisher.publish(p.batch_handle, options, **kwargs)

    automate_sites.description = 'Automate selected sites'

    actions = [automate_sites, ]


class SiteAutomationRecord(admin.ModelAdmin):
    list_display = ('site', 'succeed', 'checked_in', 'uploaded', 'downloaded', 'bonus', 'active_uploads',
                    'active_downloads', 'created_at')
    ordering = ('-id', )


admin.site.register(Site, SiteAdmin)
admin.site.register(SiteAccessRecord, SiteAutomationRecord)
