from livenodes.producer import Producer
from livenodes_core_nodes.ports import Ports_any, Ports_empty


class In_python(Producer):
    """
    Input any python data into the livenodes graph.
    Mostly for debug purposes and fast iterations.
    In the long run I would expect a custom node to always be more efficient

    Data should be a list of items to be sent into the graph.
    """

    ports_in = Ports_empty()
    ports_out = Ports_any()

    category = "Data Source"
    description = ""

    example_init = {"name": "Python In"}

    def __init__(self, name="Python In", data=[], **kwargs):
        super().__init__(name, **kwargs)
        self.data = data

    def _run(self):
        for val in self.data:
            yield self.ret(any=val)
