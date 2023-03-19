from cogs.utils.debug import log, LogLevel


log("This is an info", level=LogLevel.INFO, context="test:test_debug")
log("This is a warning", level=LogLevel.WARNING)
log("This is an error", level=LogLevel.ERROR)
log("This is a critical error", level=LogLevel.CRITICAL)

try:
    log("This is a critical error", level=None)
except Exception as e:
    print(f"1\t{e.__class__.__name__}: {e}")

try:
    log("This is a critical error", level=LogLevel.CRITICAL, context=None)
except Exception as e:
    print(f"2\t{e.__class__.__name__}: {e}")
