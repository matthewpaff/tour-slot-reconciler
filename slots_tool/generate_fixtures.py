"""Original case templates with independently supplied expected results."""
import copy
import re

TEMPLATES = [('retain a nonexpired supplied slot snapshot', {'now': 150, 'slots': [{'id': 's{n}', 'start': 200, 'end': 300, 'expires_at': 180, 'version': 1}]}, {'slots': [{'id': 's{n}', 'start': 200, 'end': 300, 'expires_at': 180, 'version': 1}]}), ('do not resurrect an older fresh slot after a newer version expires', {'now': 150, 'slots': [{'id': 's{n}', 'start': 200, 'end': 300, 'expires_at': 180, 'version': 1}, {'id': 's{n}', 'start': 200, 'end': 300, 'expires_at': 149, 'version': 2}]}, {'slots': []}), ('discard a slot at its exact expiry boundary', {'now': 180, 'slots': [{'id': 's{n}', 'start': 200, 'end': 300, 'expires_at': 180, 'version': 1}]}, {'slots': []}), ('reject conflicting equal-version slot snapshots', {'now': 0, 'slots': [{'id': 's{n}', 'start': 200, 'end': 300, 'expires_at': 180, 'version': 1}, {'id': 's{n}', 'start': 201, 'end': 300, 'expires_at': 180, 'version': 1}]}, None), ('reject nonpositive slot intervals', {'now': 0, 'slots': [{'id': 's{n}', 'start': 200, 'end': 200, 'expires_at': 180, 'version': 1}]}, None)]


def make_case(index):
    description, source, expected = copy.deepcopy(TEMPLATES[index % len(TEMPLATES)])
    def fill(value):
        if isinstance(value, str):
            if re.fullmatch(r"@i[+]\d+", value):
                return index + int(value[3:])
            return value.replace("{n}", str(index))
        if isinstance(value, list):
            return [fill(item) for item in value]
        if isinstance(value, dict):
            return {fill(key): fill(item) for key, item in value.items()}
        return value
    case = {"id": "slots-{:04d}".format(index), "description": description, "input": fill(source)}
    case.update({"expected_error": True} if expected is None else {"expected": fill(expected)})
    return case
