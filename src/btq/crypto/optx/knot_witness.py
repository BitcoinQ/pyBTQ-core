# Copyright (c) 2026 The BTQ Core developers
# Copyright (c) 2026 OPTX / Jett Optx (jettoptics.ai)
# Distributed under the MIT software license.
#
# KnotWitnessData — serialization for OP_OPTX_KNOT witness stack

import struct

# Opcodes (matching C++ src/script/script.h)
OP_OPTX_KNOT = 0xc0
OP_OPTX_KNOT_VERIFY = 0xc1

# Size constants
TKDF_ALPHA_SIZE = 16     # IEEE 754 complex128
TKDF_NU_SIZE = 16        # IEEE 754 complex128
TKDF_WRITHE_SIZE = 4     # int32 big-endian
TKDF_SEED_SIZE = 32      # 256-bit entropy
TKDF_OUTPUT_SIZE = 64    # SHAKE-256 512-bit output
TKDF_INVARIANT_SIZE = TKDF_ALPHA_SIZE + TKDF_NU_SIZE + TKDF_WRITHE_SIZE  # 36 bytes

# DoS bounds
MAX_DT_CODE_SIZE = 64
MAX_OPTX_CROSSINGS = 16
MAX_OPTX_STRANDS = 7
MAX_OPTX_WORD_LENGTH = 128
MAX_OPTX_KNOT_DATA_SIZE = 512
MAX_OPTX_SPATIAL_SIG_SIZE = 4096

# Domain separator
TKDF_DOMAIN_TAG = b"OPTX-TKDF-v1.0\x00"


class KnotWitnessData:
    """
    Parsed knot data from OP_OPTX_KNOT witness stack.

    Wire format (big-endian):
      [dt_code_len:2] [dt_code:var] [alpha_K:16] [nu_K:16] [writhe:4]
    """

    def __init__(self):
        self.dt_code: bytes = b""
        self.alpha_k: bytes = b"\x00" * TKDF_ALPHA_SIZE
        self.nu_k: bytes = b"\x00" * TKDF_NU_SIZE
        self.writhe: int = 0

    def from_bytes(self, data: bytes) -> bool:
        """Deserialize from witness stack element."""
        if len(data) < 40:
            return False

        offset = 0

        dt_len = struct.unpack_from(">H", data, offset)[0]
        offset += 2

        if dt_len == 0 or dt_len > MAX_DT_CODE_SIZE:
            return False
        if offset + dt_len + TKDF_INVARIANT_SIZE > len(data):
            return False

        self.dt_code = data[offset:offset + dt_len]
        offset += dt_len

        self.alpha_k = data[offset:offset + TKDF_ALPHA_SIZE]
        offset += TKDF_ALPHA_SIZE

        self.nu_k = data[offset:offset + TKDF_NU_SIZE]
        offset += TKDF_NU_SIZE

        self.writhe = struct.unpack_from(">i", data, offset)[0]
        offset += TKDF_WRITHE_SIZE

        return True

    def to_bytes(self) -> bytes:
        """Serialize to witness stack element."""
        result = struct.pack(">H", len(self.dt_code))
        result += self.dt_code
        result += self.alpha_k
        result += self.nu_k
        result += struct.pack(">i", self.writhe)
        return result

    def size(self) -> int:
        return 2 + len(self.dt_code) + TKDF_INVARIANT_SIZE

    @classmethod
    def from_knot(cls, dt_code: bytes, alpha_k: bytes, nu_k: bytes, writhe: int) -> "KnotWitnessData":
        """Create from components."""
        kwd = cls()
        kwd.dt_code = dt_code
        kwd.alpha_k = alpha_k
        kwd.nu_k = nu_k
        kwd.writhe = writhe
        return kwd
