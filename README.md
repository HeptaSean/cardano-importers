# Cardano Importers
Importers for some exotic wallet apps

[Cardano wallet apps](https://cardano.org/what-is-ada#wallets) usually use
24, 15, or 12 word seed phrases to export and import wallets.
It is important to keep those seed phrases safe and secure.
They give full access to the wallet and all its accounts/sub-wallets.
The seed phrases are mostly compatible and users can switch between wallet
apps or use them in parallel by importing a wallet using the seed phrase.

There are [Cardano Improvement Proposals (CIPs)](https://cips.cardano.org/)
for establishing how seed phrases, keys, and wallets should be handled on
Cardano.
The generation of root keys from seed phrases is specified in
[CIP 3](https://cips.cardano.org/cip/CIP-0003), the derivation of account,
payment, and stake keys from these root keys in
[CIP 1852](https://cips.cardano.org/cip/CIP-1852), the construction of
addresses from (the hashes of) these keys in
[CIP 19](https://cips.cardano.org/cip/CIP-0019), and human-readable prefixes
for [Bech32](https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki)
encodings of keys on different levels of the derivation hierarchy in
[CIP 5](https://cips.cardano.org/cip/CIP-0005).

Some wallet apps – especially multi-chain ones – do things differently,
though, and can often not be just imported.
This repository contains some scripts to convert different kinds of
keys/secrets to the `.skey` private key files used by
[`cardano-cli`](https://github.com/IntersectMBO/cardano-cli).
Apart from using `cardano-cli`, these key files can also be imported into
the Cardano wallet app [Eternl](https://eternl.io/) as shown below.

For running these Python scripts, I recommend getting
[`uv`](https://docs.astral.sh/uv/getting-started/installation/).
The scripts are written as single file scripts with their dependencies
specified in the header, so that `uv` can automatically get them.
If you know your Python, you can choose any other preferred method of
installing the dependencies and running the scripts, of course.

## Exodus seed phrases: `exodus2skey.py`

## Atomic private keys: `atomicxprv2skey.py`

## Importing `.skey` files to Eternl
