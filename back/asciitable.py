from typing import Union, Optional, List, Iterator
import os
import re


def rflen(txt: str) -> int:
    return len(re.sub(r'\x1b\[[0-9;a-z]*?m', '', txt))


def p(
    headers: List[str],
    rows: Iterator,
    margin: int = 1,
    sizes: Union[str, List[Union[int, str]]] = '*',
    types: Optional[List[Union[str, type]]] = None,
    hb: bool = False
) -> Iterator:

    # Width should be auto-adjusting
    margin_space = " " * margin

    if type(sizes) is int:
        sizes = (sizes,) * len(headers)

    if sizes == '_':
        rows = list(map(list, rows))
        sizes = [
            max(len(headers[h]), max(map(rflen, map(str, (r[h] for r in rows)))))
            for h in range(len(headers))
        ]

    if sizes == '*':
        sizes = os.get_terminal_size(0).columns
        sizes = sizes // len(headers)
        sizes -= len(headers) * margin * 2 + 1 + 1
        sizes = (sizes,) * len(headers)

    sizes = list(sizes or (len(l) for l in headers))

    for idx, size in enumerate(sizes):
        if size == '*':
            size = os.get_terminal_size(0).columns
            size -= sum(sizes[:idx] + sizes[idx + 1:])
            size -= len(sizes) * (margin * 2 + 1) + 1
            # size //= 2
            sizes[idx] = size

    horizontal_border = '+' + '\u253c'.join(
        '\u2500' * (i + margin * 2)
        for i in sizes
    ) + '+'

    top_border = '\u250c' + horizontal_border[1:-1] + '\u2510'
    bottom_border = '\u2514' + horizontal_border[1:-1] + '\u2518'

    # top_border = '\u256d' + horizontal_border[1:-1] + '\u256e'
    # bottom_border = '\u2570' + horizontal_border[1:-1] + '\u256f'

    top_border2 = '\u2552' + horizontal_border[1:-1] + '\u2555'
    top_border2 = top_border2.replace('\u2500', '\u2550')
    top_border2 = top_border2.replace('\u253c', '\u2564')

    top_border = top_border.replace('\u253c', '\u252c')
    bottom_border = bottom_border.replace('\u253c', '\u2534')

    horizontal_border = '\u251c' + horizontal_border[1:-1] + '\u2524'

    def ff(tup): return '\u2502' + margin_space + f'{margin_space}\u2502{margin_space}'.join(
            '%-{}s'.format(size) % (item if rflen(item) <= size else item[:size - 1] + '…')
            for item, size in zip(map(str, tup), sizes)
        ) + margin_space + '\u2502'

    lines = map(ff, rows)

    lines = [
        # '%s' % top_border,
        ' ' * len(top_border),
        '%s' % ff(headers).replace('\u2502', ' '),
        '%s' % top_border2,
        *(hb and f'\n{horizontal_border}\n' or '\n').join(
            lines
        ).split('\n'),
        bottom_border
    ]

    # tt = os.get_terminal_size(0).columns

    # lines = [
    #     l.strip().center(tt)
    #     for l in lines
    # ]

    # lines = [l.replace(' ', '@') for l in lines]
    # lines = [
    #     l + ' ' + str(len(re.sub(r'\x1b\[[0-9;a-z]*?m', '', l)))
    #     for l in lines
    # ]

    return '\n'.join(lines)


if __name__ == "__main__":

    print(
        p(headers=['name', 'Might', 'Fate'], rows=[
            ["This is the name", 3, 2],
            ["other name", 4, 2]
        ], sizes='_')
    )
