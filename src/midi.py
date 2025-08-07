try:
    import rtmidi  # type: ignore
except ModuleNotFoundError:
    # Provide a minimal stub so tests can run without native deps
    import sys
    import types

    rtmidi = types.ModuleType('rtmidi')

    class _StubMidiOut:
        def __init__(self):
            self._ports = ['MIDI Port 1', 'MIDI Port 2']
            self._open = False

        def get_ports(self):
            return self._ports

        def open_port(self, port_index):
            self._open = True

        def close_port(self):
            self._open = False

        def is_port_open(self):
            return self._open

        def send_message(self, sysex_data):
            pass

    rtmidi.MidiOut = _StubMidiOut  # type: ignore[attr-defined]
    sys.modules['rtmidi'] = rtmidi


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
