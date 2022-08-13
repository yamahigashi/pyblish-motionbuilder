import os

import pyblish.api

import pyfbsdk as fb


class CollectMotionBuilderWorkspace(pyblish.api.ContextPlugin):
    """Inject the current workspace into context"""

    order = pyblish.api.CollectorOrder - 0.5
    label = "MotionBuilder Workspace"

    hosts = ['motionbuilder']
    version = (0, 1, 0)

    def process(self, context):
        fb_sys = fb.FBSystem()
        workspace = fb_sys.CurrentDirectory()

        # Maya returns forward-slashes by default
        normalised = os.path.normpath(workspace)

        context.set_data('workspaceDir', value=normalised)

        # For backwards compatibility
        context.set_data('workspace_dir', value=normalised)
