import functools


class Singleton:
    @classmethod
    @functools.cache
    def _instance(cls):
