import unittest
from sheets_manager import SheetsManager

sheet_test = SheetsManager("1Hae-zhZKMY5PVWIipNWW7YgjS3ayWBi1jT93i46I5AE")

class DataRetrieverTest(unittest.TestCase):

    def test_write(self):
        testcase = sheet_test.write("D1", [[1], [2], [3]])
        expected = ["1Hae-zhZKMY5PVWIipNWW7YgjS3ayWBi1jT93i46I5AE", "Sheet1!D1:D3", 3, 1, 3]
        for index, case in enumerate(testcase.values()):
            self.assertEqual(expected[index], case)

if __name__ == "__main__":
    unittest.main()