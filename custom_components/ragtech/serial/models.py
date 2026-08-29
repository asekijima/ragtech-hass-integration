"""Per-model calibration profiles for supported Ragtech UPS units.

Each profile carries the response framing (header + total byte length)
and, for every metric, a `(byte_offset, multiplier, additive_offset)`
tuple. The parser applies `value = raw * multiplier + additive_offset`.

Adding a new model = adding a new entry here; the parser, client, and
config flow all derive their behavior from this table.
"""

MODEL_EASY_PRO = "easy_pro"

# Calibration constants originate from reverse-engineering the Ragtech serial
# protocol (see the original ``ragtech.sh`` script) and were validated against a
# multimeter and the official Ragtech app.
UPS_MODELS = {
    MODEL_EASY_PRO: {
        "label": "Easy Pro",
        "header": "aa21",
        "response_length": 64,
        # metric key -> (byte offset, multiplier, additive offset)
        "battery_charge":  (0x08, 0.393, 0),
        "battery_voltage": (0x0B, 0.0671, 0),  # was 0.1342 with a /2 downstream
        "input_voltage":   (0x1A, 1.06, 0),
        "output_current":  (0x0D, 0.120, 0),
        "load":            (0x0E, 1.0, 0),
        "temperature":     (0x0F, 1.0, 0),
        "frequency":       (0x18, -0.1152, 65),
        "output_voltage":  (0x1E, 0.555, 0),
    },
}
