from streamsaver.pipeline import GstPipeline, gi, GObject, Gst
from streamsaver.helpers import elmake, element_make_from_uri
import numpy as np


class Rtp2app(Gst.Bin):
    """Bin for calc mean of pixels in h264 video
    """
    def __init__(self):
        super(Rtp2app, self).__init__()

        # Create elements
        depay = elmake('rtph264depay', None)
        decoder = elmake('decodebin', None)
        self.appsink = elmake('appsink', 'appsink', 
                        asdict={"max-buffers":3000, 'emit-signals':True, 'sync':False}
                        )

        self.appsink.connect('new-sample', self.on_new_buffer)  # connect signal to callable func

        els = (depay, decoder, self.appsink)
        # Add elements to Bin
        for item in els:
            self.add(item)

        depay.link(decoder)

        decoder.connect("pad-added", self.decodebin_pad_added)

        # Add Ghost Pads
        self.add_pad(
            Gst.GhostPad.new('sink', depay.get_static_pad('sink'))
        )

    def decodebin_pad_added(self, element, pad):
        string = pad.query_caps(None).to_string()
        if string.startswith('video/x-raw'):
            pad.link(self.appsink.get_static_pad('sink'))

    def on_new_buffer(self, appsink):
        """Handler for raw byte stream
        """
        sample = appsink.emit('pull-sample')
        # get the buffer
        buf = sample.get_buffer()
        # extract data stream as string
        data = buf.extract_dup(0, buf.get_size())
        # convert data form string to numpy array
        stream = np.fromstring(data, np.uint8)  
        #just print mean value        
        print(np.mean(stream), stream.shape)
        return False


if __name__ == "__main__":
    src = element_make_from_uri("udp://localhost:6002")
    if not src:
        raise Exception("Invalid source for URI")

    src.set_property("num-buffers", 3000)
    client = GstPipeline(src, Rtp2app())
    client.run()