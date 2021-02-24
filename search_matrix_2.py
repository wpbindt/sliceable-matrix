from sliceable_matrix import SliceableMatrix


def search(matrix: SliceableMatrix[int], target: int) -> bool:
    """
    Souped up version of binary search for matrix
    with ordered columns and rows.

    Despite the slicing happening in the return
    statement (which normally scales linearly with
    the size of the matrix), this algorithm runs 
    in O(n log(n)) time, where n is the max of 
    the number of rows and columns.
    It can be proved that replacing the iteration
    over the diagonal in the beginning with something
    that runs in logarithmic time improves the total
    worst case time to being linear in the number of
    rows or columns.
    """
    if not matrix:
        return False
    diag_sup = 0
    while diag_sup < matrix.diag_size:
        if matrix[diag_sup, diag_sup] > target:
            break
        diag_sup += 1

    if diag_sup == 0:
        return False
    if matrix[diag_sup - 1, diag_sup - 1] == target:
        return True
    
    return (
        search(matrix[:diag_sup, diag_sup:], target)
        or search(matrix[diag_sup:, :diag_sup], target)
    )

