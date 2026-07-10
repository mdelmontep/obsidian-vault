---
title: vitest recoge specs e2e duplicados dentro de .next/standalone tras un build
date: 2026-07-10
source: claude-code-session
tags: [vitest, nextjs, testing]
---
Con `output: standalone`, `next build` copia el repo (incluido `tests/e2e/`) dentro de `.next/standalone/<ruta>/`. El exclude de vitest (`tests/e2e/**`, relativo a la raíz) NO cubre esas copias → `npx vitest run` tras un build reporta decenas de "failed test files" (0 tests, specs de Playwright) que parecen regresión pero son artefacto.

Fix rápido: `rm -rf .next/standalone` antes de la suite completa, o añadir `**/.next/**` al `exclude` de `vitest.config.ts` (mejor, permanente).

Señal para reconocerlo: N ficheros fallidos pero casi 0 tests fallidos, y todas las rutas empiezan por `.next/standalone/`.
