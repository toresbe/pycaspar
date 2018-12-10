class Layer():
    def __init__(self, caspar_instance, channel_id, layer_id):
        """
        Create a Caspar Layer object.

        :param pycaspar.CasparCG caspar_instance: Caspar instance
        """
        self.layer_id = layer_id
        self.channel_id = channel_id
        self.caspar = caspar_instance

    @property
    def name(self):
        """
        Return the Caspar-internal name for the current layer.
        """
        return '%d-%d' % (self.channel_id, self.layer_id)

    @property
    def id(self):
        """
        Get layer integer id as used by Caspar internally.
        """
        return self.layer_id

    def clear(self):
        """
        Clears layer by sending a CLEAR command.
        """
        self.caspar._send_command('CLEAR %s' % (self.name,))

    def play(self, filename, transition = None, loop = False, seek = False):
        """
        Play a given resource on the layer.

        :param str filename: Filename or URI to play
        :param str transition: Transition string (see https://github.com/CasparCG/help/wiki/AMCP-Protocol#loadbg for definition)
        :param bool loop: Causes the file to play indefinitely.
        :param int seek: Seek *seek* seconds into file before playing
        """
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
