import inspect
import importlib
import reminisc.modules.abstract_module as am


def is_reminisc_module_implementation(obj):
    return (inspect.isclass(obj) and
            issubclass(obj, am.AbstractModule) and
            not inspect.isabstract(obj))


def find_reminisc_module_implementations(python_module_name):
    reminisc_module = importlib.import_module(python_module_name)
    return [cls for name, cls in inspect.getmembers(reminisc_module) if is_reminisc_module_implementation(cls)]