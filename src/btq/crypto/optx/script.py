# Copyright (c) 2026 The BTQ Core developers
# Copyright (c) 2026 OPTX / Jett Optx (jettoptics.ai)
# Distributed under the MIT software license.
#
# Script construction helpers for OP_OPTX_KNOT

from .knot_witness import OP_OPTX_KNOT, OP_OPTX_KNOT_VERIFY


def build_optx_knot_witness(spatial_sig: bytes, knot_data: bytes, pubkey: bytes,
                             verify: bool = False) -> list:
    """
    Build OP_OPTX_KNOT witness stack items.

    Stack layout: [spatial_sig, knot_data, pubkey, opcode_byte]
    """
    opcode = OP_OPTX_KNOT_VERIFY if verify else OP_OPTX_KNOT
    return [spatial_sig, knot_data, pubkey, bytes([opcode])]
