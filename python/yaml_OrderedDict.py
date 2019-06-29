#!/usr/bin/env python
from collections import OrderedDict
import yaml

# try to use LibYAML bindings if possible
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from yaml.representer import SafeRepresenter
_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG


def dict_representer(dumper, data):
    return dumper.represent_dict(data.items())


def dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))

Dumper.add_representer(OrderedDict, dict_representer)
Loader.add_constructor(_mapping_tag, dict_constructor)

Dumper.add_representer(str,
                       SafeRepresenter.represent_str)

yml_dict = OrderedDict(
    abc=OrderedDict(
        [('x', OrderedDict([(0, None)])), ('y', OrderedDict([(1, None)]))]))

import json
print(json.dumps(yml_dict, indent=2))
print

# dump ordereddict to yaml
output = yaml.dump(yml_dict, Dumper=Dumper, default_flow_style=False)
print(output)

# directly write to a file object to save memory.
with open('result.yml', 'w') as f:
    yaml.dump(yml_dict, f, Dumper=Dumper, default_flow_style=False)


with open('result.yml') as f:
    print(yaml.load(f, Loader=Loader))
