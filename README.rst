===
Ret
===
A pure-python command-line regular expression tool for stream filtering, extracting,
and parsing, designed to be minimal with an intuitive command-line interface.

Installation
-------------

You can install this via

.. code-block:: bash

    python3 -m pip install ret
    ✨🍰✨


or using pipx

.. code-block:: bash

    pipx install ret
    ✨🍰✨

Ret is pure python (3.6+) with no dependencies.

Usage
------

Example
~~~~~~~~

You can use ``Ret`` to extract text via regex capture groups:

.. code-block:: bash

    $ git branch
    * master
    $ git branch | ret "\* (\w+)" --group 1
    master

...finding all occurrences of a pattern:

.. code-block:: bash

    $ ls | ret ".*\.py" findall
    foo.py
    bar.py

and even all occurrences of a pattern **with capture groups**:

.. code-block:: bash

    $ ls | ret "(.*)\.py" findall --group 1
    foo
    bar

And remember, this is python regex: a very powerful regular expression engine.

The possibilities of usage are endless.

Demonstration
~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/ThatXliner/ret/master/assets/demo.svg
   :alt: Demonstration photo


This is only just *one* use case.

Background
-------------
I love ``grep``. But grep isn't really for text extraction.

For example, you cannot extract regexes via capture groups.

Since I wanted that functionality, I decided to build this, ``Ret``.

Why the name?
~~~~~~~~~~~~~

``Ret`` is an acronym for **r**\ egular **e**\ xpression **t**\ ool.


Why it can't replace grep (yet)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Ret`` originally was designed to provide some features ``grep`` lacks.
It never intended to replace good ol' ``grep``.

Grep is great for searching directories while
``ret`` (currently) can only read from a file or stdin.

Furthermore, you cannot guarantee that ``ret`` is installed on the machine.

Also, ``Ret`` relies on the (slow) python regex engine.

Feel free to contribute!
