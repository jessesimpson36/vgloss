import unittest

from django.test import TestCase

from vgloss import models, scan
from tests import testdata

class TestScan(TestCase):

    def setUp(self):
        testdata.clean()

    def tearDown(self):
        testdata.clean()

    def test_scan(self):
        testdata.basic_data()
        scan.scan_all()

        black_square = models.FilePath.objects.get(path="black_square.jpg")
        black_square2 = models.FilePath.objects.get(path="black_square2.jpg")
        white_square = models.FilePath.objects.get(path="white_square.jpg")
        self.assertEqual(black_square.file, black_square2.file)
        self.assertNotEqual(white_square.file, black_square.file)

        metadata = white_square.file.metadata
        self.assertEqual(metadata["BitsPerSample"], 8)
        self.assertEqual(metadata["ColorComponents"], 3)

    @unittest.skip("Test not implemented")
    def test_non_image_file(self):
        raise NotImplementedError()

    @unittest.skip("Test not implemented")
    def test_extract_timestamp(self):
        # From exif
        # From filename
        # From stat???
        raise NotImplementedError()

    @unittest.skip("Test not implemented")
    def test_image_types(self):
        # jpg, jpeg, png, gif, etc.
        raise NotImplementedError()

    @unittest.skip("Test not implemented")
    def test_versions(self):
        raise NotImplementedError()