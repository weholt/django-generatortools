# django-generatortools
A set of tools to easily generate typical django models and code structure.

$ python -m pip install --upgrade pip
$ pip install wheel
$ pip install check-wheel-contents
$ python setup.py bdist_wheel
$ check-wheel-contents .\dist
$ pip install twine
$ twine upload dist/*