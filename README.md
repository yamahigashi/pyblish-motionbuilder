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

### Persistence


<br>
<br>
<br>
