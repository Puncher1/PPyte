from cogs.utils.debug import log, LogLevel


log("This is an info", level=LogLevel.INFO, context="test:test_debug")
log("This is a warning", level=LogLevel.WARNING, context="test:test_debug")
log("This is an error", level=LogLevel.ERROR, context="test:test_debug")
log("This is a critical error", level=LogLevel.CRITICAL, context="test:test_debug")
