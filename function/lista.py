from random import shuffle
from statistics import mean
from typing import List, MutableSequence, Sequence


def mean_level(level_list: MutableSequence[int], n: int) -> List[int]:
    if n <= 0:
        raise ValueError(f'n precisa ser maior que zero. n={n}')

    len_list = len(level_list)
    step = min(len_list, n)
    shuffle(level_list)

    return [
        int(mean(chunk))
        for chunk in chunks(level_list, step)
    ]


def chunks(_list: Sequence, total_chunks: int):
    pivot = 0
    for i in range(0, total_chunks):
        len_slice = len(_list[i::total_chunks])
        pos_pivot = pivot+len_slice
        yield _list[pivot:pos_pivot]
        pivot += len_slice


if __name__ == '__main__':
    number_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    print(list(chunks(number_list, 6)))
    print(mean_level(number_list, 6))
