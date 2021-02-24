class SliceableMatrix:
    def __init__(self, rows, *, col_slice=None, row_slice=None):
        self.rows = rows
        if col_slice is None:
            col_slice = slice(0, len(rows[0]))
        if row_slice is None:
            row_slice = slice(0, len(rows))
        self._col_slice = col_slice
        self._row_slice = row_slice

    def __iter__(self):
        yield from [
            row[self._col_slice]
            for row in self.rows[self._row_slice]
        ]
    
    def __repr__(self):
        return str(list(self))

    def __getitem__(self, index):
        if not(isinstance(index, tuple) and len(index) == 2):
            raise ValueError('Invalid slice')
            
        row, col = index[0], index[1]
        if isinstance(row, int) and isinstance(col, int):
            if not self._row_slice.start + row < self._row_slice.stop:
                raise IndexError('Row index out of range')
            if not self._col_slice.start + col < self._col_slice.stop:
                raise IndexError('Column index out of range')
            return self.rows[
                self._row_slice.start + row
            ][
                self._col_slice.start + col
            ]
        
        if isinstance(row, int):
            row = slice(row, row + 1, None)
        if isinstance(col, int):
            col = slice(col, col + 1, None)
       
        return SliceableMatrix(
            self.rows,
            col_slice=slice(
                self._col_slice.start + col.start, 
                self._col_slice.start + col.stop
            ),
            row_slice=slice(
                self._row_slice.start + row.start, 
                self._row_slice.start + row.stop
            )
        )

