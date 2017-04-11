import threading

from threads.thread_tree import ThreadNode


class API(object):
    __slots__ = ['main_thread_node', 'thread_node_registry']

    def __init__(self):
        main_thread = threading.main_thread()
        self.main_thread_node = ThreadNode(main_thread)

        self.thread_node_registry = {self.main_thread_node.ident: self.main_thread_node}  # All thread nodes

    def report_threads(self):
        """Watches currently active threads and updates output"""
        #  Main thread contains all children by reference, so we just need him
        thread_tree = {self.main_thread_node.ident: self.main_thread_node.__dict__()}
        return thread_tree

    def watch_threads(self):
        """
        Maps threads to their children and adds them to registry
        Threads that were not listed in threading.enumerate are checked if they're still alive
        """
        while True:
            thread_idents_iterated = []
            for thread in threading.enumerate():
                parent = getattr(thread, 'parent', None)
                if not parent and not thread.ident == self.main_thread_node.ident:  # Not a poolhub thread or MainThread
                    continue

                # Checks if thread is already registered
                thread_node = self.thread_node_registry.get(thread.ident)
                if not thread_node:  # Register thread for the first time
                    thread_node = ThreadNode(thread)
                    self.thread_node_registry[thread_node.ident] = thread_node
                thread_node.update_time()

                thread_idents_iterated.append(thread.ident)

                if not parent:
                    continue

                # Makes sure parent exists in registry and append child into parent node if doesn't exist
                parent_node = self.thread_node_registry.get(parent.ident)
                # Checks if parent is already registered
                if not parent_node:
                    parent_node = ThreadNode(parent)
                    self.thread_node_registry[parent_node.ident] = parent_node
                parent_node.add_child(thread_node)

            # Checks if threads are still alive,
            # if not we erase them from thread_registry and update thread_registry_node
            outdated_threads = [thread_node for ident, thread_node in self.thread_node_registry.items() if
                                ident not in thread_idents_iterated and thread_node.health == 'Alive']
            for thread_node in outdated_threads:
                # Thread state might've been altered in mean time:
                if thread_node.health == 'Alive':
                    thread_node.health = 'Dead'
                    thread_node.status = getattr(thread_node.thread, 'status', 'None')

    def terminate_thread(self, ident):
        self.thread_node_registry[ident].terminate_thread()

    # TODO: Remove this
    def build_thread_tree(self, node):
        """Builds a thread tree starting from node, using thread_registry"""
        sub_tree = {}
        if node.children:
            for child_ident, child in node.children.items():
                sub_tree.update(self.build_thread_tree(child))
        return {node.ident: sub_tree}
