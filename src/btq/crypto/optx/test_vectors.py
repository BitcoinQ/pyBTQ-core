# Copyright (c) 2026 The BTQ Core developers
# Copyright (c) 2026 OPTX / Jett Optx (jettoptics.ai)
# Distributed under the MIT software license.
#
# Reference test vectors for OP_OPTX_KNOT

import struct
from .knot_witness import KnotWitnessData

# Trefoil: 3_1, DT code = [4, 6, 2], writhe = -3
TREFOIL_DT_CODE = bytes([4, 6, 2, 0, 0, 0])


def trefoil_test_vector() -> KnotWitnessData:
    """Generate trefoil (3_1) test vector for OP_OPTX_KNOT testing."""
    # Alexander: Delta_{3_1}(-1) = -3
    alpha_k = struct.pack(">dd", -3.0, 0.0)
    # Jones: V_{3_1}(-1) = -3
    nu_k = struct.pack(">dd", -3.0, 0.0)
    writhe = -3
    return KnotWitnessData.from_knot(TREFOIL_DT_CODE, alpha_k, nu_k, writhe)


def figure_eight_test_vector() -> KnotWitnessData:
    """Generate figure-eight (4_1) test vector for OP_OPTX_KNOT testing."""
    dt_code = bytes([4, 6, 8, 2, 0, 0])
    # Alexander: Delta_{4_1}(-1) = 5
    alpha_k = struct.pack(">dd", 5.0, 0.0)
    # Jones: V_{4_1}(-1) = -1
    nu_k = struct.pack(">dd", -1.0, 0.0)
    writhe = 0  # Figure-eight is amphicheiral
    return KnotWitnessData.from_knot(dt_code, alpha_k, nu_k, writhe)
