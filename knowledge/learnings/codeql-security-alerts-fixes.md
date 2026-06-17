---
title: codeql code scanning (seguridad) — rest sí funciona; recetas de fix js recurrentes
date: 2026-06-17
source: claude-code-session
tags: [github, codeql, code-scanning, security, regex]
---
Code Scanning (seguridad) ≠ Code Quality (preview): aquí el REST **sí** funciona —
`gh api repos/X/code-scanning/alerts` (list) y `PATCH .../alerts/N -f state=dismissed
-f dismissed_reason="false positive|won't fix|used in tests" -f dismissed_comment=...`.
El auto-mode de Claude BLOQUEA el PATCH (escritura externa masiva sobre items que no creó)
→ el user lo corre con `!` en el prompt. Complementa [[github-code-quality-triage]].

Recetas de fix recurrentes (no obvias, validadas PR #337):
- `js/bad-tag-filter`: `</script\s*>` NO basta (CodeQL exige cubrir `</script\n bar>`, que el
  navegador trata como cierre) → `<\/script(?:\s[^>]*)?>`. Igual para style/head.
- `js/polynomial-redos` email: `[^\s@]+@[^\s@]+\.[^\s@]+` es ambiguo (`.` ∈ ambos lados) →
  `^[^\s@]+@(?:[^\s@.]+\.)+[^\s@.]+$` (segmentos sin punto, determinista).
- `js/incomplete-multi-character-sanitization`: aplicar el replace en bucle hasta estabilizar
  (anidamiento `<scr<script>ipt>` se reconstruye en una sola pasada).
- `js/biased-cryptographic-random`: `randomBytes % N` sesga → rejection sampling.
FP típicos a dismiss: blob URL en img.src, Math.random en datos seed/mock, substring-check en asserts de test.
