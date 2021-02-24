import unittest

from sliceable_matrix import SliceableMatrix


class TestSliceableMatrix(unittest.TestCase):
    def test_no_slicing(self) -> None:
        rows = [[1, 2, 3, 4],
                [4, 5, 6, 9],
                [8, 10, 11, 13]]
        matrix = SliceableMatrix(rows)

        for row in range(3):
            for col in range(4):
                with self.subTest(row=row, col=col):
                    self.assertEqual(
                        matrix[row, col],
                        rows[row][col]
                    )
        
        for row in range(3):
            with self.subTest(row=row):
                with self.assertRaises(IndexError):
                    matrix[row, 4]
        for col in range(4):
            with self.subTest(col=col):
                with self.assertRaises(IndexError):
                    matrix[3, col]

    def test_slicing(self) -> None:
        rows = [[1, 2, 3, 4],
                [4, 5, 6, 9],
                [8, 10, 11, 13]]
        matrix = SliceableMatrix(rows)
        sliced_matrix = matrix[0:2, 1]
        for row in range(2):
            with self.subTest("Multiple rows, one column", row=row):
                self.assertEqual(
                    sliced_matrix[row, 0],
                    rows[row][1]
                )
        with self.assertRaises(IndexError):
            sliced_matrix[2, 0]
        for row in range(2):
            with self.subTest("Multiple rows, one column", row=row):
                with self.assertRaises(IndexError):
                    sliced_matrix[row, 1]

