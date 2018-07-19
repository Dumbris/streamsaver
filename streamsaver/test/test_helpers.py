import unittest
from time import sleep
from streamsaver.helpers import elmake, element_make_from_uri

VALID_URI = ["udp://localhost:6002", "tcp://localhost:6003", "file:///tmp/out.mp4", "rtsp://rtsp.localhost/movie.mp4"]
NOT_VALID_URI = [None, "", "test", 42, "1tcp://localhost:6003", "up://:6002"]

class TestHelpers(unittest.TestCase):
    def test_element_make_from_uri(self):
        for uri in VALID_URI:
            el = element_make_from_uri(uri)
            self.assertNotEqual(el, None)

    def test_element_make_from_uri_negative(self):
        with self.assertRaises(TypeError):
            element_make_from_uri(None)

        with self.assertRaises(Exception):
            self.assertEqual(element_make_from_uri(""), None)
        with self.assertRaises(TypeError):
            self.assertEqual(element_make_from_uri(42), None)
        with self.assertRaises(Exception):
            self.assertEqual(element_make_from_uri("test"), None)
        with self.assertRaises(Exception):
            self.assertEqual(element_make_from_uri("1tcp://localhost:6003"), None)
        with self.assertRaises(Exception):
            self.assertEqual(element_make_from_uri("up://:6002"), None)

    def test_elmake(self):
        self.assertNotEqual(elmake("fakesrc"), None)
        self.assertNotEqual(elmake("fakesrc", filltype="zero"), None)
        self.assertNotEqual(elmake("fakesrc", asdict={"is-live": True}), None)

    def test_elmake_negative(self):
        with self.assertRaises(Exception):
            elmake("")
        with self.assertRaises(Exception):
            elmake("okthen")
        with self.assertRaises(TypeError):
            elmake("fakesrc", num=1)
        