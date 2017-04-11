import threading


class Thread(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.parent = threading.current_thread()
        self.status = "Started"
        self.exception = None
        super(Thread, self).__init__(*args, **kwargs)

    def run(self):
        """just like threading.py def run() but with an except to capture exception"""
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        except Exception as e:
            self.exception = e.__class__.__name__
            raise
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs


def monkey_patch_threads():
    threading.Thread = Thread
