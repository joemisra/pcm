from src.jv1080 import JV1080Patch
from src.patch import ModulationMatrix, Macro

class XV5080Patch(JV1080Patch):
    def __init__(self, name, data):
        super().__init__(name, data)
        self.modulation_matrix = ModulationMatrix()
        self.macros = {}
    def get_parameter(self, address, visited=None):
        if visited is None:
            visited = set()
        if address in visited:
            # Avoid infinite recursion
            return self.data.get(address, 0)
        visited.add(address)

        value = self.data.get(address, 0)
        for mod in self.modulation_matrix.modulations:
            if mod.destination == address:
                source_value = self.get_parameter(mod.source, visited)
                value += int(source_value * mod.amount)

        # Clamp the value to the valid MIDI range (0-127)
        return max(0, min(127, value))

    def set_parameter(self, address, value):
        if address in self.macros:
            macro = self.macros[address]
            scaled_value = int(
                ((value / 127) * (macro.max_value - macro.min_value)) + macro.min_value
            )
            for p in macro.parameters:
                self.set_parameter(p, scaled_value)
        else:
            self.data[address] = value

    def to_sysex(self):
        # Placeholder implementation
        header = [0xF0, 0x41, 0x10, 0x00, 0x00, 0x08, 0x12]
        data = []
        for address, value in self.data.items():
            data.extend(self._address_to_bytes(address))
            data.extend(self._value_to_bytes(value))
        checksum = self._calculate_checksum(data)
        footer = [checksum, 0xF7]
        return header + data + footer

    def _address_to_bytes(self, address):
        return [
            (address >> 21) & 0x7F,
            (address >> 14) & 0x7F,
            (address >> 7) & 0x7F,
            address & 0x7F,
        ]

    def _value_to_bytes(self, value):
        return [value]

    def to_dict(self):
        return {
            'name': self.name,
            'data': self.data,
            'modulation_matrix': {
                'modulations': [mod.__dict__ for mod in self.modulation_matrix.modulations]
            },
            'macros': {str(address): macro.__dict__ for address, macro in self.macros.items()}
        }

    def _calculate_checksum(self, data):
        checksum = 0
        for byte in data:
            checksum += byte
        return 128 - (checksum % 128)
