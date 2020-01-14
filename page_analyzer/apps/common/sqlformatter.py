import logging

import sqlparse
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.sql import SqlLexer

from django.conf import settings

TIME_CRIT = 0.2
TIME_WARN = 0.05
TIME_FORMAT = u'\x1b[0;30;{bgcolor}m {duration:.3f}s \x1b[0m\n{msg}'

LEXER = SqlLexer()
FORMATTER = Terminal256Formatter(style=settings.SQL_FORMATTER_STYLE)


class SqlFormatter(logging.Formatter):
    def format(self, record):
        try:
            sql = record.sql.strip()
            duration = record.duration
        except AttributeError:
            return super(SqlFormatter, self).format(record)

        sql = sqlparse.format(sql, reindent=True, keyword_case='upper')
        bgcolor = 41 if duration > TIME_CRIT else 43 if duration > TIME_WARN else 42

        return TIME_FORMAT.format(bgcolor=bgcolor, duration=duration, msg=highlight(sql, LEXER, FORMATTER))
