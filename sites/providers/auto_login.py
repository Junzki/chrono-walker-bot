# -*- coding:utf-8 -*-
import logging
import typing as ty

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from sites.models import Site, SiteAccessRecord


class AutoLoginProvider(object):

    def __init__(self, preserve_driver: bool = False,
                 lazy: bool = False):
        self.preserve_driver = preserve_driver
        if not lazy:
            self.init_driver()
        else:
            self.driver = None

    def init_driver(self):
        options = FirefoxOptions()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

    def access(self, site: Site):
        if not self.driver:
            self.init_driver()

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
        if not self.driver:
            self.init_driver()

        try:
            self._automate(site)
        finally:
            if not self.preserve_driver:
                self.driver.quit()

    def batch_handle(self, site_id_list: ty.List[int],
                     shutdown_on_finish: bool = True):
        if not self.driver:
            self.init_driver()

        try:
            sites = Site.objects.filter(pk__in=site_id_list)

            for site in sites:
                logging.info("Checking %s" % site.name)
                self.automate(site)
                logging.info("Checking %s ... OK" % site.name)
        finally:
            if shutdown_on_finish:
                self.shutdown()

    def shutdown(self):
        if self.driver:
            self.driver.quit()
