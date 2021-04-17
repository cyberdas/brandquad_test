from django.test import TestCase


class LogParseTest(TestCase):

    @classmethod
    def setUpclass(cls):
        super().setUpClass()
        pass # create url
        # test wrong url, test save_to_db, test_save_file