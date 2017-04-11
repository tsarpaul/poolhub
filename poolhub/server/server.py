import asyncio
import threading

import socketio
import aiohttp
import aiohttp.web
import aiohttp_cors
from aiohttp import web

from ..frontend.utils import launch_index_page
from ..threads.threadsAPI import API


def start_server():
    """Should be run a different thread"""
    sio = socketio.AsyncServer(async_mode='aiohttp')

    @sio.on('update')
    async def update_threads(sid, message):
        thread_tree = threads_api.report_threads()
        await sio.emit('reply', room=sid, data={'threads': thread_tree})

    async def terminate_thread(request):
        data = await request.json()
        ident = data['ident']
        response = threads_api.terminate_thread(ident)
        return web.Response(text=response)

    threads_api = API()
    t = threading.Thread(name="PoolHub Watcher", target=threads_api.watch_threads, daemon=True)
    t.start()

    def init_app():
        app = web.Application()
        app.router.add_put('/terminateThread', terminate_thread)
        # Configure default CORS settings.
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })

        # Configure CORS on all routes.
        for route in list(app.router.routes()):
            cors.add(route)
        return app

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = init_app()
    sio.attach(app)

    launch_index_page()  # Launch frontend

    aiohttp.web.run_app(app, port=9876)
