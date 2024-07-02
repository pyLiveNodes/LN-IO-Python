from livenodes.node import Node
from livenodes_core_nodes.ports import Ports_any, Ports_empty


class Out_python(Node):
    """Saves all input into an externally accessible list.

    Saves each process invocation into a list. I.e. if you set the input to
    `emit_at_once=5`, you'll get list entries of size 5. Correspondes to
    the `in_python` interface.

    This data can be accessed via `get_state` on this node in your Python
    process. Useful for testing other nodes or extracting results from
    Livenodes graphs for further external processing.

    Ports In
    --------
    any : Port_Any
        Input data entry to save.

    Methods
    -------
    get_state : list
        Returns the saved data. Datatype of list entries depends on input data.
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
