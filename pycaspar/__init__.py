import socket
import logging
import xml.etree.ElementTree as ET
import re
from .channel import Channel
from .layer import Layer


class CasparCG:
    def __init__(self, hostname, amcp_port = 5250):
        """

        Open a connection to a CasparCG instance.

        :param string hostname: Host name of Caspar server.
        :param int amcp_port: Port number for AMCP connection.
        """
        self.socket = None
        self.hostname = hostname
        self.amcp_port = amcp_port
        if self.socket is not None:
            self.disconnect()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.hostname, self.amcp_port))

    def _read_reply(self):
        response = self.socket.recv(3)

        try:
            return_code = int(response)
        except ValueError:
            raise ValueError('Did not receive numeric return code from CasparCG')

        while response[-2:] != b'\r\n':
            response += self.socket.recv(1)

        logging.debug('CasparCG replied %s' % (response.strip().decode('UTF-8'),))

        response = ''

        # From the AMCP spec:
        #
        # 200 [command] OK - The command has been executed and several lines of
        # data (seperated by \r\n) are being returned (terminated with an
        # additional \r\n)
        #
        # 201 [command] OK - The command has been executed and
        # data (terminated by \r\n) is being returned.
        #
        # 202 [command] OK - The command has been executed.

        if return_code == 200: # multiline returned_data
            returned_data_buffer = b''

            while returned_data_buffer[-4:] != b'\r\n\r\n':
                returned_data_buffer += self.socket.recv(512)

            returned_data = returned_data_buffer.splitlines()[:-1]

        elif return_code == 201: # single-line returned_data
            returned_data = b''
            while returned_data[-2:] != b'\r\n':
                returned_data += self.socket.recv(512)

        elif return_code == 202: # no data returned
            returned_data = None

        else:
            raise ValueError('CasparCG command failed: ' + response)

        if returned_data is None:
            return None
        return returned_data.decode()

    def _send_command(self, command, xmlreply=False):
        self.socket.send(('%s\r\n' % command).encode('UTF-8'))
        logging.debug("sending command %s" % (command,))
        return self._read_reply()

    def _get_info(self):
        self._channels = {}
        for line in self._send_command('INFO'):
            (channel_id, video_standard, status) = line.split(' ', 3)
            self._channels[int(channel_id)] = {'standard': video_standard, 'status': status}
            (resolution, refreshmode, framerate) = re.match(r'([0-9]+)(.)([0-9]+)', video_standard).groups()
            self._channels[int(channel_id)]['framerate'] = float(framerate) / 100

        for channel_id in list(self._channels.keys()):
            xml_string = self._send_command('INFO %d' % (channel_id,))
            # This hack needs doing because CasparCG emits malformed XML; tags must begin with alpha...
            xml_string = re.sub(r'(?P<start><|</)(?P<number>[0-9]+?)>', '\g<start>tag\g<number>>', xml_string, 0)
            root = ET.fromstring(xml_string)
            self._layers = {}
            for child in root.findall("stage/layer/"):
                layer_id = int(re.match(r'...(?P<number>[0-9]+)$', child.tag).group('number'))
                self._layers[layer_id] = child

    @property
    def channels(self):
        """

        Query the server and return a list of channels.
        """
        self._get_info()
        return self._channels

    def layer(self, channel_id, layer_id):
        """

        Create and return a Layer object corresponding to channel and layer ID numbers.

        :param int channel_id: Channel ID number.
        :param int layer_id: Layer ID number.
        """
        return Layer(self, channel_id, layer_id)

    def channel(self, channel_id):
        """

        Create and return a Channel object corresponding to channel ID number.

        :param int channel_id: Channel ID number.
        """
        return Channel(self, channel_id)

    @property
    def layers(self):
        """

        Query the server and return a list of layers.
        """
        self._get_info()
        return self._layers

if __name__ == '__main__':
    #c = CasparCG('localhost')
    #print(c._send_command('INFO 1-50'))
    #print((c.channel(1).framerate))
    pass
