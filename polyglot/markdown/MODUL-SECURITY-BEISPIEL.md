# 🔒 CROD Security Beispiel-Implementierungen

## .env-Handling
```bash
cp .env.example .env
# Niemals .env ins Repo committen!
```

## Post-Quantum Crypto (Python, Pseudocode)
```python
from pqcrypto.kem.kyber512 import generate_keypair, encrypt, decrypt
pk, sk = generate_keypair()
ciphertext, ss = encrypt(pk)
ss2 = decrypt(sk, ciphertext)
assert ss == ss2
```

## ToDo: Sealed Secrets für K8s, Hardware Security Module, Audit-Skripte
