# Standard library
import os
import sys
import contextlib

# Pyblish libraries
import pyblish
import pyblish.api

# Host libraries
import pyfbsdk as fb

# Local libraries
from . import plugins

self = sys.modules[__name__]
self._has_been_setup = False
self._has_menu = False
self._registered_gui = None
self._dock = None
self._dock_control = None


def setup(menu=True):
    """Setup integration

    Registers Pyblish for Motionbuilder plug-ins and appends an item to the File-menu

    Attributes:
        console (bool): Display console with GUI
        port (int, optional): Port from which to start looking for an
            available port to connect with Pyblish QML, default
            provided by Pyblish Integration.

    """

    if self._has_been_setup:
        teardown()

    register_plugins()
    register_host()

    if menu:
        add_to_filemenu()
        self._has_menu = True

    self._has_been_setup = True
    print("Pyblish loaded successfully.")


def show():
    """Try showing the most desirable GUI

    This function cycles through the currently registered
    graphical user interfaces, if any, and presents it to
    the user.

    """
    from Qt import QtWidgets

    parent = next(
        o for o in QtWidgets.QApplication.instance().topLevelWidgets()
        if "MotionBuilder " in o.windowTitle()
    )

    try:
        pyqt5 = os.path.abspath(os.path.join(os.getenv("PYBLISH_QML_PYQT5"), "../"))
        sys.path.append(pyqt5)
        os.environ["QT_PREFERRED_BINDING"] = "PySide"
    except TypeError:
        pass

    gui = _discover_gui()

    if gui is None:
        _show_no_gui()
    else:
        return gui(parent)



def _discover_gui():
    """Return the most desirable of the currently registered GUIs"""

    # Prefer last registered
    guis = reversed(pyblish.api.registered_guis())

    for gui in guis:
        try:
            gui = __import__(gui).show
        except (ImportError, AttributeError):
            continue
        else:
            return gui


def teardown():
    """Remove integration"""
    if not self._has_been_setup:
        return

    deregister_plugins()
    deregister_host()

    if self._has_menu:
        remove_from_filemenu()
        self._has_menu = False

    self._has_been_setup = False
    print("pyblish: Integration torn down successfully")


def deregister_plugins():
    # Register accompanying plugins
    plugin_path = os.path.dirname(plugins.__file__)
    pyblish.api.deregister_plugin_path(plugin_path)
    print("pyblish: Deregistered %s" % plugin_path)


def register_host():
    """Register supported hosts"""
    pyblish.api.register_host("motionbuilderbatch")
    pyblish.api.register_host("motionbuilder")


def deregister_host():
    """Register supported hosts"""
    pyblish.api.deregister_host("motionbuilderbatch")
    pyblish.api.deregister_host("motionbuilder")


def register_plugins():
    # Register accompanying plugins
    plugin_path = os.path.dirname(plugins.__file__)
    pyblish.api.register_plugin_path(plugin_path)
    print("pyblish: Registered %s" % plugin_path)


def add_to_filemenu():
    """Add Pyblish to file-menu"""
    # FIXME: if batch mode, return

    def eventMenu(control, event):
        if "Publish" == event.Name:
            import pyblish_motionbuilder
            try:
                pyblish_motionbuilder.show()

            except Exception:
                import traceback
                traceback.print_exc()

    menu_mgr = fb.FBMenuManager()
    menu = menu_mgr.GetMenu("File")  # type: fb.FBGenericMenuItem
    last = int(menu.GetLastItem().Id)
    before = last
    for i in range(last):
        cursor = menu.GetItem(i)

        if not cursor:
            # id of absence
            continue

        if "Publish" in cursor.Caption:
            # menu already exists
            break

        if "Batch" in cursor.Caption:
            before = cursor

    else:
        # add menu
        menu.InsertBefore(before, "", last + 1)
        menu.InsertBefore(before, "Publish", last + 2)  # type: fb.FBGenericMenuItem
        menu.InsertBefore(before, "", last + 3)

        menu.OnMenuActivate.Add(eventMenu)


def remove_from_filemenu():
    raise NotImplementedError


