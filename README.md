# Prototype Pollution (`prototype-pollution`)

**Category:** web · **Difficulty:** hard · **Points:** 350

A deep-merge of user JSON pollutes Object.prototype, flipping an admin gate.

## Run it

```bash
docker build -t sparflag/prototype-pollution .
# `deca-ai start prototype-pollution` (or the web UI) prints the docker run line with your
# SPARFLAG_SERVER + SPARFLAG_INSTANCE_TOKEN
```

## Recover the flag

The delivery blob is Fernet ciphertext. Discover the key seed, derive the Fernet key, then decrypt.

The plaintext flag is never written to disk or served — only the encoded delivery blob
is. When you have it:

```bash
deca-ai submit prototype-pollution 'sparflag{...}'
```

## Hints

- Send __proto__ in your JSON body.
- Pollute a flag that the admin check reads, then fetch the seed.
