from . parser import Parser
from . import table


class McMasterParser(Parser):
    def parse(self, tokens):
        tables = table(tokens.tree)
        return {
            'tables': len(tables),
            'captions': [t.caption for t in tables],
        }
