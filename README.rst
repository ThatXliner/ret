===
Ret
===
A pure-python command-line regular expression tool for stream filtering, extracting,
and parsing, designed to be minimal with an intuitive command-line interface.

Installation
-------------

You can install this via

.. code-block:: bash

    $ python3 -m pip install ret
    ✨🍰✨


or using pipx

.. code-block:: bash

    $ pipx install ret
    ✨🍰✨

Ret is pure python (tested on python 3.6+) with no dependencies.

That way, you can get a clean uninstall.

.. note::

	If you want to install the bleeding edge version of ret, right when it gets pushed to master, see `here <https://github.com/ThatXliner/ret/blob/master/CONTRIBUTING.md#development-installation>`_ for instructions.



Usage
------

Example
~~~~~~~~

You can use ``Ret`` to extract text via regex capture groups:

.. code-block:: bash

    $ git branch
    * master
    $ git branch | ret "\* (\w+)" s --group 1
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


While those may seem untypical use cases, I have found myself using ``Ret`` countless times.

Here's a one-liner for uninstalling unnecessary stuff for ``pip``:

.. code-block:: bash

   $ pip list --not-required | ret ".+\n.+\n((?:\n|.)+)" f -g 1 | ret "([^\s]+)\s+.+\n" f -g 1 | xargs pip uninstall --yes


Another case
~~~~~~~~~~~

Imagine this: you have just downloaded a bunch of tarballs, and have ran

.. code-block:: bash

   for x in $(grep ".+\.tar\.gz"); do tar -xzf $x; done

Now you just want to ``cd`` into all of the extracted files, run :code:`./configure && make && make install`.

You could use ``Ret`` to get the names of the extracted files, just from the tarballs' names. Like this:

.. code-block:: bash

   $ ls | grep ".+\.tar\.gz"
   foo.tar.gz
   bar.tar.gz
   foobar.tar.gz
   extractme.tar.gz


   $ ls | ret "(.+\.tar\.gz)" f -g 1
   foo
   bar
   foobar
   extractme


and with that combined, we can do

.. code-block:: bash

   $ for x in (ls | ret "(.+\.tar\.gz)" f -g 1); do {
      current_dir=`pwd`;
      cd $current_dir &&
      ./configure && make && make install &&
      cd $current_dir}; done
   ✨🍰✨

A life saver.

----

And remember, this is python regex: a very powerful regular expression engine.

The possibilities of usage are endless.

Demonstration
~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/ThatXliner/ret/master/assets/demo.svg
   :alt: Demonstration photo


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
