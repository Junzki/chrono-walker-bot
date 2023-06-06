# -*- coding:utf-8 -*-
import importlib
import os
import typing as ty
import pickle
from concurrent.futures.thread import ThreadPoolExecutor
from django.conf import settings


class Worker(object):

    def __init__(self):
        self.pool = ThreadPoolExecutor(4)
        self.fifo_file = settings.FIFO_FILE
        self.alive = True
        self.fifo = None

    def setup(self):
        if not os.path.exists(self.fifo_file):
            os.mkfifo(self.fifo_file)

        self.fifo = open(self.fifo_file, 'rb')

    def tear_down(self):
        self.fifo.close()

    def spawn(self):
        while self.alive:
            data = self.fifo.read()
            if 0 == len(data):
                self.alive = False
                continue

            task = pickle.loads(data)
            provider_rel = task['provider']
            method_name = task['method']
            kwargs = task.get('kwargs', dict())

            self.pool.submit(self.task, **dict(
                provider_rel=provider_rel,
                method_name=method_name,
                kwargs=kwargs,
            ))

    @staticmethod
    def task(provider_rel: str, method_name: str,
             options: ty.Dict[str, str] | None = None,
             kwargs: ty.Dict[str, str] | None = None):
        mod, klass = provider_rel.rsplit('.', 1)
        mod = importlib.import_module(mod)

        klass = getattr(mod, klass)

        options = options or dict()
        provider = klass(**options)

        m = getattr(provider, method_name)

        kwargs = kwargs or dict()
        m(**kwargs)
