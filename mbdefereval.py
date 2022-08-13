# -*- coding: utf-8 -*-
"""Deferred evaluation module for MotionBuilder.

This code is inspired by hdefereval.py from SideFx Houdini.

https://docs.python.org/3/library/threading.html#condition-objects
http://docs.autodesk.com/MOBPRO/2017/ENU/MotionBuilder-Developer-Help/index.html#!/url=py_ref/class_f_b_system.html#a8264ab3ccd6e7001ca8763549294e2b8
http://docs.autodesk.com/MOBPRO/2017/ENU/MotionBuilder-Developer-Help/index.html#!/url=./files/GUID-2A900B42-AC78-44A0-BA39-74F7D6D39133.htm


import mbdefereval as e
def x():
    print("foo")

e.executeInMainThreadWithResult(x)
"""

import sys
import time
import traceback

if sys.version_info >= (3, 0):  # pylint: disable=using-constant-test
    from queue import Queue
else:
    from Queue import Queue

import pyfbsdk as fb  # type: ignore

if sys.version_info >= (3, 0):  # pylint: disable=using-constant-test
    # For type annotation
    from typing import (  # NOQA: F401 pylint: disable=unused-import
        Dict,
        Tuple,
        Callable,
        Any,
        Text,
        Union,
    )

    # type alias
    Code = Union[Callable, Text]
    JobData = Tuple[Code, bool, Tuple, Dict]  # code, block, args, kwargs


# -----------------------------------------------------------------------------
_queue = Queue()  # type: Queue[JobData]
_last_result = None
_last_exc_info = None
_fb_sys = fb.FBSystem()
_is_running = False

MAXIMUM_SECONDS_IN_ONE_TICK = 1.0


# -----------------------------------------------------------------------------
def execute_deferred(code, *args, **kwargs):
    # type: (Code, Tuple, Dict) -> None
    """Run the code in MotionBuilder"""
    _enqueue(code, args, kwargs, block=False)


def execute_in_main_thread_with_result(code, *args, **kwargs):
    # type: (Code, Tuple, Dict) -> Any
    """Run the code in MotionBuilder with result"""

    return _enqueue(code, args, kwargs, block=True)


def _enqueue(code, args, kwargs, block):
    # type: (Code, Tuple, Dict, bool) -> Any
    """Put a job on the queue. if block set True wait done and return value"""

    # If text expression is specified as code, any argument is not supported.
    if all((
        not callable(code),
        (len(args) + len(kwargs)) != 0
    )):
        raise ValueError(
            "You cannot pass arguments unless you pass in a callable object")

    _register_event_loop_callback()
    _queue.put((code, block, args, kwargs), block=block)

    if block:
        _queue.join()

        if _last_exc_info is None:
            return _last_result

        traceback.print_exception(*_last_exc_info)
        raise _last_exc_info[1]

    return None


# -----------------------------------------------------------------------------
def _register_event_loop_callback():
    # type: () -> None
    """Add the event loop callback if it has not already been added."""
    global _is_running

    if not _is_running:
        _fb_sys.OnUIIdle.Add(_process_deferred_wrapper)
        _is_running = True


def _deregister_event_loop_callback():
    # type: () -> None
    """Remove the event loop callback."""
    global _is_running

    _fb_sys.OnUIIdle.Remove(_process_deferred_wrapper)
    _is_running = False


def _process_deferred_wrapper(_control, _event):
    # type: (fb.FBSystem, fb.FBEvent) -> None
    """Invoked from MotionBuilder. If the processing time exceeds the
    MAXIMUM_SECONDS_IN_ONE_TICK, the subsequent job on the queue will be
    sent to the next tick.
    """

    start_time = time.time()
    elapsed_time = 0.0

    while elapsed_time < MAXIMUM_SECONDS_IN_ONE_TICK:
        _process_deferred()
        elapsed_time = time.time() - start_time


# -----------------------------------------------------------------------------
def _process_deferred():
    # type: () -> None
    """Run the queued job whose execution has been deferred."""
    global _last_result, _last_exc_info

    if _queue.empty():
        _deregister_event_loop_callback()
        return

    code, notify, args, kwargs = _queue.get()

    exc_info = None
    try:
        if callable(code):
            result = code(*args, **kwargs)
        else:
            # TODO: to rewrite with  ast.literal_eval
            result = eval(code, __import__('__main__').__dict__)

    except Exception:
        exc_info = (sys.exc_type, sys.exc_value, sys.exc_traceback)  # type: ignore
        result = None

    finally:
        _queue.task_done()

    if notify:
        _last_exc_info = exc_info
        _last_result = result

    elif exc_info is not None:
        traceback.print_exception(*exc_info)


# -----------------------------------------------------------------------------
# shourtcuts
executeDeferred = execute_deferred
executeInMainThreadWithResult = execute_in_main_thread_with_result
