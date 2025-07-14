import unittest
from src.patch import Patch

class TestPatch(unittest.TestCase):
    def test_get_parameter_raises_not_implemented(self):
        patch = Patch("Test Patch", {})
        with self.assertRaises(NotImplementedError):
            patch.get_parameter(0x00)

    def test_set_parameter_raises_not_implemented(self):
        patch = Patch("Test Patch", {})
        with self.assertRaises(NotImplementedError):
            patch.set_parameter(0x00, 0x00)

    def test_to_sysex_raises_not_implemented(self):
        patch = Patch("Test Patch", {})
        with self.assertRaises(NotImplementedError):
            patch.to_sysex()

    def test_from_sysex_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            Patch.from_sysex([])

if __name__ == '__main__':
    unittest.main()
