from typing import Union, Iterator, Any, Optional, List, Dict
from types import GeneratorType
from functools import partial, wraps
import re

html = str


def ellipsis(h: str, t: int = 300) -> str:

    if len(h) > t:
        return h[:t-6] + ' [...]'
    
    return h


def pretty_html(doc: html) -> html:
    
    def f():
        indent = 4
        depth = 0
        for c in doc.split('\n'):
            
            c = c.strip()

            if '<!' in c:
                yield c
                continue

            # Remove all args and odd forms

            # Sum and counter sum of opening /closing brackets
            a = len(re.findall(r'<[^/]', c))
            b = (c.count(r'</'))

            ttt = a + b
            total = a - b

            # if ttt == 0:
            #     depth -= 1

            if total < 0:
                depth += total
                c = ' ' * depth * indent + c
            else:
                c = ' ' * depth * indent + c
                depth += total
            
            yield c

    return '\n'.join(f())


def unroll(visa):
    for item in visa:
        if type(item) in (GeneratorType, list, tuple):# or ('__dict__' in item and '__iter__' in item.__dict__):
            yield from item
        else:
            yield item


def vise(
    *content: Union[str, Iterator], 
    tag: str, 
    attrs: dict = {},
    **kw
) -> str:

    attrs = attrs or {}
    attrs.update(kw)
    
    attrs = ' ' * (not not attrs) + ' '.join(
        '{}={!r}'.format(*a) for a in attrs.items()
    )
    
    backtrack = '/>'
    if content:
        if type(content) in (GeneratorType, list, tuple):
            content = unroll(content)
            content = '\n' + '\n'.join(map(str, content)) + '\n'
        backtrack = f'>{content}</{tag}>'
    
    return f'<{tag}{attrs}{backtrack}'


class X:

    def __getattr__(self, name):
        return partial(vise, tag=name)

    def __add__(self, content):
        return f"""<!DOCTYPE html>\n<html>\n{content}\n</html>"""

    def css(self, **kw):
        kw = {
            k.replace('_', '-'): v
            for k, v in kw.items()
        }
        return ' '.join(map(
            '%s: %s;'.__mod__,
            kw.items()
        ))

m = X()


def hprettify(f):
    @wraps(f)
    def wrapper(*a, **kw):
        result = f(*a, **kw)
        result = pretty_html(result)
        return result
    return wrapper


def as_html(
    dataset: List[Dict[str, Any]],
    max_results: int = 300
) -> html:

    if not dataset:
        return m.strong('Empty')

    
    return m.div(
        m.table(
            m.tr(
                m.th( key )
                for key in dataset[0]
            ),
            *(
                m.tr(
                    m.td(ellipsis(str(value))) 
                    for value in item.values()
                )
                for item in dataset[:max_results]
            )
        ),
        m.style(open('style.css').read()),
        attrs={'class': 'zig'}
    )

x = as_html(
    [
        {'a': 3, 'b': 2},
        {'a': 4, 'b': 5}
    ]
)

x = pretty_html(x)

# print(x)
# print(x.decode('utf-8'))
