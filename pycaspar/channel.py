class CasparChannel():
    def __init__(self, caspar_instance, channel_id):
        self.channel_id = channel_id
        self.caspar = caspar_instance

    @property
    def framerate(self):
        self.caspar._get_info()
        return self.caspar._channels[self.channel_id]['framerate']

    @property
    def name(self):
        return '%d' % (self.channel_id,)

    @property
    def id(self):
        return self.channel_id

    def layer(self, layer_id):
        return CasparLayer(self.caspar, self.channel_id, layer_id)

    def clear(self):
        self.caspar._send_command('CLEAR %s' % (self.name,))
