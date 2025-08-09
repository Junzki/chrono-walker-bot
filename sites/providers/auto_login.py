# -*- coding:utf-8 -*-
import typing as ty

from django.conf import settings
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from sites.models import Site, SiteAccessRecord


class AutoLoginProvider(object):

    def __init__(self, preserve_driver: bool = False):
        options = FirefoxOptions()
        options.headless = True

        service_kwargs = dict()
        if settings.GECKO_DRIVER_PATH:
            service_kwargs['executable_path'] = str(settings.GECKO_DRIVER_PATH)

        service = FirefoxService(**service_kwargs)

        self.driver = webdriver.Firefox(options=options, service=service)
        self.preserve_driver = preserve_driver

    def access(self, site: Site):
        url = site.url
        cookies = site.cookies.all()

        self.driver.get(url)

        for cookie in cookies:
            self.driver.add_cookie(dict(
                name=cookie.key,
                value=cookie.value,
                domain=cookie.domain
            ))

        self.driver.get(url)

    def check_logged_in(self) -> bool:
        try:
            self.driver.find_element('id', 'mainmenu')
        except selenium.common.exceptions.NoSuchElementException:
            return False

        return True


    def check_in(self) -> str | None:
        try:
            entry = self.driver.find_element('id', 'signed')
        except selenium.common.exceptions.NoSuchElementException:
            return

        entry.click()

        try:
            alert = self.driver.switch_to.alert
        except selenium.common.exceptions.NoAlertPresentException:
            return

        alert_text = alert.text
        alert.accept()
        return alert_text

    def check_checked_in(self) -> bool:
        try:
            self.driver.find_element('id', 'signed')
        except selenium.common.exceptions.NoSuchElementException:
            pass
        else:
            return False

        try:
            self.driver.find_element('id', 'sp_signed')
        except selenium.common.exceptions.NoSuchElementException:
            return False

        return True

    def _automate(self, site: Site):
        record = SiteAccessRecord.objects.create(site=site)

        self.access(site)

        record.succeed = self.check_logged_in()
        record.save()

        if not self.check_checked_in():
            self.check_in()

        checked = self.check_checked_in()
        record.succeed = True
        record.checked_in = checked
        record.save()

        site.save()  # Update updated_at

    def automate(self, site: Site):
        try:
            self._automate(site)
        finally:
            if not self.preserve_driver:
                self.driver.quit()

    def shutdown(self):
        self.driver.quit()