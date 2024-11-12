import unittest
from analyzer import ParityAnalyzer

class TestParityAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = ParityAnalyzer()

    def test_even_variable(self):
        code = """
        x = 4
        y = x + 2
        """
        self.analyzer.build_cfg(code)
        result = self.analyzer.analyze()
        self.assertEqual(result['x'], 'Even')
        self.assertEqual(result['y'], 'Even')

    def test_odd_variable(self):
        code = """
        x = 5
        y = x + 2
        """
        self.analyzer.build_cfg(code)
        result = self.analyzer.analyze()
        self.assertEqual(result['x'], 'Odd')
        self.assertEqual(result['y'], 'Odd')

    def test_mixed_operations(self):
        code = """
        a = 3
        b = 6
        c = a + b
        d = a * b
        """
        self.analyzer.build_cfg(code)
        result = self.analyzer.analyze()
        self.assertEqual(result['a'], 'Odd')
        self.assertEqual(result['b'], 'Even')
        self.assertEqual(result['c'], 'Odd')  # Odd + Even = Odd
        self.assertEqual(result['d'], 'Even')  # Odd * Even = Even

if __name__ == "__main__":
    unittest.main()
