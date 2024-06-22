#!/usr/bin/env python3
"""I think logging is important sometimes"""
from typing import List
import re
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.asctime = self.formatTime(record, self.datefmt)
        msg = filter_datum(self.fields, RedactingFormatter.REDACTION,
                           record.msg, RedactingFormatter.SEPARATOR)
        msg = re.sub(';', '; ', msg)
        return f'[HOLBERTON] {record.name} \
{record.levelname} {record.asctime}: {msg}'


def filter_datum(fields: List[str],
                 redaction: str, message: str, separtor: str) -> str:
    pattern = f"({'|'.join(map(re.escape, fields))})=[^{separtor}]*"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)

# the_string_list = message.split(';')
# the_string_list.pop()
# final_string = ''
# elm_list = []
# for elm in the_string_list:
#     elm_list = elm.split('=')
#     if elm_list[0] in fields:
#         elm_list[1] = redaction
#     elm_list.insert(1, '=')
#     elm_list.append(separtor)
#     final_string = final_string + ''.join(elm_list)
# return final_string
