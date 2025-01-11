import inspect
import logging

def print(*objects, sep=" ", **kwargs):
    if not logging.root.isEnabledFor(logging.DEBUG):
        return
    
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    logger_name = module.__name__ if module else "circuitmatter"
    logging.getLogger(logger_name).debug(sep.join([f"{object}" for object in objects]))
