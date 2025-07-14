import rtmidi

class MidiController:
    def __init__(self):
        self.midi_out = rtmidi.MidiOut()
        self.available_ports = self.midi_out.get_ports()

    def open_port(self, port_name):
        if port_name in self.available_ports:
            port_index = self.available_ports.index(port_name)
            self.midi_out.open_port(port_index)
        else:
            raise ValueError(f"Port {port_name} not found.")

    def close_port(self):
        self.midi_out.close_port()

    def send_sysex(self, sysex_data):
        if self.midi_out.is_port_open():
            self.midi_out.send_message(sysex_data)
        else:
            raise RuntimeError("MIDI port not open.")
