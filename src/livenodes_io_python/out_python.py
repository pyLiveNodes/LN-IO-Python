from livenodes.node import Node
from livenodes_core_nodes.ports import Ports_any, Ports_empty


class Out_python(Node):
    """
    Saves all input from the 'any' port into a mp.SimpleQueue.
    This data can be accessed via 'get_state' on this node in your python process.

    Saves each process invocation into a list.
    I.e. if you set the input to emit_at_once=5, you'll get list entries of size 5.
    Correspondes to the in_python interface.

    The node must run in the same python process as the process you want to access the data from.
    I have looked into shared mem to allow subprocesses, but found that quite often the mp.queue.put() blocks if the queue is even partially full and then blocks the full livenode graph
    """

    ports_in = Ports_any()
    ports_out = Ports_empty()

    category = "Data Sink"
    description = ""

    example_init = {"name": "Python Out"}

    def __init__(self, name="Python Out", **kwargs):
        super().__init__(name, **kwargs)
        self.out = []

    def process(self, any, **kwargs):
        self.out.append(any)

    def get_state(self):
        return self.out
