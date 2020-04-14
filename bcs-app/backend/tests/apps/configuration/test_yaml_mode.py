# -*- coding: utf-8 -*-
from django.test import TestCase

from backend.apps.configuration.yaml_mode.release import ReleaseDataProcessor


class YAMLTemplateSetsTestCase(TestCase):

    def setUp(self):
        self.user = ''

    def test_process_release_data_by_data_processor(self):
        ReleaseDataProcessor(self.user, None)
