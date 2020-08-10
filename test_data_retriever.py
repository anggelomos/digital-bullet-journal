import unittest
from data_retriever import DataRetriever

data_test = DataRetriever("B63SG1dvEUH_h5YZAus3mZLlTzKUyvlt5_KBmyhZ")

class DataRetrieverTest(unittest.TestCase):

    def test_productivity_time(self):
        testcase = data_test.productivity_time()
        self.assertIsInstance(testcase, dict)
        for category, time in testcase.items():
            self.assertIn(category, ["very productive", "productive", "neutral", "distracting", "very distracting", "total"])
            self.assertGreaterEqual(time, 0)

if __name__ == "__main__":
    unittest.main()