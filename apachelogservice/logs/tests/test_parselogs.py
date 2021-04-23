import logging
from io import StringIO

from logs.management.commands.parselogs import Command

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, SimpleTestCase


class SimpleLogParserTest(SimpleTestCase):

    def setUp(self):
        self.invalid_download = 'http://google.com/nowhere'
        self.invalid_url = 'google.com'
        self.url = 'http://www.almhuette-raith.at/apache-log/access.log'

    def test_invalid_url(self):
        with self.assertRaises(CommandError, msg='Given URL is not valid'):
            Command().validate_url(self.invalid_url)

    def test_valid_url(self):
        result = Command().validate_url(self.url)
        self.assertEqual(result, self.url)

    def test_download_fail(self):
        with self.assertRaises(CommandError, msg='HTTP Error 404: Not Found'):
            logging.disable(logging.CRITICAL)
            Command().download_file(self.invalid_download)


class LogParserTest(TestCase):

    def setUp(self):
        self.url = 'http://www.almhuette-raith.at/apache-log/access.log'

    def log_call_command(self, *args, **kwargs):
        out = StringIO()
        call_command(
            'parselogs',
            self.url,
            *args,
            stdout=out,
            stderr=out,
        )
        return out.getvalue()

    def test_parselogs(self):
        out = self.log_call_command()
        self.assertIn('Saved logs to DB', out)
