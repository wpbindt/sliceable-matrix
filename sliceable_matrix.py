class SliceableMatrix:
    # TODO: replace start and stop with col_slice, row_slice
    def __init__(self, lists, *, start=(0,0), stop=None):
        self.lists = lists
        if stop is None:
            stop = (len(lists), len(lists[0]))
        self.stop = stop
        self.start = start

    def __iter__(self):
        yield from [
            row[self.start[1]:self.stop[1]] 
            for row in self.lists[self.start[0]:self.stop[0]]
        ]
    
    def __repr__(self):
        return str(list(self))

    def __getitem__(self, index):
        if not(isinstance(index, tuple) and len(index) == 2):
            raise ValueError('Invalid slice')
            
        row, col = index[0], index[1]
        if isinstance(row, int) and isinstance(col, int):
            if not (
                self.start[0] + row <= self.stop[0] 
                and self.start[1] + col <= self.stop[1]
            ):
                raise IndexError('Index out of range')
            return self.lists[self.start[0] + index[0]][self.start[1] + col]
        
        if isinstance(row, int):
            row = slice(row, row + 1, None)
        if isinstance(col, int):
            col = slice(col, col + 1, None)
        
        return SliceableMatrix(
            self.lists,
            start=(self.start[0] + row.start, self.start[1] + col.start),
            stop=(self.start[0] + row.stop - 1, self.start[1] + col.stop - 1)
        )

