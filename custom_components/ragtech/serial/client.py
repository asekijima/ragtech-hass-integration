import logging
import time

import serial

from .models import MODEL_EASY_PRO, UPS_MODELS
from .parser import parse_data

_LOGGER = logging.getLogger(__name__)

# Command that asks the UPS for its current status. All known Ragtech models
# respond to the same request.
REQUEST_COMMAND = bytes.fromhex("AA0400801E9E")
# The UPS needs a short moment to answer after receiving the request.
READ_DELAY = 2


class RagtechSerialClient:
    def __init__(self, port: str, baud_rate: int, timeout: int, model: str = MODEL_EASY_PRO):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.model = model
        profile = UPS_MODELS.get(model, UPS_MODELS[MODEL_EASY_PRO])
        self._response_length = profile["response_length"]
        self.last_data = None

    def get_status(self):
        try:
            with serial.Serial(self.port, self.baud_rate, timeout=self.timeout) as ser:
                _LOGGER.debug(
                    "[get_status] requesting status on %s @ %s baud (%s)",
                    self.port,
                    self.baud_rate,
                    self.model,
                )
                ser.write(REQUEST_COMMAND)
                time.sleep(READ_DELAY)
                response = ser.read(self._response_length)

                parsed = parse_data(response, self.model)
                if parsed:
                    self.last_data = parsed
                _LOGGER.debug("[get_status] data: %s", parsed)
                return parsed
        except Exception as e:
            _LOGGER.warning("[get_status] error: %s", e)
            return None
