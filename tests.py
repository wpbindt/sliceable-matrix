from typing import List
import unittest

from sliceable_matrix import SliceableMatrix


class TestSliceableMatrix(unittest.TestCase):
    def _check_contents(
        self,
        matrix: SliceableMatrix,
        expected: List[List[int]],
        msg: str
    ) -> None:
        row_boundary = len(expected)
        col_boundary = len(expected[0])
        for row in range(row_boundary):
            for col in range(col_boundary):
                with self.subTest(
                    f'Matrix content check for {msg}', 
                    row=row, 
                    col=col
                ):
                    self.assertEqual(
                        matrix[row, col],
                        expected[row][col]
                    )

        for row in range(row_boundary):
            with self.subTest(
                f'Matrix column boundary check for {msg}', 
                row=row
            ):
                with self.assertRaises(IndexError):
                    matrix[row, col_boundary]

        for col in range(col_boundary):
            with self.subTest(
                f'Matrix row boundary check for {msg}', 
                col=col
            ):
                with self.assertRaises(IndexError):
                    matrix[row_boundary, col]

    def test_slicing(self) -> None:
        rows = [[1, 2, 3, 4],
                [4, 5, 6, 9],
                [8, 10, 11, 13]]
        matrix = SliceableMatrix(rows)

        self._check_contents(
            matrix,
            expected=rows,
            msg='unsliced matrix'
        )

        self._check_contents(
            matrix[0:2, 1],
            expected=[[2], [5]],
            msg='sliced rows, selected column'
        )

        self._check_contents(
            matrix[1, 1:],
            expected=[[5, 6, 9]],
            msg='sliced columns, selected row'
        )

        self._check_contents(
            matrix[1:3, 1:4],
            expected=[
                [5, 6, 9],
                [10, 11, 13]
            ],
            msg='sliced rows and columns'
        )

        self._check_contents(
            matrix[:3, 1:3][1:3, :2],
            expected=[
                [5, 6],
                [10, 11]
            ],
            msg='doubly sliced matrix'
        )

        self._check_contents(
            matrix[:, :],
            expected=rows,
            msg='slices with None start and stop'
        )

