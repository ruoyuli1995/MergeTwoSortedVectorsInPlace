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


def forward_scheme(inp, head_first, head_second):
    """block merge forward scheme
    make sure head_second < int(len(inp) ** 0.5)
    """
    length = len(inp)
    idx_first, idx_second = head_first, head_second
    while idx_first < idx_second:
        # directly rotate
        if inp[idx_first] > inp[-1]:
            rotate(inp, idx_first, length, length - idx_second)
            break
        # not greater than idx_second
        if inp[idx_first] <= inp[idx_second]:
            idx_first += 1
            continue
        for i in xrange(idx_second, length - 1):
            if inp[idx_first] <= inp[i + 1]:
                rotate(inp, idx_first, i + 1, i + 1 - idx_second)
                idx_first += (i + 1 - idx_second + 1)
                idx_second = i + 1
                break


def main_algorithm(inp, start, end, sqrt_length):
    assert((end - start) % sqrt_length == 0)
    length = end - start
    # sort right blocks
    # there is an error in the paper when sorting right blocks
    # since it only considers tails of blocks
    # however, we can construct blocks like 5|5|5, 4|5|5, 4|4|4
    # which will results in error since after the first two done, 4|5|5 is left behind
    # so we need to consider the head of every block too(every block is sorted internally)
    # this error is brought by sort strategy and how to deal with I and J in section 3
    for i in xrange(1, length / sqrt_length):
        min_head, min_tail, idx = inp[start + i * sqrt_length], inp[start + i * sqrt_length + sqrt_length - 1], i
        for j in xrange(i, length / sqrt_length):
            if min_tail > inp[start + j * sqrt_length + sqrt_length - 1]:
                min_head, min_tail, idx = inp[start + j * sqrt_length], inp[start + j * sqrt_length + sqrt_length - 1], j
            elif min_head > inp[start + j * sqrt_length] and min_tail == inp[start + j * sqrt_length + sqrt_length - 1]:
                min_head, min_tail, idx = inp[start + j * sqrt_length], inp[start + j * sqrt_length + sqrt_length - 1], j
        for j in xrange(0, sqrt_length):
            inp[start + i * sqrt_length + j], inp[start + idx * sqrt_length + j] = inp[start + idx * sqrt_length + j], inp[start + i * sqrt_length + j]
    # locate and merge two series in a loop
    head_first = sqrt_length + start
    while head_first / sqrt_length < length / sqrt_length:
        tail_first = None
        for i in xrange((head_first - start) / sqrt_length, length / sqrt_length - 1):
            if inp[start + i * sqrt_length + sqrt_length - 1] > inp[start + i * sqrt_length + sqrt_length]:
                tail_first = i * sqrt_length + sqrt_length - 1 + start
                break
        if not tail_first:
            break
        head_second = tail_first + 1
        head_first = merge_series(inp, head_first - sqrt_length, head_first, tail_first, head_second)
    # rotate buffer block to tail
    rotate(inp, head_first - sqrt_length, start + length, end - head_first)
    # sort tail block
    for i in xrange(1, sqrt_length + 1):
        max_, idx = inp[end - i], i
        for j in xrange(i, sqrt_length + 1):
            if max_ < inp[end - j]:
                max_, idx = inp[end - j], j
        inp[end - i], inp[end - idx] = inp[end - idx], inp[end - i]


def merge(to_merge):
    length = len(to_merge)
    # ⌊sqrt(length)⌋
    sqrt_length = int(length ** 0.5)
    max_index_a = None
    for idx in xrange(length - 1):
        if to_merge[idx] > to_merge[idx + 1]:
            max_index_a = idx
            break
    if not max_index_a:
        return
    # block merge forward scheme
    if max_index_a + 1 < sqrt_length:
        forward_scheme(to_merge, 0, max_index_a + 1)
    # block merge backwards scheme
    # but here use "rotate + block merge forward scheme" instead
    elif length - (max_index_a + 1) < sqrt_length:
        rotate(to_merge, 0, length, length - (max_index_a + 1))
        forward_scheme(to_merge, 0, length - (max_index_a + 1))
    # normal procedure
    else:
        max_index_b = length - 1
        record = 0
        index_a, index_b = max_index_a, max_index_b
        # to find max sqrt_length elements
        while index_a >= 0 and index_b > max_index_a and record < sqrt_length:
            record += 1
            if to_merge[index_a] > to_merge[index_b]:
                index_a -= 1
            else:
                index_b -= 1
        s1 = max_index_a - index_a
        s2 = max_index_b - index_b
        index_a += 1
        index_b += 1
        assert(s1 + s2 == sqrt_length)
        # A: [index_a : max_index_a]
        # B: [index_b : max_index_b]
        c = index_a - s2
        # C: [c : index_a - 1]
        d = (max_index_b - max_index_a - s2) % sqrt_length
        d = index_b - d
        # D: [d : index_b - 1]
        # swap B and C
        for i in xrange(s2):
            to_merge[c + i], to_merge[index_b + i] = to_merge[index_b + i], to_merge[c + i]
        # buffer: [c : max_index_a]
        # E: [d : length - 1], which will be dealed at last
        # in the paper E is merged from C and D, but we can simply sort E instead
        for i in xrange(1, length + 1 - d):
            max_, idx = to_merge[-i], i
            for j in xrange(i, length + 1 - d):
                if max_ < to_merge[-j]:
                    max_, idx = to_merge[-j], j
            to_merge[-i], to_merge[-idx] = to_merge[-idx], to_merge[-i]
        t1 = (max_index_a + 1) % sqrt_length
        # F: [0 : t1 - 1]
        g = max_index_a + sqrt_length + 1
        # G: [max_index_a + 1 : g - 1]
        # get H and I
        # or we can merge two series here, which is described in the paper
        rotate(to_merge, 0, max_index_a + 1, max_index_a + 1 - t1)
        for i in xrange(max_index_a + 1 - t1, max_index_a + 1 + sqrt_length):
            min_, idx = to_merge[i], i
            for j in xrange(i, max_index_a + 1 + sqrt_length):
                if min_ > to_merge[j]:
                    min_, idx = to_merge[j], j
            to_merge[i], to_merge[idx] = to_merge[idx], to_merge[i]
        rotate(to_merge, 0, max_index_a + 1, t1)
        # H: [0 : t1 - 1]
        for i in xrange(sqrt_length):
            to_merge[t1 + i], to_merge[c + i] = to_merge[c + i], to_merge[t1 + i]
        # start main algorithm
        main_algorithm(to_merge, t1, d, sqrt_length)
        # deal with E
        # how to deal with E is not described in paper, but because 0 < len(E) < 2 * sqrt_length
        # we can use forward scheme here, which still can confirm the time complexity is no more than O(N)
        # but maybe better solution can be found
        rotate(to_merge, 0, length, length - d)
        forward_scheme(to_merge, 0, length - d)


def test():
    """Test with random functions
    """
    from random import randint
    from time import time
    for _ in xrange(1024):
        input_first = []
        for _ in xrange(randint(4, 1024)):
            input_first.append(randint(4, 1024))
        input_second = []
        for _ in xrange(randint(4, 1024)):
            input_second.append(randint(4, 1024))
        input_first.sort()
        input_second.sort()
        temp = input_first + input_second
        start = time()
        temp.sort()
        print(time() - start)
        to_merge = input_first + input_second
        start = time()
        merge(to_merge)
        print(time() - start)
        assert(temp == to_merge)


# use case
temp = [1, 2, 3, 4, 5] + [1, 2, 3, 4, 5]
merge(temp)
print(temp)

# test with random functions
test()
