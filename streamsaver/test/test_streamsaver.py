import unittest
from streamsaver.pipeline import Rtp2mp4, Rtp2jpeg, GstPipeline
from streamsaver.helpers import elmake
from gi.repository import GObject, Gst
from time import sleep

class TestBins(unittest.TestCase):
    def test_jpeg(self):
        client = GstPipeline(elmake("fakesrc", asdict={"num-buffers": 100}),
                            Rtp2jpeg(),
                            elmake("fakesink")
                            )
        client.pipeline.set_state(Gst.State.PLAYING)
        sleep(0.1)
        client.pipeline.send_event(Gst.Event.new_eos())

    def test_mp4(self):
        client = GstPipeline(elmake("fakesrc", asdict={"num-buffers": 100}),
                            Rtp2mp4(),
                            elmake("fakesink")
                            )
        client.pipeline.set_state(Gst.State.PLAYING)
        sleep(0.1)
        client.pipeline.send_event(Gst.Event.new_eos())