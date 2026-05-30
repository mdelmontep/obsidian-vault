---
title: Renombrar import en handler → actualizar TODOS los `vi.mock` que mockean ese path
date: 2026-05-30
source: facturaia Fase 2.6 — 52 tests rotos por mocks contra path legacy
tags: [tests, vitest, refactor, mocks]
---

Cuando renombras el import de un módulo en código de producción (e.g. `@/lib/voice/auth` → `@/lib/internal/auth`), Vitest **NO actualiza automáticamente** los `vi.mock('@/lib/voice/auth', ...)` de los tests. El mock queda apuntando al path viejo que ya no se importa, y el código real se ejecuta sin mock → tests rompen masivamente.

Síntoma típico en facturaia Fase 2.6: tras migrar 22 rutas de `requireServiceKey` a `requireServiceAuth`, 52 tests fallaron porque sus `vi.mock` seguían apuntando al módulo legacy.

Fix mecánico:

```ts
// antes
vi.mock('@/lib/voice/auth', () => ({
  requireServiceKey: (req: Request) => null,
}))

// después
vi.mock('@/lib/internal/auth', () => ({
  requireServiceAuth: (req: Request, body: string) => null,  // ← nueva firma
}))
```

Comprobaciones antes de pushear el refactor:

1. `grep -rln 'vi.mock.*lib/voice/auth' src/` → ¿algún test sin migrar?
2. `npx vitest run` localmente, no solo tests del directorio modificado.
3. Si el mock acepta args, **migrar también la firma del mock** — `requireServiceKey(req)` (1 arg) vs `requireServiceAuth(req, body)` (2 args). Tests que verifican llamadas con `.toHaveBeenCalledWith(req)` rompen.

Patrón sed útil para migraciones repetitivas:

```bash
for f in test1.ts test2.ts ...; do
  sed -i '' \
    -e "s|vi.mock('@/lib/old/path', () => ({$|vi.mock('@/lib/new/path', () => ({|" \
    -e "s|  requireServiceKey: (req: Request) => requireServiceKeyMock(req),|  requireServiceAuth: (req: Request, body: string) => requireServiceAuthMock(req, body),|" \
    -e 's|requireServiceKeyMock|requireServiceAuthMock|g' \
    "$f"
done
```

Casos especiales que sed no cubre:
- `vi.doMock` dentro de un test concreto (override del mock global).
- Mocks con shape custom (no solo `() => null`).
- Tests que usan `vi.importActual` y solo overridean ciertos exports.

Estos requieren edición manual.

Anti-pattern: dejar el mock viejo "por si acaso". Vitest no warna sobre mocks no consumidos — el mock queda fantasma y el siguiente refactor lo encuentra todavía ahí confundiendo.

[[migrar-auth-wrapper-default-vs-handler-por-handler]] [[vitest-vi-fn-sin-params-rompe-spread-args]]
