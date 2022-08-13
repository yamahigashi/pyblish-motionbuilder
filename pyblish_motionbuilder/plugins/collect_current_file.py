import os

import pyblish.api

import pyfbsdk as fb


class CollectMotionBuilderCurrentFile(pyblish.api.ContextPlugin):
    """Inject the current working file into context"""

    order = pyblish.api.CollectorOrder - 0.5
    label = "MotionBuilder Current File"

    hosts = ['motionbuilder']
    version = (0, 1, 0)

    def process(self, context):
        """Inject the current working file"""
        fb_app = fb.FBApplication()
        current_file = fb_app.FBXFileName

        # Maya returns forward-slashes by default
        normalised = os.path.normpath(current_file)

        context.set_data('currentFile', value=normalised)

        # For backwards compatibility
        context.set_data('current_file', value=normalised)
