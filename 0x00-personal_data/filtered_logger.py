#!/usr/bin/env python3
"""I think logging is important sometimes"""
from typing import List
import re
import logging
import os
import mysql.connector
PII_FIELDS = ('name', 'email', 'password', 'ssn', 'phone')


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
        ) -> str:
    """A function to expresss yourself"""
    pattern = f"({'|'.join(map(re.escape, fields))})=[^{separator}]*"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)


def get_logger() -> logging.Logger:
    """Logger getter"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Database connector"""
    db_name = os.get('PERSONAL_DATA_DB_NAME', '')
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD ', '')
    db_host = os.getenv('and PERSONAL_DATA_DB_HOST', 'localhost')
    config = {
        'host': db_host,
        'user': db_username,
        'password': db_password,
        'database': db_name,
        'port': 3306
    }
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error as error:
        print("Couldn't connect")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Do you think we have to do this"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Some documentation is here"""
        record.asctime = self.formatTime(record, self.datefmt)
        msg = filter_datum(self.fields, RedactingFormatter.REDACTION,
                           record.msg, RedactingFormatter.SEPARATOR)
        return f'[HOLBERTON] {record.name} \
{record.levelname} {record.asctime}: {msg}'
