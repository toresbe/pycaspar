class Layer():
    def __init__(self, caspar_instance, channel_id, layer_id):
        self.layer_id = layer_id
        self.channel_id = channel_id
        self.caspar = caspar_instance

    @property
    def name(self):
        return '%d-%d' % (self.channel_id, self.layer_id)

    @property
    def id(self):
        return self.layer_id

    def clear(self):
        self.caspar._send_command('CLEAR %s' % (self.name,))

    def play(self, filename, transition = None, loop = False, seek = False):
        command = 'PLAY ' + self.name + ' '

        #FIXME: file name needs proper escaping
        command += '"' + filename + '" '

        if transition:
            command += transition + ' '

        if loop:
            command += 'LOOP '

        if seek:
            command += 'SEEK %d ' % (seek,)

        self.caspar._send_command(command)
