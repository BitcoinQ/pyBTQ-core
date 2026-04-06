# Copyright (c) 2026 The BTQ Core developers
# Copyright (c) 2026 OPTX / Jett Optx (jettoptics.ai)
# Distributed under the MIT software license.
#
# TKDF — Topological Key Derivation Function
# GENSYS OPTX btQ v1.0, eq. (4)

import struct
import hashlib

from .knot_witness import (
    KnotWitnessData,
    TKDF_ALPHA_SIZE,
    TKDF_NU_SIZE,
    TKDF_SEED_SIZE,
    TKDF_OUTPUT_SIZE,
    TKDF_DOMAIN_TAG,
)


def tkdf_derive(alpha_k: bytes, nu_k: bytes, writhe: int, seed: bytes) -> bytes:
    """
    Topological Key Derivation Function.

    Computes: SHAKE-256(domain_tag || alpha_K || nu_K || omega_K || seed) -> 512 bits

    Args:
        alpha_k: Alexander polynomial evaluation (16 bytes, IEEE 754 complex128 BE)
        nu_k:    Jones polynomial evaluation (16 bytes, IEEE 754 complex128 BE)
        writhe:  Writhe number w(K) (int32)
        seed:    Entropy seed (32 bytes)

    Returns:
        64 bytes of TKDF output for ML-DSA KeyGen seed
    """
    assert len(alpha_k) == TKDF_ALPHA_SIZE, f"alpha_k must be {TKDF_ALPHA_SIZE} bytes"
    assert len(nu_k) == TKDF_NU_SIZE, f"nu_k must be {TKDF_NU_SIZE} bytes"
    assert len(seed) == TKDF_SEED_SIZE, f"seed must be {TKDF_SEED_SIZE} bytes"

    preimage = TKDF_DOMAIN_TAG
    preimage += alpha_k
    preimage += nu_k
    preimage += struct.pack(">i", writhe)
    preimage += seed

    shake = hashlib.shake_256(preimage)
    return shake.digest(TKDF_OUTPUT_SIZE)


def tkdf_derive_from_witness(knot: KnotWitnessData, seed: bytes) -> bytes:
    """Derive TKDF output from KnotWitnessData + seed."""
    return tkdf_derive(knot.alpha_k, knot.nu_k, knot.writhe, seed)
