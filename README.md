# Markdown TikZ

Utilities to compile TikZ figure in Markdown files.
It is experimental and may be unstable, with potential for crashes or rendering issues.

## Installation

With `pip`:

```bash
git clone https://github.com/vvasseur/markdown-tikz.git
cd markdown-tikz
pip install .
```

## Dependencies

This extension relies on the following:
- [SuperFences](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/): an extension of the [PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/);
- `lualatex`: for processing LaTeX;
- `pdf2svg`: for converting PDFs to SVG format.

Please ensure that you have a complete LaTeX distribution installed, which includes `lualatex` and TikZ.
Both `lualatex` and `pdf2svg` should be accessible in your system's PATH.

## Configuration

To allow compilation of TikZ figures to SVG, configure a custom fence from Python:

```python
from markdown import Markdown
from markdown_tikz import formatter, validator

Markdown(
    extensions=["pymdownx.superfences"],
    extension_configs={
        "pymdownx.superfences": {
            "custom_fences": [
                {
                    "name": "tikz",
                    "class": "tikz",
                    "format": formatter,
                }
            ]
        }
    }
)
```

...or in MkDocs configuration file, as a Markdown extension:

```yaml
# mkdocs.yml
markdown_extensions:
- pymdownx.superfences:
    custom_fences:
    - name: tikz
      class: tikz
      format: !!python/name:markdown_tikz.formatter
```

## Usage

You are now able to execute code blocks instead of displaying them:

````md
```tikz
\begin{scope}
\clip (0,0) circle (1cm);
\fill[black] (0cm,1cm) rectangle (-1cm, -1cm);
\end{scope}

\fill[black] (0,0.5) circle (0.5cm);
\fill[white] (0,-0.5) circle (0.5cm);

\fill[white] (0,0.5) circle (0.1cm);
\fill[black] (0,-0.5) circle (0.1cm);

\draw (0,0) circle (1cm);
```
````

To include TikZ libraries or set options for the tikzpicture environment, specify them in the header:

````md
```tikz library='angles,quotes' option='scale=3'
\coordinate (A) at (1,0);
\coordinate (B) at (0,0);
\coordinate (C) at (30:1cm);

\draw (A) -- (B) -- (C) pic [draw=green!50!black, fill=green!20, angle radius=9mm, "$\alpha$"] {angle = A--B--C};
```
````

## Credits

This project is a stripped-down, modified version of Timothée Mazzucotelli's [Markdown Exec](https://github.com/pawamoy/markdown-exec).
