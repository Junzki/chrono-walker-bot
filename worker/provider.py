# -*- coding:utf-8 -*-
import os.path
import typing as ty
import pickle

from django.conf import settings


class WorkPublisher(object):

    def __init__(self):
        self.fifo_file = settings.FIFO_FILE

    def publish(self, func: callable, options: ty.Dict[str, ty.Any] | None, **kwargs):
        if not os.path.exists(self.fifo_file):
            raise FileNotFoundError("Worker not initialized")

        klass = func.__self__.__class__
        mod = klass.__module__
        klass_name = klass.__name__
        method_name = func.__name__

        task = dict(
            provider=f'{mod}.{klass_name}',
            method=method_name,
            options=options or dict(),
            kwargs=kwargs
        )

        with open(self.fifo_file, 'wb') as fifo:
            fifo.write(pickle.dumps(task))
