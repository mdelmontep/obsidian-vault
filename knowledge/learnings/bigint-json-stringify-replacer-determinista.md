---
name: bigint-json-stringify-replacer-determinista
description: JSON.stringify lanza con BigInt — replacer obligatorio en hashes deterministas sobre céntimos enteros.
date: 2026-05-22
source: claude-code-session
tags: [typescript, bigint, hash, determinismo]
---

**Gotcha**: `JSON.stringify(123n)` → `TypeError: Do not know how to serialize a BigInt`. Pasa sistemáticamente al hashear datos monetarios calculados en céntimos enteros (BigInt evita drift float).

**Fix canónico** (`src/lib/fiscal/hash.ts` patrón):
```ts
const bigintReplacer = (_: string, v: unknown) =>
  typeof v === 'bigint' ? v.toString() : v

JSON.stringify(payload, bigintReplacer)
```

**Reglas para hash determinista con BigInts**:
1. Replacer convierte cada BigInt a su `toString()` decimal exacto
2. Ordenar las claves del objeto alfabéticamente antes de serializar (`Object.fromEntries(Object.entries(o).sort(...))`)
3. Ordenar arrays de IDs antes (`[...ids].sort()`)
4. Incluir `version_calculador` para evitar colisión entre versiones del motor
5. Probar: mismo input dos veces → mismo hash; mismo input con BigInt enorme (`10n**18n`) → no throw

**Aplicable**: hash Verifactu, hash fiscal (303/130), hash conciliación, snapshot inmutable de cualquier cálculo monetario. Sin replacer, los tests pasan solo si por casualidad ningún campo es BigInt — fallo latente.
