from inject import Binder, Injector, clear_and_configure

from .environment import Settings


def _config(binder: Binder) -> Binder:
    return binder.bind(Settings, Settings())


def configure_inject() -> Injector:
    return clear_and_configure(_config)
