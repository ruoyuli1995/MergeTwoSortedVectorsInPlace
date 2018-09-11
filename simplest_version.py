#coding=utf-8

def rotate(inp, start, end, rotate_steps):
    """Rotate a list by rotate_steps steps within O(N) time and O(1) space
    """
    def reverse(l, start, end):
        while start < end:
            l[start], l[end] = l[end], l[start]
            start += 1
            end -= 1
    rotate_steps %= (end - start)
    rotate_steps += start
    end -= 1
    reverse(inp, start, end)
    reverse(inp, start, rotate_steps - 1)
    reverse(inp, rotate_steps, end)

def merge_series(inp, buffer_first, head_first, tail_first, head_second):
    """Merge two series
    It is a little trick with variable buffer_first
    """
    idx_first, idx_second = head_first, head_second
    while idx_first <= tail_first:
        if inp[idx_first] <= inp[idx_second]:
            inp[idx_first], inp[buffer_first] = inp[buffer_first], inp[idx_first]
            buffer_first += 1
            idx_first += 1
        else:
            inp[idx_second], inp[buffer_first] = inp[buffer_first], inp[idx_second]
            buffer_first += 1
            idx_second += 1
    return idx_second

def merge(to_merge):
    """Simplest version from Section 2
    """
    length = len(to_merge)
    sqrt_length = int(length ** 0.5)
    for idx in xrange(length - 1):
        if to_merge[idx] > to_merge[idx + 1]:
            max_index_a = idx
            break
    max_index_b = length - 1
    record = 0
    index_a, index_b = max_index_a, max_index_b
    # to find max sqrt_length elements
    while index_a >= 0 and index_b > max_index_a:
        record += 1
        if record == sqrt_length - 1:
            break
        if to_merge[index_a] > to_merge[index_b]:
            index_a -= 1
        else:
            index_b -= 1
    # rotate in-place twice to get first block
    rotate(to_merge, 0, max_index_a + 1, max_index_a + 1 - index_a)
    rotate(to_merge, 0, max_index_b + 1, max_index_b + 1 - index_b)
    # sort right blocks
    for i in xrange(1, sqrt_length):
        min_, idx = to_merge[i * sqrt_length + sqrt_length - 1], i
        for j in xrange(i, sqrt_length):
            if min_ > to_merge[j * sqrt_length + sqrt_length - 1]:
                min_, idx = to_merge[j * sqrt_length + sqrt_length - 1], j
        for j in xrange(0, sqrt_length):
            to_merge[i * sqrt_length + j], to_merge[idx * sqrt_length + j] = to_merge[idx * sqrt_length + j], to_merge[i * sqrt_length + j]
    # merge first two series
    head_first = sqrt_length
    for i in xrange(1, sqrt_length):
        if to_merge[i * sqrt_length + sqrt_length - 1] > to_merge[i * sqrt_length + sqrt_length]:
            tail_first = i * sqrt_length + sqrt_length - 1
            break
    head_second = tail_first + 1
    head_first = merge_series(to_merge, 0, head_first, tail_first, head_second)
    # merge next two series
    for i in xrange(head_first / sqrt_length, sqrt_length):
        if to_merge[i * sqrt_length + sqrt_length - 1] > to_merge[i * sqrt_length + sqrt_length]:
            tail_first = i * sqrt_length + sqrt_length - 1
            break
    head_second = tail_first + 1
    head_first = merge_series(to_merge, head_first - sqrt_length, head_first, tail_first, head_second)
    # rotate original first(max) block to tail
    rotate(to_merge, head_first - sqrt_length, length, sqrt_length)
    # sort tail block
    for i in xrange(1, sqrt_length):
        max_, idx = to_merge[-i], i
        for j in xrange(i, sqrt_length):
            if max_ < to_merge[-j]:
                max_, idx = to_merge[-j], j
        to_merge[-i], to_merge[-idx] = to_merge[-idx], to_merge[-i]
    to_merge[-sqrt_length : ] = sorted(to_merge[-sqrt_length : ])
    return to_merge

answer = [1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 4, 4, 5, 5, 5, 6, 7, 7, 8, 9, 7, 8, 8, 9, 10]
input_first, input_second = [2, 2, 2, 4, 4, 5, 5, 6, 7, 8, 8, 10], [1, 1, 1, 2, 2, 3, 3, 5, 7, 7, 8, 9, 9]
print(merge(input_first + input_second) == answer)
