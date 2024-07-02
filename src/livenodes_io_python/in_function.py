import asyncio
import numpy as np

from livenodes.producer_async import Producer_async

from livenodes_core_nodes.ports import Port_Dict, Port_Data, Port_List_Str, Ports_empty
from typing import NamedTuple


class Ports_out(NamedTuple):
    data: Port_Data = Port_Data("Data")
    channels: Port_List_Str = Port_List_Str("Channel Names")
    meta: Port_Dict = Port_Dict("Meta")


class In_function(Producer_async):
    """ """

    ports_in = Ports_empty()
    ports_out = Ports_out()

    category = "Data Source"
    description = ""

    example_init = {
        "function": "sin",
        "meta": {"sample_rate": 100, "targets": ["target 1"], "channels": ["Channel 1"]},
        "emit_at_once": 1,
        "name": "Data input",
    }

    # TODO: consider using a file for meta data instead of dictionary...
    def __init__(self, meta, function="sin", emit_at_once=1, name="Function Input", **kwargs):
        super().__init__(name, **kwargs)

        self.meta = meta
        self.function = function
        self.emit_at_once = emit_at_once

        self.sample_rate = meta.get('sample_rate')
        self.targets = meta.get('targets')
        self.channels = meta.get('channels')

    def _settings(self):
        return {"emit_at_once": self.emit_at_once, "function": self.function, "meta": self.meta}

    async def _async_run(self):
        self.ret_accu(self.meta, port=self.ports_out.meta)
        self.ret_accu(self.channels, port=self.ports_out.channels)

        ctr = 0
        n_channels = len(self.channels)

        time_to_sleep = 1.0 / self.sample_rate * self.emit_at_once
        # last_emit_time = time.time()

        def linear(x):
            return x / 1000

        try:
            fn = getattr(np, self.function)
        except:
            self.error(f'Could not find {self.function}. Defaulting to linear.')
            fn = linear

        while True:
            samples = np.linspace(ctr, ctr + self.emit_at_once, 1)
            res = fn(samples)
            res = np.array([np.array([res] * n_channels).T])
            self.ret_accu(res, port=self.ports_out.data)

            ctr += self.emit_at_once

            # process_time = time.time() - last_emit_time
            # if time_to_sleep > process_time:
            #     await asyncio.sleep(time_to_sleep - process_time)
            await asyncio.sleep(time_to_sleep)

            yield self.ret_accumulated()
            # last_emit_time = time.time()
