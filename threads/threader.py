import threading


class Thread(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.parent = threading.current_thread()
        self.status = "Started"
        super(Thread, self).__init__(*args, **kwargs)


def monkey_patch_threads():
    threading.Thread = Thread
