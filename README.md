### ![](https://cloud.githubusercontent.com/assets/2152766/6998101/5c13946c-dbcd-11e4-968b-b357b7c60a06.png)

[![Build Status](https://travis-ci.org/yamahigashi/pyblish-motionbuilder.svg?branch=master)](https://travis-ci.org/yamahigashi/pyblish-motionbuilder)

Pyblish integration for The Autodesk MotionBuilder 2017

<br>
<br>
<br>

### What is included?

A set of common plug-ins and functions shared across other integrations - such as getting the current working file. It also visually integrates Pyblish into the File-menu for easy access.

- Common [plug-ins](https://github.com/yamahigashi/pyblish-motionbuilder/tree/master/pyblish_motionbuilder/plugins)
- Common [functionality](https://github.com/yamahigashi/pyblish-motionbuilder/blob/master/pyblish_motionbuilder__init__.py)
- File-menu shortcut

<br>
<br>
<br>

### Installation

pyblish-motionbuilder depends on [pyblish-base](https://github.com/pyblish/pyblish-base) and is available via PyPI.

```bash
$ pip install pyblish-motionbuilder
```

You may also want to consider a graphical user interface, such as [pyblish-qml](https://github.com/pyblish/pyblish-qml) or [pyblish-lite](https://github.com/pyblish/pyblish-lite).

<br>
<br>
<br>

### Usage

To get started using pyblish-motionbuilder, run `setup()` at startup of your application.

```python
# 1. Register your favourite GUI
import pyblish.api
pyblish.api.register_gui("pyblish_lite")

# 2. Set-up Pyblish for MotionBuilder
import pyblish_motionbuilder
pyblish_motionbuiledr.setup()
```

### Documentation

- [Under the hood](#under-the-hood)
- [Manually show GUI](#manually-show-gui)
- [No menu-item](#no-menu-item)
- [Teardown pyblish-motionbuilder](#teardown-pyblish-motionbuilder)
- [No GUI](#no-gui)

<br>
<br>
<br>

##### Under the hood

The `setup()` command will:

1. Register `motionbuilder` as as a ["host"](http://api.pyblish.com/pages/Plugin.hosts.html) to Pyblish, allowing plug-ins to be filtered accordingly.
2. Append a new menu item, "Publish" to your File-menu
3. Register a minimal set of plug-ins that are common across all integrations.

![image](https://user-images.githubusercontent.com/523673/184475901-d978aad1-2901-4a79-9995-189d97b1bd20.png)

<br>
<br>
<br>

##### No menu-item

Should you not want a menu-item, pass `menu=False`.

```python
import pyblish_motionbuilder
pyblish_motionbuilder.setup(menu=False)
```

<br>
<br>
<br>

##### Manually show GUI

The menu-button is set to run `show()`, which you may also manually call yourself, such as from a button.

```python
import pyblish_motionbuilder
pyblish_motionbuilder.show()
```

<br>
<br>
<br>

##### Teardown pyblish-motionbuilder

To get rid of the menu, and completely remove any trace of pyblish-motionbuilder from your motionbuilder session, run `teardown()`.

```python
import pyblish_motionbuilder
pyblish_motionbuilder.teardown()
```

*This is not implemented yet.*

<br>
<br>
<br>

##### No GUI

*This is not implemented yet.*
