# Contributing Guide

First off, good for you for contributing :smiley:!

## Development Installation

Since this is a poetry-based project, many people would be confused on how to install the latest and greatest version of the project.

### Step 1: Poetry it

Poetry is a project and dependency manager. Since this project has zero dependencies, poetry is just for the ease of development (python package building, publishing, etc). And to make sure to avoid situations like "well, it worked on my computer!".

On the official website, here's how you can get poetry:

**Mac/Linux/BashOnWindows**
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
**Windows PowerShell**

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

### Step 2: Clone it

You know the drill:

```bash
git clone https://github.com/ThatXliner/ret.git
```
### Step 3: Build it

Poetry has a very handy command: `poetry build`.

What it does is very similar to `python setup.py build sdist bdist_wheel` except that it is **all in *one* command**. Kinda cool, huh?

```bash
poetry build
```

### Step 4: Install it

Since `poetry build` creates an `sdist` (source distribution) and `bdist_wheel` (python wheel binary), you can use `pip` to install the distributions.

```bash
pip install dist/ret-X.X.X-py3-none-any.whl
```

or, if you want to get *really* fancy:

```bash
python3 -m pip install dist/ret-X.X.X-py3-none-any.whl
```

### Step 5: Enjoy it

Though be warned, there may be bugs :bug:!
