"""Markdown TikZ package.

Utilities to compile TikZ figure in Markdown files.
"""

# https://facelessuser.github.io/pymdown-extensions/extensions/superfences/#custom-fences
# https://squidfunk.github.io/mkdocs-material/setup/extensions/python-markdown-extensions/#snippets

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from markdown import Markdown

from markdown_tikz.formatter import format_tikz

__all__: list[str] = ["formatter", "validator"]


def validator(
    language: str,
    inputs: dict[str, str],
    options: dict[str, Any],
    attrs: dict[str, Any],  # noqa: ARG001
    md: Markdown,  # noqa: ARG001
) -> bool:
    """Validate code blocks inputs.

    Parameters:
        language: The code language.
        inputs: The code block inputs, to be sorted into options and attrs.
        options: The container for options.
        attrs: The container for attrs:
        md: The Markdown instance.

    Returns:
        Success or not.
    """
    options["tikzlibrary"] = inputs.pop("library", "")
    options["tikzoption"] = inputs.pop("option", "")
    return True


def formatter(
    source: str,
    language: str,
    css_class: str,  # noqa: ARG001
    options: dict[str, Any],
    md: Markdown,
    classes: list[str] | None = None,  # noqa: ARG001
    id_value: str = "",  # noqa: ARG001
    attrs: dict[str, Any] | None = None,  # noqa: ARG001
    **kwargs: Any,  # noqa: ARG001
) -> str:
    """Execute code and return HTML.

    Parameters:
        source: The code to execute.
        language: The code language.
        css_class: The CSS class to add to the HTML element.
        options: The container for options.
        attrs: The container for attrs:
        md: The Markdown instance.
        classes: Additional CSS classes.
        id_value: An optional HTML id.
        attrs: Additional attributes
        **kwargs: Additional arguments passed to SuperFences default formatters.

    Returns:
        HTML contents.
    """
    if language == "tikz":
        return format_tikz(code=source, md=md, **options)
    else:
        return source
