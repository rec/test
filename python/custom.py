from typing_extensions import Annotated

from pydantic import (
    AfterValidator,
    PlainSerializer,
    TypeAdapter,
    WithJsonSchema,
)


class MyType:
    def __init__(self, value: str) -> None:
        self.value = value


TruncatedFloat = Annotated[
    float,
    AfterValidator(lambda x: round(x, 1)),
    PlainSerializer(lambda x: f'{x:.1e}', return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization'),
]


ta = TypeAdapter(TruncatedFloat)

input = 1.02345
assert input != 1.0

assert ta.validate_python(input) == 1.0

assert ta.dump_json(input) == b'"1.0e+00"'

assert ta.json_schema(mode='validation') == {'type': 'number'}
assert ta.json_schema(mode='serialization') == {'type': 'string'}
