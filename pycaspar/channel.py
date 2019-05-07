from .layer import Layer

class Channel():
    def __init__(self, caspar_instance, channel_id):
        self.channel_id = channel_id
        self.caspar = caspar_instance

    @property
    def framerate(self):
        """
        Query server and return the frame rate of the channel.
        """
        self.caspar._get_info()
        return self.caspar._channels[self.channel_id]['framerate']

    @property
    def name(self):
        return '%d' % (self.channel_id,)

    @property
    def id(self):
        """
        Get channel integer id as used by Caspar internally.
        """
        return self.channel_id

    def layer(self, layer_id):
        """
        Get a Caspar Layer object for the given numeric layer ID
        :param int layer_id: Layer ID
        """
        return Layer(self.caspar, self.channel_id, layer_id)

    def clear(self):
        """
        Clear channel and all layers on channel.
        """
        self.caspar._send_command('CLEAR %s' % (self.name,))
