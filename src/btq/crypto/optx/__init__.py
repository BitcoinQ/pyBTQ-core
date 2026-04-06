# OPTX Phase 7: Topological Key Derivation Function (TKDF)
# GENSYS OPTX btQ v1.0 — OP_OPTX_KNOT Python bindings
#
# BIP: https://github.com/bitcoin/bips/pull/2133
# Ref: btq-ag/btq-core Phase 7

from .knot_witness import (
    KnotWitnessData,
    OP_OPTX_KNOT,
    OP_OPTX_KNOT_VERIFY,
    TKDF_DOMAIN_TAG,
    MAX_OPTX_CROSSINGS,
    MAX_OPTX_STRANDS,
    MAX_OPTX_WORD_LENGTH,
)
from .tkdf import (
    tkdf_derive,
    tkdf_derive_from_witness,
)
from .bounds import (
    check_knot_data_bounds,
)
from .script import (
    build_optx_knot_witness,
)
from .test_vectors import (
    trefoil_test_vector,
    figure_eight_test_vector,
    TREFOIL_DT_CODE,
)

__all__ = [
    "KnotWitnessData",
    "OP_OPTX_KNOT",
    "OP_OPTX_KNOT_VERIFY",
    "TKDF_DOMAIN_TAG",
    "MAX_OPTX_CROSSINGS",
    "MAX_OPTX_STRANDS",
    "MAX_OPTX_WORD_LENGTH",
    "tkdf_derive",
    "tkdf_derive_from_witness",
    "check_knot_data_bounds",
    "build_optx_knot_witness",
    "trefoil_test_vector",
    "figure_eight_test_vector",
    "TREFOIL_DT_CODE",
]
