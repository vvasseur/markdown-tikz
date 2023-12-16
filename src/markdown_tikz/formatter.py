"""TikZ formatter."""

from __future__ import annotations

import subprocess
import os
import tempfile

from typing import TYPE_CHECKING, Any
from uuid import uuid4

from markupsafe import Markup
from markdown_tikz.rendering import MarkdownConverter, add_source

if TYPE_CHECKING:
    from markdown.core import Markdown

default_tabs = ("Code", "Figure")


def tikz_to_svg(
    code: str,
    tikzlibrary: str,
    tikzoption: str,
    **options: Any,
) -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
        latex_path = os.path.join(temp_dir, "tikz.tex")
        pdf_path = os.path.join(temp_dir, "tikz.pdf")
        svg_path = os.path.join(temp_dir, "tikz.svg")

        latex_document = f"""
        \\documentclass[tikz, border=10pt]{{standalone}}
        \\usetikzlibrary{{{tikzlibrary}}}
        \\begin{{document}}
        \\begin{{tikzpicture}}[{tikzoption}]
        {code}
        \\end{{tikzpicture}}
        \\end{{document}}
        """

        with open(latex_path, "w") as file:
            file.write(latex_document)

        subprocess.run(
            [
                "lualatex",
                "--interaction=nonstopmode",
                "--output-directory",
                temp_dir,
                latex_path,
            ],
            check=True,
        )

        subprocess.run(["pdf2svg", pdf_path, svg_path], check=True)
        # You may also use Inkscape
        # subprocess.run(
        #     ["inkscape", pdf_path, "--export-filename=" + svg_path], check=True
        # )

        with open(svg_path, "r") as file:
            svg_content = file.read()

        return svg_content


def format_tikz(
    code: str,
    md: Markdown,
    tikzlibrary: str,
    tikzoption: str,
    **options: Any,
) -> Markup:
    """Execute code and return HTML.

    Parameters:
        code: The code to execute.
        md: The Markdown instance.

    Returns:
        HTML contents.
    """
    markdown = MarkdownConverter(md)

    output = tikz_to_svg(code, tikzlibrary, tikzoption, **options)

    placeholder = str(uuid4())

    full_code = f"""\
\\usetikzlibrary{{{tikzlibrary}}}
\\begin{{tikzpicture}}[{tikzoption}]
{code}
\\end{{tikzpicture}}
"""
    wrapped_output = add_source(
        source=full_code,
        output=placeholder,
        language="latex",
        tabs=default_tabs,
    )
    return markdown.convert(wrapped_output, stash={placeholder: output})
