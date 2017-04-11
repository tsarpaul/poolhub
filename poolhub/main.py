import threading

from .threads import threader
from .server.server import start_server

threader.monkey_patch_threads()

t = threading.Thread(name="PoolHub Server", target=start_server, daemon=True)
t.start()
