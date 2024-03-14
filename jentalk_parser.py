import re
from functools import reduce

class JentalkParser:
    def __init__(self):
        self.primitives = {
            'entity': r'∃',
            'animate_entity': r'∃°',
            'inanimate_entity': r'∃-',
            'action': r'>',
            'physical_action': r'>°',
            'mental_action': r'>^',
            'property': r'○',
            'physical_property': r'○°',
            'mental_property': r'○^',
            'relation': r'∆',
            'space': r'□',
            'absolute_space': r'□°',
            'relative_space': r'□^',
            'time': r'◊',
            'absolute_time': r'◊°',
            'relative_time': r'◊^'
        }
        
        self.modifiers = {
            'plural': r'\.{3}',
            'past': r'«',
            'present': r'\|',
            'future': r'»',
            'negation': r'¬',
            'intensifier': r'¡',
            'continuous': r'~'
        }

        self.continued_fraction_regex = re.compile(r'\[\[([0-9,]+)\]\]')

        self.primitive_regex = re.compile('|'.join(self.primitives.values()))
        self.modifier_regex = re.compile('|'.join(self.modifiers.values()))
        self.token_regex = re.compile(
            f"({'|'.join(map(re.escape, self.primitives.values()))})"
            f"({'|'.join(map(re.escape, self.modifiers.values()))})*"
        )

    def tokenize(self, expression):
        return self.token_regex.findall(expression)

    def parse_continued_fraction(self, expression):
        matches = self.continued_fraction_regex.findall(expression)
        for match in matches:
            numbers = list(map(int, match.split(',')))
            result = reduce(lambda acc, x: x + 1/acc, reversed(numbers[1:]), numbers[0])
            expression = expression.replace(f'[[{match}]]', str(result))
        return expression

    def parse(self, expression):
        expression = self.parse_continued_fraction(expression)
        lines = expression.split('\n')
        parsed_expressions = []
        for line in lines:
            line = line.strip()
            if line:
                tokens = self.tokenize(line)
                parsed_line = []
                for token in tokens:
                    if isinstance(token, tuple):
                        primitive = token[0]
                        modifiers = token[1:]
                        token_type = self.identify_token_type(primitive)
                        parsed_line.append((token_type, ''.join(token)))
                        for modifier in modifiers:
                            modifier_type = self.identify_modifier_type(modifier)
                            parsed_line.append((modifier_type, modifier))
                    else:
                        token_type = self.identify_token_type(token)
                        parsed_line.append((token_type, token))
                parsed_expressions.append(parsed_line)
        return parsed_expressions

    def identify_token_type(self, token):
        for name, regex in self.primitives.items():
            if re.match(regex, token):
                return name
        return 'UNKNOWN'

    def identify_modifier_type(self, modifier):
        for name, regex in self.modifiers.items():
            if re.match(regex, modifier):
                return name
        return 'UNKNOWN'