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
        result = self.analyzer.analyze(code)
        self.assertEqual(result['x'], 'Even')
        self.assertEqual(result['y'], 'Even')

    def test_odd_variable(self):
        code = """
        x = 5
        y = x + 2
        """
        result = self.analyzer.analyze(code)
        self.assertEqual(result['x'], 'Odd')
        self.assertEqual(result['y'], 'Odd')

if __name__ == "__main__":
    unittest.main()
