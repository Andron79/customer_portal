import re


space_modifiers = " kMGTPEZY"
space_re = re.compile(fr"(?P<number>\d+(.\d+)?)(?P<modifier>[{space_modifiers}]|$)")


def convert_file_size_str_to_num(value: str, default: int = 0) -> int:
    if not value:
        return default
    if not (requirement := space_re.match(value)):
        raise ValueError(f"'{value}' is not a valid space requirement")

    req_number = float(requirement.groupdict()['number'])
    if not (req_modifier := requirement.groupdict()['modifier'].strip()):
        return int(req_number)

    for _modifier in space_modifiers:
        if _modifier == req_modifier:
            return int(req_number)
        req_number *= 1000

    raise ValueError(f"Unknown modifier: {req_modifier}")
