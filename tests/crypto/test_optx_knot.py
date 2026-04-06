# Copyright (c) 2026 The BTQ Core developers
# Copyright (c) 2026 OPTX / Jett Optx (jettoptics.ai)
# Distributed under the MIT software license.
#
# Tests for OPTX Phase 7: OP_OPTX_KNOT Python bindings

import os
import pytest

from btq.crypto.optx import (
    KnotWitnessData,
    OP_OPTX_KNOT,
    OP_OPTX_KNOT_VERIFY,
    tkdf_derive,
    tkdf_derive_from_witness,
    check_knot_data_bounds,
    build_optx_knot_witness,
    trefoil_test_vector,
    figure_eight_test_vector,
    TREFOIL_DT_CODE,
)


class TestKnotWitnessData:
    def test_trefoil_roundtrip(self):
        tv = trefoil_test_vector()
        data = tv.to_bytes()
        kwd = KnotWitnessData()
        assert kwd.from_bytes(data)
        assert kwd.dt_code == tv.dt_code
        assert kwd.alpha_k == tv.alpha_k
        assert kwd.nu_k == tv.nu_k
        assert kwd.writhe == tv.writhe

    def test_figure_eight_roundtrip(self):
        tv = figure_eight_test_vector()
        data = tv.to_bytes()
        kwd = KnotWitnessData()
        assert kwd.from_bytes(data)
        assert kwd.writhe == 0

    def test_reject_short_data(self):
        kwd = KnotWitnessData()
        assert not kwd.from_bytes(b"\x00" * 10)

    def test_reject_zero_dt_code(self):
        kwd = KnotWitnessData()
        data = b"\x00\x00" + b"\x00" * 38
        assert not kwd.from_bytes(data)


class TestTKDF:
    def test_trefoil_tkdf(self):
        tv = trefoil_test_vector()
        seed = os.urandom(32)
        output = tkdf_derive_from_witness(tv, seed)
        assert len(output) == 64

    def test_figure_eight_tkdf(self):
        tv = figure_eight_test_vector()
        seed = os.urandom(32)
        output = tkdf_derive_from_witness(tv, seed)
        assert len(output) == 64

    def test_different_knots_different_output(self):
        seed = b"\x42" * 32
        out_trefoil = tkdf_derive_from_witness(trefoil_test_vector(), seed)
        out_fig8 = tkdf_derive_from_witness(figure_eight_test_vector(), seed)
        assert out_trefoil != out_fig8

    def test_deterministic(self):
        tv = trefoil_test_vector()
        seed = b"\xaa" * 32
        out1 = tkdf_derive_from_witness(tv, seed)
        out2 = tkdf_derive_from_witness(tv, seed)
        assert out1 == out2

    def test_different_seeds_different_output(self):
        tv = trefoil_test_vector()
        out1 = tkdf_derive_from_witness(tv, b"\x00" * 32)
        out2 = tkdf_derive_from_witness(tv, b"\x01" * 32)
        assert out1 != out2


class TestBounds:
    def test_trefoil_bounds_pass(self):
        tv = trefoil_test_vector()
        assert check_knot_data_bounds(tv.to_bytes())

    def test_figure_eight_bounds_pass(self):
        tv = figure_eight_test_vector()
        assert check_knot_data_bounds(tv.to_bytes())

    def test_reject_oversized(self):
        assert not check_knot_data_bounds(b"\x00" * 513)

    def test_reject_undersized(self):
        assert not check_knot_data_bounds(b"\x00" * 10)


class TestScript:
    def test_build_witness(self):
        sig = b"\x01" * 64
        knot = trefoil_test_vector().to_bytes()
        pubkey = b"\x02" * 32
        witness = build_optx_knot_witness(sig, knot, pubkey)
        assert len(witness) == 4
        assert witness[3] == bytes([OP_OPTX_KNOT])

    def test_build_witness_verify(self):
        sig = b"\x01" * 64
        knot = trefoil_test_vector().to_bytes()
        pubkey = b"\x02" * 32
        witness = build_optx_knot_witness(sig, knot, pubkey, verify=True)
        assert witness[3] == bytes([OP_OPTX_KNOT_VERIFY])
