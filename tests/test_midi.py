import unittest
from unittest.mock import patch, MagicMock
from src.midi import MidiController

class TestMidiController(unittest.TestCase):
    @patch('rtmidi.MidiOut')
    def test_send_sysex(self, MockMidiOut):
        # Create a mock instance of MidiOut
        mock_midi_out_instance = MockMidiOut.return_value
        mock_midi_out_instance.get_ports.return_value = ['MIDI Port 1', 'MIDI Port 2']
        mock_midi_out_instance.is_port_open.return_value = True

        # Create an instance of our MidiController
        controller = MidiController()
        controller.midi_out = mock_midi_out_instance

        # Open a port
        controller.open_port('MIDI Port 1')

        # Send a SysEx message
        sysex_data = [0xF0, 0x41, 0x10, 0x46, 0x12, 0x04, 0x00, 0x00, 0x00, 0x01, 0x7B, 0xF7]
        controller.send_sysex(sysex_data)

        # Assert that the send_message method was called with the correct data
        mock_midi_out_instance.send_message.assert_called_with(sysex_data)

if __name__ == '__main__':
    unittest.main()
