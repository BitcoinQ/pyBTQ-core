# Copyright (c) 2026 The BTQ Core developers
# Copyright (c) 2026 OPTX / Jett Optx (jettoptics.ai)
# Distributed under the MIT software license.
#
# DoS bounds checking for OP_OPTX_KNOT witness data

import struct

from .knot_witness import (
    MAX_OPTX_KNOT_DATA_SIZE,
    MAX_DT_CODE_SIZE,
    MAX_OPTX_CROSSINGS,
)


def check_knot_data_bounds(data: bytes) -> bool:
    """
    Validate knot witness data bounds (DoS protection).
    Matches C++ CheckKnotDataBounds().
    """
    if len(data) > MAX_OPTX_KNOT_DATA_SIZE:
        return False
    if len(data) < 40:
        return False

    dt_len = struct.unpack_from(">H", data, 0)[0]
    if dt_len == 0 or dt_len > MAX_DT_CODE_SIZE:
        return False

    num_crossings = dt_len // 2
    if num_crossings > MAX_OPTX_CROSSINGS:
        return False
    if num_crossings < 3:
        return False

    return True
