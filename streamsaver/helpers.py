import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
Gst.init(None)


def element_make_from_uri(uri, type_=Gst.URIType.SRC):
    """Creates Gst element from URI locator
    """
    if not Gst.uri_is_valid(uri):
        raise Exception("Invalid URI {}".format(uri))

    proto = Gst.uri_get_protocol(uri)
    
    if proto == "tcp":
        u = Gst.uri_from_string(uri)
        return elmake("tcpserversrc", host=u.get_host(), port=u.get_port())

    if not Gst.uri_protocol_is_supported(type_, proto):
        raise Exception("Protocol {} not supported, URI {}".format(proto, uri))

    return Gst.Element.make_from_uri(type_, uri, None)


def elmake(type_, name_=None, *args, **kwargs):
    """Allows using concise syntax to make element and set properties.
    -----------------------
       params:
            type_ - Gst element type, see GStreamer docs for details
            name_ (optional) - name of element to refer in pipeline
            kwargs - other args will be treated as properties
       examples:
            elmake("fakesrc")
            elmake("filter", "filter1")
            elmake("udpsrc", port=6002)
            elmake("videotestsrc", asdict={"num-buffers": 10}

    """
    el = Gst.ElementFactory.make(type_, name_)
    if not el:
        raise Exception("{} not found".format(type_))
    for key, val in kwargs.items():
        if key == "asdict":
            for k, v in val.items():
                el.set_property(k, v)
            continue
        el.set_property(key, val)
    return el