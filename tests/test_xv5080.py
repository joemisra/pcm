import unittest
from src.xv5080 import XV5080Patch
from src.patch import Modulation, Macro

class TestXV5080Patch(unittest.TestCase):
    def test_modulation_matrix(self):
        patch = XV5080Patch("Test Patch", {})
        patch.set_parameter(0x100, 100)
        patch.set_parameter(0x200, 20)
        mod = Modulation(source=0x100, destination=0x200, amount=0.5)
        patch.modulation_matrix.add_modulation(mod)
        self.assertEqual(patch.get_parameter(0x200), 70)

    def test_macro(self):
        patch = XV5080Patch("Test Patch", {})
        macro = Macro("Test Macro", [0x100, 0x200])
        patch.macros[0x300] = macro
        patch.set_parameter(0x300, 50)
        self.assertEqual(patch.get_parameter(0x100), 50)
        self.assertEqual(patch.get_parameter(0x200), 50)

if __name__ == '__main__':
    unittest.main()
