import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor


def await_coroutine(coroutine, timeout_s: float = 30):
    """Await an async method in a sync context."""

    def run_in_new_loop():
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        try:
            return new_loop.run_until_complete(coroutine)
        finally:
            new_loop.close()

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coroutine)

    if threading.current_thread() is threading.main_thread():
        if not loop.is_running():
            return loop.run_until_complete(coroutine)
        else:
            with ThreadPoolExecutor() as pool:
                future = pool.submit(run_in_new_loop)
                return future.result(timeout=timeout_s)
    else:
        return asyncio.run_coroutine_threadsafe(coroutine, loop).result()
