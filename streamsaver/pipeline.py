import time
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
from streamsaver.helpers import elmake, element_make_from_uri

#Warning: you need to initialize Gst object before using Gst.Bin as parent class
GObject.threads_init()
Gst.init(None)

CAPS = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96"


class Rtp2mp4(Gst.Bin):
    """Bin for h264 video convertation in to mp4 container
       Corresponds to "rtph264depay ! h264parse ! mp4mux" pipeline
    """
    def __init__(self):
        super(Rtp2mp4, self).__init__()

        # Create elements
        depay = elmake('rtph264depay', None)
        parser = elmake('h264parse', None)
        #muxer = elmake('mp4mux', None)
        muxer = elmake('matroskamux', None)

        # Add elements to Bin
        self.add(depay)
        self.add(parser)
        self.add(muxer)

        # Link elements
        depay.link(parser)
        parser.link(muxer)

        # Add Ghost Pads
        self.add_pad(
            Gst.GhostPad.new('sink', depay.get_static_pad('sink'))
        )
        self.add_pad(
            Gst.GhostPad.new('src', muxer.get_static_pad('src'))
        )


class Rtp2jpeg(Gst.Bin):
    """Bin for h264 video convertation in to mp4 container
       Corresponds to "rtph264depay ! decodebin ! videoconvert ! videoscale !
       videorate ! video/x-raw,framerate=1/10 ! queue leaky=2 max-size-buffers=10 !
       jpegenc idct-method=1 quality=100" pipeline
    """
    def __init__(self):
        super(Rtp2jpeg, self).__init__()

        # Create elements
        depay = elmake('rtph264depay', None)
        decoder = elmake('decodebin', None)
        self.vconvert = elmake('videoconvert', None)
        vscale = elmake('videoscale', None)
        vrate = elmake('videorate', None)
        filter1 = elmake("capsfilter", 'filter1')
        filter1.set_property('caps', Gst.Caps.from_string("video/x-raw,framerate=1/10"))
        queue1 = elmake('queue', None)
        queue1.set_property("leaky", 2)
        queue1.set_property("max-size-buffers", 10)
        jpegenc = elmake('jpegenc', None)
        jpegenc.set_property("idct-method", 1)
        jpegenc.set_property("quality", 100)

        els = (depay, decoder, self.vconvert, vscale, vrate, filter1, queue1, jpegenc)
        # Add elements to Bin
        for item in els:
            self.add(item)

        depay.link(decoder)
        els2 = (self.vconvert, vrate, filter1, jpegenc)

        # Link elements
        for pair in zip(els2, els2[1:]):
            pair[0].link(pair[1])

        decoder.connect("pad-added", self.decodebin_pad_added)

        # Add Ghost Pads
        self.add_pad(
            Gst.GhostPad.new('sink', depay.get_static_pad('sink'))
        )
        self.add_pad(
            Gst.GhostPad.new('src', jpegenc.get_static_pad('src'))
        )

    def decodebin_pad_added(self, element, pad):
        string = pad.query_caps(None).to_string()
        #print('Found stream: %s' % string)
        if string.startswith('video/x-raw'):
            pad.link(self.vconvert.get_static_pad('sink'))


class GstPipeline():
    """Base class that combine source, video decoder and output element into runable Gst pipeline
    """
    def __init__(self, src, video, filesink):
        """params
        --------------------
            src - source element, e.g. tcpsrc, udpsrc
            video - bin with decoder inside, see classes Rtp2jpg, Rtp2mp4
            sink - output element e.g. filesink
        """
        self.loop = None
        self.pipeline = Gst.Pipeline.new('pipeline')
        self.src = src
        self.video = video
        self.filesink = filesink
        self.constructPipeline()
        self.connectSignals()


    def connectSignals(self):
        """
        Connect various signals with the class methods.
        """
        # Connect the signals. ( catch the messages on the bus )
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.message_handler)


    def run(self):
        """Run the built pipeline. Actually convert will be started here.
        """

        self.loop = GObject.MainLoop()
        self.pipeline.set_state(Gst.State.PLAYING)
        try:
            self.loop.run()
        except KeyboardInterrupt:
            self.pipeline.send_event(Gst.Event.new_eos())
        finally:
            #wait to make sure all data chunks will be written on disk
            time.sleep(0.5)

        # cleanup
        self.pipeline.set_state(Gst.State.NULL)


    def message_handler(self, bus, message):
        """
        Capture the messages on the bus and
        set the appropriate flag.
        """
        #print(message.type)
        msgType = message.type
        if msgType == Gst.MessageType.ERROR:
            self.pipeline.set_state(Gst.State.NULL)
            self.error_message = message.parse_error()
            print(self.error_message)
        elif msgType == Gst.MessageType.EOS:
            self.loop.quit()

    def constructPipeline(self):
        """
        Create an instance of gst.Pipeline, create, add element objects
        to this pipeline. Create appropriate connections between the elements.
        """
        self.filter1 = elmake("capsfilter", 'filter1')
        self.filter1.set_property('caps', Gst.Caps.from_string(CAPS))
        self.src.connect("pad-added", self._src_pad_added)
        for item in ( self.src,
                           self.filter1,
                           self.video,
                           self.filesink):
            if item:
                self.pipeline.add(item)
            else:
                raise Exception("Element null")

        self.src.link(self.filter1)
        self.filter1.link(self.video)
        self.video.link(self.filesink)


    def _src_pad_added(self, element, pad):
        string = pad.query_caps(None).to_string()
        if string.startswith('application/x-rtp, media=(string)video'):
            pad.link(self.filter1.get_static_pad('sink'))



def transform(input_uri, out_type, out_file, num_buffers=-1):
    """Creates GStreamer pipeline using source URI and output type and location
        parameters
        ------------------
        input_uri - URI locator for source video stream
        out_type - type of output file/s. Options "mp4", "frames"
        out_file - output file name, e.g. /tmp/out.mp4 or /tmp/out_%d.jpg (for multiple jpg files)
        num_buffer - limit for input frames

    """
    src = element_make_from_uri(input_uri)
    if not src:
        raise Exception("Invalid source for URI {}".format(input_uri))


    try:
        src.set_property("num-buffers", num_buffers)
    except:
        pass

    transcoder = None
    sink = None

    if out_type == "mp4":
        transcoder = Rtp2mp4()
        sink = elmake("filesink", location=out_file)

    elif out_type == "frame":
        transcoder = Rtp2jpeg()
        sink = elmake("multifilesink", location=out_file)
    else:
        raise Exception("Invalid out type {}".format(out_type))

    client = GstPipeline(src,
                        transcoder,
                        sink
                        )


    client.run()
