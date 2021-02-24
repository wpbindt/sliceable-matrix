from typing import List
import unittest

from sliceable_matrix import SliceableMatrix


class TestSliceableMatrix(unittest.TestCase):
    def _check_contents(
        self,
        matrix: SliceableMatrix,
        expected: List[List[int]]
    ) -> None:
        row_boundary = len(expected)
        col_boundary = len(expected[0])
        for row in range(row_boundary):
            for col in range(col_boundary):
                with self.subTest('Matrix content check', row=row, col=col):
                    self.assertEqual(
                        matrix[row, col],
                        expected[row][col]
                    )

        for row in range(row_boundary):
            with self.subTest('Matrix column boundary check', row=row):
                with self.assertRaises(IndexError):
                    matrix[row, col_boundary]

        for col in range(col_boundary):
            with self.subTest('Matrix row boundary check', col=col):
                with self.assertRaises(IndexError):
                    matrix[row_boundary, col]


    def test_no_slicing(self) -> None:
        rows = [[1, 2, 3, 4],
                [4, 5, 6, 9],
                [8, 10, 11, 13]]
        matrix = SliceableMatrix(rows)

        self._check_contents(
            matrix,
            rows
        )

    def test_slicing(self) -> None:
        rows = [[1, 2, 3, 4],
                [4, 5, 6, 9],
                [8, 10, 11, 13]]
        matrix = SliceableMatrix(rows)

        self._check_contents(
            matrix[0:2, 1],
            expected=[[2], [5]]
        )

        self._check_contents(
            matrix[1, 1:4],
            expected=[[5, 6, 9]]
        )

        self._check_contents(
            matrix[1:3, 1:4],
            expected=[
                [5, 6, 9],
                [10, 11, 13]
            ]
        )

    def test_double_slicing(self) -> None:
        rows = [[1, 2, 3, 4],
                [4, 5, 6, 9],
                [8, 10, 11, 13]]
        matrix = SliceableMatrix(rows)

        self._check_contents(
            matrix[0:3, 1:3][1:3, 0:2],
            expected=[
                [5, 6],
                [10, 11]
            ]
        )


    def test_none_slice(self) -> None:
        ...

