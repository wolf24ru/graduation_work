import re


def phon_valid(phone_namer: str):
    regex = '^(\+?7|8)?[\D\s-]?[\(]?(?P<ph1>\d{3})[\)]?[\D\s-]?(?P<ph2>\d{3})[\D\s-]?(?P<ph3>\d{2})[\D\s-]?(?P<ph4>\d{2})$'
    if phone_namer:
        pre = re.search(regex, phone_namer)
        if pre:
            final_phone_number = f'+7 ({pre.group("ph1")}) {pre.group("ph2")}-{pre.group("ph3")}-{pre.group("ph4")}'
            return final_phone_number
        else:
            return None
    return None
