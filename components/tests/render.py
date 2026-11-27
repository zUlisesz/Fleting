"""Utilidad de pruebas: expande un árbol de componentes sin abrir una ventana."""

import dataclasses
from collections.abc import Iterator

from flet.components.component import Component, Renderer
from flet.controls.base_control import BaseControl


def _children(control: BaseControl) -> Iterator[BaseControl]:
    for field in dataclasses.fields(control):
        value = getattr(control, field.name, None)
        if isinstance(value, dict):
            value = list(value.values())
        for item in value if isinstance(value, (list, tuple)) else [value]:
            if isinstance(item, BaseControl):
                yield item


def walk(node: BaseControl) -> Iterator[BaseControl]:
    """Recorre el árbol; los ``Component`` se evalúan (ejecutan sus hooks)."""
    if isinstance(node, Component):
        node.before_update()
        built = node._b if isinstance(node._b, list) else [node._b]
        for item in built:
            if item is not None:
                yield from walk(item)
        return
    yield node
    for child in _children(node):
        yield from walk(child)


def render(component, *args, **kwargs) -> list[BaseControl]:
    """Renderiza ``component(*args, **kwargs)`` y devuelve todos los controles."""
    with Renderer().with_context():
        return list(walk(component(*args, **kwargs)))
