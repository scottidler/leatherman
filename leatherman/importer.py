#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import importlib.util


def import_modules(dirpath, endswith):
    files = [f for f in os.listdir(dirpath) if f.endswith(endswith)]
    modules = []
    for f in files:
        module_name = f.split(".")[0]
        file_path = os.path.join(dirpath, f)
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        modules.append(module)
    return modules

