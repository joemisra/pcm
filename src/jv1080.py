from src.patch import Patch

class JV1080Patch(Patch):
    def get_parameter(self, address):
        return self.data.get(address, 0)

    def set_parameter(self, address, value):
        self.data[address] = value

    def to_sysex(self):
        # Placeholder empty SysEx for JV-1080 (not implemented)
        return []

    @classmethod
    def from_sysex(cls, sysex_data):
        # In a real implementation, this would parse a SysEx message and create a patch
        pass