@contextlib.contextmanager
def maintained_selection():
    """Maintain selection during context

    Example:
        >>> with maintained_selection():
        ...     # Modify selection
        ...     cmds.select('node', replace=True)
        >>> # Selection restored

    """

    previous_selection = fb.FBModelList()
    parent = None
    selected = True
    reserve_order = True
    fb.FBGetSelectedModels(previous_selection, parent, selected, reserve_order)

    try:
        yield

    finally:
        current_selection = fb.FBModelList()
        fb.FBGetSelectedModels(current_selection, parent, selected, reserve_order)

        for model in current_selection:
            model.Select(False)

        if previous_selection:

            for model in previous_selection:
                model.Select(True)


@contextlib.contextmanager
def maintained_time():
    """Maintain current time during context

    Example:
        >>> with maintained_time():
        ...    cmds.playblast()
        >>> # Time restored

    """

    ct = cmds.currentTime(query=True)
    try:
        yield

    finally:
        cmds.currentTime(ct, edit=True)


def _show_no_gui():
    """Popup with information about how to register a new GUI

    In the event of no GUI being registered or available,
    this information dialog will appear to guide the user
    through how to get set up with one.

    """
    from Qt import QtWidgets, QtGui

    messagebox = QtWidgets.QMessageBox()
    messagebox.setIcon(messagebox.Warning)
    messagebox.setWindowIcon(QtGui.QIcon(os.path.join(
        os.path.dirname(pyblish.__file__),
        "icons",
        "logo-32x32.svg"))
    )

    spacer = QtWidgets.QWidget()
    spacer.setMinimumSize(400, 0)
    spacer.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                         QtWidgets.QSizePolicy.Expanding)

    layout = messagebox.layout()
    layout.addWidget(spacer, layout.rowCount(), 0, 1, layout.columnCount())

    messagebox.setWindowTitle("Uh oh")
    messagebox.setText("No registered GUI found.")

    if not pyblish.api.registered_guis():
        messagebox.setInformativeText(
            "In order to show you a GUI, one must first be registered. "
            "Press \"Show details...\" below for information on how to "
            "do that.")

        messagebox.setDetailedText(
            "Pyblish supports one or more graphical user interfaces "
            "to be registered at once, the next acting as a fallback to "
            "the previous."
            "\n"
            "\n"
            "For example, to use Pyblish Lite, first install it:"
            "\n"
            "\n"
            "$ pip install pyblish-lite"
            "\n"
            "\n"
            "Then register it, like so:"
            "\n"
            "\n"
            ">>> import pyblish.api\n"
            ">>> pyblish.api.register_gui(\"pyblish_lite\")"
            "\n"
            "\n"
            "The next time you try running this, Lite will appear."
            "\n"
            "See http://api.pyblish.com/register_gui.html for "
            "more information.")

    else:
        messagebox.setInformativeText(
            "None of the registered graphical user interfaces "
            "could be found."
            "\n"
            "\n"
            "Press \"Show details\" for more information.")

        messagebox.setDetailedText(
            "These interfaces are currently registered."
            "\n"
            "%s" % "\n".join(pyblish.api.registered_guis()))

    messagebox.setStandardButtons(messagebox.Ok)
    messagebox.exec_()


'''
class Dock(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(Dock, self).__init__(parent)
        QtWidgets.QVBoxLayout(self)
        self.setObjectName("pyblish_motionbuilder.dock")
'''


def dock(window):

    from Qt import QtWidgets, QtGui
    main_window = None
    for obj in QtWidgets.qApp.topLevelWidgets():
        if obj.objectName() == "MotionbuilderWindow":
            main_window = obj

    if not main_window:
        raise ValueError("Could not find the main Motionbuilder window.")

    # Deleting existing dock
    print("Deleting existing dock...")
    if self._dock:
        self._dock.setParent(None)
        self._dock.deleteLater()

    # Creating new dock
    print("Creating new dock...")
    dock = Dock(parent=main_window)

    dock_control = cmds.dockControl(label=window.windowTitle(), area="right",
                                    visible=True, content=dock.objectName(),
                                    allowedArea=["right", "left"])
    dock.layout().addWidget(window)

    self._dock = dock
    self._dock_control = dock_control
