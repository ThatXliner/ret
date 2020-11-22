===
Ret
===
A pure-python command-line regular expression tool for stream filtering, extracting, and parsing.

Installation
-------------

You can install this via

.. code-block:: bash

    python3 -m pip install ret


or using pipx

.. code-block:: bash

    pipx install ret

Ret is pure python (3.6+) with no dependencies.

Usage
------

Example
~~~~~~~~

You can use ``ret`` to extract text via regex capture groups:

.. code-block:: bash

    $ git branch
    * master
    $ git branch | ret "\*\s+(\w+)" --group 1
    master

finding all occurrences of a pattern:

.. code-block:: bash
    $ ls | ret ".*\.py" findall
    foo.py
    bar.py

Background
-------------
I love ``grep``. But grep isn't really for text extraction.

For example, you cannot extract regexes via capture groups.

Since I wanted that functionality, I decided to build this, ``ret``.

Why the name?
~~~~~~~~~~~~~

``Ret`` is an acronym for **r**egular **e**xpression **t**ool.


Why it can't replace grep (yet)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Grep is great for searching directories. Currently, ``ret`` can only read from a file or stdin.

Feel free to contribute!
