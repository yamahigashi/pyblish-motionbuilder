
try:
    __import__("pyblish_motionbuilder")

except ImportError as e:
    import traceback
    print("pyblish-motionbuilder: Could not load integration: %s"
          % traceback.format_exc())
    print(e)

else:
    import pyblish_motionbuilder
    pyblish_motionbuilder.setup()
