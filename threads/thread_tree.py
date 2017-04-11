import ctypes
import time


class ThreadNode(object):
    """A ThreadNode used in building the thread tree"""
    __slots__ = ['ident', 'name', 'thread', 'health', 'exception', 'status', 'daemon', 'children', 'last_updated']

    def __init__(self, thread):
        self.ident = thread.ident
        self.name = thread.name
        self.thread = thread
        self.health = 'Alive'
        self.status = getattr(thread, 'status', None)
        self.exception = getattr(thread, 'exception', None)
        self.daemon = thread.daemon
        self.children = {}
        self.last_updated = str(time.time())

    def add_child(self, child):
        if not isinstance(child, ThreadNode):
            raise ValueError('Child must be a ThreadNode object')
        self.children.update({child.ident: child})
        self.update_time()

    def terminate_thread(self):
        self.health = 'Terminating'
        # Raise KeyboardInterrupt to crash the thread
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(self.ident), ctypes.py_object(KeyboardInterrupt)
        )
        if res:  # Success
            self.health = 'Terminated'
        else:
            self.health = 'Alive'

        return res

    def update_time(self):
        self.last_updated = str(time.time())

    def handle_exception(self):
        self.exception = self.thread.exception
        self.health = 'Crashed'

    def __dict__(self):
        return {'ident': self.ident,
                'name': self.name,
                'health': self.health,
                'daemon': self.daemon,
                'status': self.status or 'None',
                'exception': self.exception or 'None',
                'children': {ident: child.__dict__() for ident, child in self.children.items()},
                'updated': self.last_updated}
