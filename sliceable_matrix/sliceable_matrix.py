from __future__ import annotations

from typing import Generic, Iterator, List, TypeVar, Union

T = TypeVar('T')


class SliceableMatrix(Generic[T]):
    #TODO read slices modulo length
    def __init__(
        self, 
        rows: List[List[T]],
        *, 
        col_slice: slice = slice(None),
        row_slice: slice = slice(None)
    ) -> None:
        self._rows = rows
        self._row_slice = self._remove_nones_from_slice(
            row_slice, 
            replacement_stop=len(rows)
        )
        self._col_slice = self._remove_nones_from_slice(
            col_slice, 
            replacement_stop=len(rows[0])
        )

    @property
    def rows(self) -> List[List[T]]:
        return [
            row[self._col_slice]
            for row in self._rows[self._row_slice]
        ]

    def __iter__(self) -> Iterator[T]:
        yield from [
            element
            for row in self.rows
            for element in row
        ]

    @property
    def diag_size(self) -> int:
        col_boundary = min(self._col_slice.stop, len(self._rows[0]))
        row_boundary = min(self._row_slice.stop, len(self._rows))
        return max(
            0,
            min(
                col_boundary - self._col_slice.start,
                row_boundary - self._row_slice.start
            )
        )

    def __bool__(self) -> bool:
        return self.diag_size > 0

    def __str__(self) -> str:
        return str(self.rows)

    def __getitem__(self, index) -> Union[T, SliceableMatrix[T]]:
        if isinstance(index, int) or len(index) != 2:
            raise TypeError('Invalid slice or index')

        row, col = index[0], index[1]
        if isinstance(row, int) and isinstance(col, int):
            return self._get_single_item(row, col)

        if isinstance(row, int):
            row = slice(row, row + 1, None)
        if isinstance(col, int):
            col = slice(col, col + 1, None)

        return self._get_slice(row, col)

    def _get_single_item(self, row: int, col: int) -> T:
        if self._row_slice.start + row >= self._row_slice.stop:
            raise IndexError('Row index out of range')
        if self._col_slice.start + col >= self._col_slice.stop:
            raise IndexError('Column index out of range')

        return self._rows[
            self._row_slice.start + row
        ][
            self._col_slice.start + col
        ]

    def _get_slice(self, row: slice, col: slice) -> SliceableMatrix[T]:
        row = self._remove_nones_from_slice(row, self._row_slice.stop)
        col = self._remove_nones_from_slice(col, self._col_slice.stop)

        return SliceableMatrix(
            self._rows,
            col_slice=slice(
                self._col_slice.start + col.start, 
                self._col_slice.start + col.stop
            ),
            row_slice=slice(
                self._row_slice.start + row.start, 
                self._row_slice.start + row.stop
            )
        )

    @staticmethod
    def _remove_nones_from_slice(
        slice_: slice, 
        replacement_stop: int
    ) -> slice:
        if slice_.start is None:
            start = 0
        else:
            start = slice_.start
        if slice_.stop is None:
            stop = replacement_stop
        else:
            stop = slice_.stop

        return slice(start, stop)

