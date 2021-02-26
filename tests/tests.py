from dataclasses import dataclass
from typing import List
import unittest

from sliceable_matrix.sliceable_matrix import SliceableMatrix


@dataclass
class Case:
    matrix: SliceableMatrix[int]
    expected: List[List[int]]
    msg: str


class TestSliceableMatrix(unittest.TestCase):
    def _check_contents(self, case: Case) -> None:
        matrix = case.matrix
        expected = case.expected
        msg = case.msg

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
                with self.assertRaises(IndexError) as e:
                    matrix[row, col_boundary]
                self.assertEqual(
                    str(e.exception),
                    'Column index out of range'
                )

        for col in range(col_boundary):
            with self.subTest(
                f'Matrix row boundary check for {msg}', 
                col=col
            ):
                with self.assertRaises(IndexError) as e:
                    matrix[row_boundary, col]
                self.assertEqual(
                    str(e.exception),
                    'Row index out of range'
                )


        with self.subTest(f'Diagonal size check for {msg}'):
            self.assertEqual(
                matrix.diag_size,
                min(row_boundary, col_boundary)
            )

        with self.subTest(f'Rows property check for {msg}'):
            self.assertEqual(
                matrix.rows,
                expected
            )

    def test_slicing(self) -> None:
        rows = [[1, 2, 3, 4],
                [4, 5, 6, 9],
                [8, 10, 11, 13]]
        matrix = SliceableMatrix(rows)

        single_row = SliceableMatrix([[101, 20, 3, 4]])

        single_col = SliceableMatrix([[101], [20], [3]])
        
        cases = [
            Case(
                matrix=matrix,
                expected=rows,
                msg='unsliced matrix'
            ),
            Case(
                matrix=matrix[0:2, 1],
                expected=[[2], [5]],
                msg='sliced rows, selected column'
            ),
            Case(
                matrix=matrix[1, 1:],
                expected=[[5, 6, 9]],
                msg='sliced columns, selected row'
            ),
            Case(
                matrix=matrix[1:3, 1:4],
                expected=[
                    [5, 6, 9],
                    [10, 11, 13]
                ],
                msg='sliced rows and columns'
            ),
            Case(
                matrix=matrix[0:3, 1:3][1:3, :2],
                expected=[
                    [5, 6],
                    [10, 11]
                ],
                msg='doubly sliced matrix'
            ),
            Case(
                matrix=matrix[:, :],
                expected=rows,
                msg='slices with None start and stop'
            ),
            Case(
                matrix=single_row[:, :2],
                expected=[[101,20]],
                msg='single row matrix'
            ),
            Case(
                matrix=single_col[:2, :],
                expected=[[101], [20]],
                msg='single column matrix'
            )
        ]

        for case in cases:
            self._check_contents(case)

    def test_exceptions(self) -> None:
        rows = [[1, 2, 3, 4],
                [4, 5, 6, 9],
                [8, 10, 11, 13]]
        matrix = SliceableMatrix(rows)
        with self.assertRaises(TypeError):
            matrix[1]

        with self.assertRaises(TypeError):
            matrix[1:2]

        with self.assertRaises(TypeError):
            matrix[1, 2, 3]

        with self.assertRaises(TypeError):
            matrix[1:2, 2, 3]

    def test_empty(self) -> None:
        rows = [[1, 2, 3, 4],
                [4, 5, 6, 9],
                [8, 10, 11, 13]]
        matrix = SliceableMatrix(rows)

        self.assertTrue(matrix)
        self.assertTrue(matrix[1:2, 2])

        self.assertFalse(matrix[1:1, 2])
        self.assertFalse(matrix[:0, 2])
        self.assertFalse(matrix[3:, 2])

        self.assertFalse(matrix[1:1, :])
        self.assertFalse(matrix[:0, :])
        self.assertFalse(matrix[3:, :])

        self.assertFalse(matrix[:, 1:1])
        self.assertFalse(matrix[:, :0])
        self.assertFalse(matrix[:, 4:])

        self.assertFalse(matrix[2, 1:1])
        self.assertFalse(matrix[2, :0])
        self.assertFalse(matrix[2, 4:])

        self.assertFalse(matrix[2, 4:5])
        self.assertFalse(matrix[3:4, 2])

