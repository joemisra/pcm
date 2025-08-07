from src.patch import Patch


class MU128Patch(Patch):
    def get_parameter(self, address):
        return self.data.get(address, 0)

    def set_parameter(self, address, value):
        self.data[address] = value

    def to_sysex(self):
        # Simplified Yamaha-style SysEx placeholder
        # Format: F0 43 10 4C <data...> <checksum> F7
        header = [0xF0, 0x43, 0x10, 0x4C]
        data_bytes = []
        for address, value in self.data.items():
            data_bytes.extend(self._address_to_bytes(address))
            data_bytes.append(value & 0x7F)
        checksum = self._calculate_checksum(data_bytes)
        footer = [checksum, 0xF7]
        return header + data_bytes + footer

    def _address_to_bytes(self, address):
        # 3 x 7-bit bytes (placeholder mapping)
        return [
            (address >> 14) & 0x7F,
            (address >> 7) & 0x7F,
            address & 0x7F,
        ]

    def _calculate_checksum(self, data):
        checksum_sum = sum(data) & 0x7F
        return (128 - checksum_sum) & 0x7F