import os

import webbrowser


def get_index_path():
    path = os.path.join(os.path.dirname(__file__), 'poolhub-app', 'dist', 'index.html')
    return path


def launch_index_page():
    path = get_index_path()
    webbrowser.open('file://' + path)
