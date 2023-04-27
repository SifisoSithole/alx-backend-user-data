#!/usr/bin/env python3
"""
This module obfuscate sensitive information
"""
import logging
import re
from typing import List, Tuple
from os import getenv
import mysql.connector

PII_FIELDS: Tuple[str] = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """
    returns an obfuscated log message

    Arguments:
        fields (list): a list of strings representing all fields to obfuscate
        redaction (str): a string representing by what the
                         field will be obfuscated
        message (str): a string representing the log line
        separator (str): a string representing by which character is
                         separating all fields in the log line
    Return:
        (str): obfuscated log message
    """
    for field in fields:
        message = re.sub(rf'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}',
                         message)
    return message


def get_logger() -> logging.Logger:
    """
    returns a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    returns a connector to the database
    """
    username = getenv('PERSONAL_DATA_DB_USERNAME', default='root')
    password = getenv('PERSONAL_DATA_DB_PASSWORD', default='')
    host = getenv('PERSONAL_DATA_DB_HOST', default='localhost')
    database = getenv('PERSONAL_DATA_DB_NAME')
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initialize class"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        filter values in incoming log records using filter_datum
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
