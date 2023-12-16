"""Markdown extensions and helpers."""

from __future__ import annotations

from contextlib import contextmanager
from functools import lru_cache
from textwrap import indent
from typing import TYPE_CHECKING, Iterator

from markdown import Markdown
from markupsafe import Markup

from markdown_tikz.processors import (
    IdPrependingTreeprocessor,
    InsertHeadings,
    RemoveHeadings,
)

if TYPE_CHECKING:
    from xml.etree.ElementTree import Element


def code_block(language: str, code: str) -> str:
    """Format code as a code block.

    Parameters:
        language: The code block language.
        code: The source code to format.

    Returns:
        The formatted code block.
    """
    return f"```{language}\n{code}\n```"


def tabbed(*tabs: tuple[str, str]) -> str:
    """Format tabs using `pymdownx.tabbed` extension.

    Parameters:
        *tabs: Tuples of strings: title and text.

    Returns:
        The formatted tabs.
    """
    parts = []
    for title, text in tabs:
        title = title.replace(r"\|", "|").strip()  # noqa: PLW2901
        parts.append(f'=== "{title}"')
        parts.append(indent(text, prefix=" " * 4))
        parts.append("")
    return "\n".join(parts)


def add_source(
    *,
    source: str,
    output: str,
    language: str,
    tabs: tuple[str, str],
) -> str:
    """Add source code block to the output.

    Parameters:
        source: The source code block.
        output: The current output.
        language: The code language.
        tabs: Tabs titles (if used).

    Raises:
        ValueError: When the given location is not supported.

    Returns:
        The updated output.
    """
    source_tab_title, result_tab_title = tabs
    source_block = code_block(language, source)

    return tabbed((result_tab_title, output), (source_tab_title, source_block))


@lru_cache(maxsize=None)
def _register_headings_processors(md: Markdown) -> None:
    md.treeprocessors.register(
        InsertHeadings(md),
        InsertHeadings.name,
        priority=75,  # right before markdown.blockprocessors.HashHeaderProcessor
    )
    md.treeprocessors.register(
        RemoveHeadings(md),
        RemoveHeadings.name,
        priority=4,  # right after toc
    )


def _mimic(md: Markdown, headings: list[Element]) -> Markdown:
    new_md = Markdown()
    new_md.registerExtensions(md.registeredExtensions, {})
    new_md.treeprocessors.register(
        IdPrependingTreeprocessor(md, ""),
        IdPrependingTreeprocessor.name,
        priority=4,  # right after 'toc' (needed because that extension adds ids to headings)
    )
    new_md._original_md = md  # type: ignore[attr-defined]

    return new_md


@contextmanager
def _id_prefix(md: Markdown, prefix: str | None) -> Iterator[None]:
    MarkdownConverter.counter += 1
    id_prepending_processor = md.treeprocessors[IdPrependingTreeprocessor.name]
    id_prepending_processor.id_prefix = (
        prefix if prefix is not None else f"tizk-{MarkdownConverter.counter}--"
    )
    try:
        yield
    finally:
        id_prepending_processor.id_prefix = ""


class MarkdownConverter:
    """Helper class to avoid breaking the original Markdown instance state."""

    counter: int = 0

    def __init__(self, md: Markdown) -> None:  # noqa: D107
        self._md_ref: Markdown = md
        self._headings: list[Element] = []

    @property
    def _original_md(self) -> Markdown:
        return getattr(self._md_ref, "_original_md", self._md_ref)

    def convert(
        self,
        text: str,
        stash: dict[str, str] | None = None,
        id_prefix: str | None = None,
    ) -> Markup:
        """Convert Markdown text to safe HTML.

        Parameters:
            text: Markdown text.
            stash: An HTML stash.

        Returns:
            Safe HTML.
        """
        md = _mimic(self._original_md, self._headings)

        # convert markdown to html
        with _id_prefix(md, id_prefix):
            converted = md.convert(text)

        # restore html from stash
        for placeholder, stashed in (stash or {}).items():
            converted = converted.replace(placeholder, stashed)

        markup = Markup(converted)

        return markup
