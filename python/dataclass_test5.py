from dataclasses import dataclass


class ConfigBase:
    def __setattr__(self, k, v):
        if not hasattr(self, k):
            raise AttributeError(f'{self} has no attribute "{k}"')
        super().__setattr__(k, v)

    def __post_init__(self):
        print('here')


@dataclass
class Data(ConfigBase):
    one: str = 'one'
