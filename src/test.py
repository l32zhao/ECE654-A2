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
        analysis_result = self.analyzer.analyze()
        
        # Print the detailed analysis result
        print("\nAnalysis Result for test_even_variable:")
        for line_info in analysis_result:
            print(line_info)

        # Get the final state of variable states from the analysis report
        final_state = analysis_result[-1][2]
        self.assertEqual(final_state['x'], 'Even')
        self.assertEqual(final_state['y'], 'Even')

    def test_odd_variable(self):
        code = """
        x = 5
        y = x + 2
        """
        self.analyzer.build_cfg(code)
        analysis_result = self.analyzer.analyze()
        
        # Print the detailed analysis result
        print("\nAnalysis Result for test_odd_variable:")
        for line_info in analysis_result:
            print(line_info)

        # Get the final state of variable states from the analysis report
        final_state = analysis_result[-1][2]
        self.assertEqual(final_state['x'], 'Odd')
        self.assertEqual(final_state['y'], 'Odd')

    def test_mixed_operations(self):
        code = """
        a = 3
        b = 6
        c = a + b
        d = a * b
        """
        self.analyzer.build_cfg(code)
        analysis_result = self.analyzer.analyze()
        
        # Print the detailed analysis result
        print("\nAnalysis Result for test_mixed_operations:")
        for line_info in analysis_result:
            print(line_info)

        # Get the final state of variable states from the analysis report
        final_state = analysis_result[-1][2]
        self.assertEqual(final_state['a'], 'Odd')
        self.assertEqual(final_state['b'], 'Even')
        self.assertEqual(final_state['c'], 'Odd')  # Odd + Even = Odd
        self.assertEqual(final_state['d'], 'Even')  # Odd * Even = Even

if __name__ == "__main__":
    unittest.main()
