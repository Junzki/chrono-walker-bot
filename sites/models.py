from django.db import models
from django.utils.translation import gettext_lazy as _


class Site(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Site Name"))
    url = models.URLField(null=True, default=None, verbose_name=_("URL"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    def __str__(self):
        return f'Site: {self.name}'


class SiteCookie(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='cookies', verbose_name=_("Site"))
    key = models.CharField(max_length=255, null=False, blank=False, verbose_name=_("Cookie Key"))
    value = models.CharField(max_length=255, null=False, blank=False, verbose_name=_("Cookie Value"))
    domain = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Cookie Domain"))
    expiry = models.DateTimeField(null=True, blank=True, verbose_name=_("Cookie Expiry"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cookie: {self.key}'


class SiteAccessRecord(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='access_records', verbose_name=_("Site"))
    succeed = models.BooleanField(default=False, verbose_name=_("Succeed"))
    checked_in = models.BooleanField(default=False, verbose_name=_("Checked in"))

    uploaded = models.FloatField(default=0, verbose_name=_("Uploaded"))
    downloaded = models.FloatField(default=0, verbose_name=_("Downloaded"))
    bonus = models.FloatField(default=0, verbose_name=_("Bonus"))

    active_uploads = models.IntegerField(default=0, verbose_name=_("Active Uploads"))
    active_downloads = models.IntegerField(default=0, verbose_name=_("Active Downloads"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    def __str__(self):
        return f'Access Record: {self.site_id} -> {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'
