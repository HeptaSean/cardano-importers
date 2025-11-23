#!/usr/bin/env -S uv run --script
#
# /// script
# dependencies = ["pycardano"]
# ///
import sys
import os
from pycardano import (
    HDWallet,
    PaymentExtendedSigningKey,
    StakeExtendedSigningKey,
    Address,
)
from typing import Tuple


BECH32_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
BECH32_GENERATOR = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]


def bech32_decode(bech32: str) -> Tuple[str, bytearray]:
    """Decode Bech32 string into human-readable part and data."""
    # Check format, divide human-readable and data part
    # and decode characters to 5-bit integers:
    if not bech32 == bech32.lower() and not bech32 == bech32.upper():
        raise ValueError("Bech32 string mixes uppercase and lowercase.")
    bech32 = bech32.lower()
    if "1" not in bech32:
        raise ValueError("Bech32 string has no separator ('1').")
    hrp, _, data_string = bech32.rpartition("1")
    if not hrp:
        raise ValueError("Human-readable part of Bech32 string is empty.")
    if any(ord(char) < 33 or ord(char) > 126 for char in hrp):
        raise ValueError("Invalid character in human-readable part of Bech32 string.")
    if len(data_string) < 6:
        raise ValueError("Data part of Bech32 string is too short.")
    if any(char not in BECH32_CHARSET for char in data_string):
        raise ValueError("Invalid character in data part of Bech32 string.")
    data_int5 = [BECH32_CHARSET.find(char) for char in data_string]
    # Calculate checksum:
    to_check = [ord(char) >> 5 for char in hrp] + [0]
    to_check += [ord(char) & 31 for char in hrp]
    to_check += data_int5
    checksum = 1
    for int5 in to_check:
        top = checksum >> 25
        checksum = (checksum & 0x1FFFFFF) << 5 ^ int5
        for i in range(5):
            checksum ^= BECH32_GENERATOR[i] if ((top >> i) & 1) else 0
    if checksum != 1:
        raise ValueError("Checksum of Bech32 string does not match.")
    # Recode 5-bit integers into bytes:
    data = bytearray()
    bits = 0
    current = 0
    for int5 in data_int5[:-6]:
        bits += 5
        current = (current << 5) + int5
        while bits >= 8:
            bits -= 8
            byte = current >> bits
            data.append(byte)
            current -= byte << bits
    return hrp, data


if len(sys.argv) >= 2:
    xprv_str = sys.argv[1]
else:
    xprv_str = input("Enter the 'xprv1…' key: ").strip()
_, xprv = bech32_decode(xprv_str)
hdwallet = HDWallet.from_seed(xprv.hex())
payment = PaymentExtendedSigningKey.from_hdwallet(hdwallet.derive_from_path("m/0/0"))
stake = StakeExtendedSigningKey.from_hdwallet(hdwallet.derive_from_path("m/2/0"))
address = Address(
    payment.to_verification_key().hash(), stake.to_verification_key().hash()
)
bech32 = address.encode()
print(f"Derived address: {bech32}")
try:
    os.remove("payment.skey")
except OSError:
    pass
payment.save("payment.skey")
try:
    os.remove("stake.skey")
except OSError:
    pass
stake.save("stake.skey")
print("Files payment.skey and stake.skey written to current directory.")
