# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from worker.worker import Worker


class Command(BaseCommand):
    help = "Init worker"

    def add_arguments(self, parser):
        ...

    def handle(self, *args, **options):
        w = Worker()
        w.setup()
        w.spawn()

        w.tear_down()
