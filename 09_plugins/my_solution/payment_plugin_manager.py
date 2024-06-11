from decimal import Decimal
import importlib
import os
from typing import Protocol
from importlib.util import module_from_spec, spec_from_file_location


class PaymentPlugin(Protocol):
    def payment_method_name(self) -> str:
        ...

    def process_payment(self, total: Decimal) -> None:
        ...

PLUGINS: dict[str, PaymentPlugin] = {}

def load_plugins():
    for root, _, files in os.walk("09_plugins/my_solution/payment_plugins"):
        for file in files:
            if file.endswith(".py"):
                module_name = file[:-3]
                module_path = os.path.join(root, file)
                m = import_module(module_name, module_path)
                PLUGINS[m.payment_method_name()] = m

def import_module(name: str, path: str) -> PaymentPlugin:
    spec = spec_from_file_location(name, path)
    if spec:
        module: PaymentPlugin = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    raise ImportError(f"Could not import {name} from {path}")
    
def plugin_names():
    return list(PLUGINS.keys())

def get_plugin(name: str):
    return PLUGINS[name]