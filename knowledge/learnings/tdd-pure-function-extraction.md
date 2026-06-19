---
title: extraer función pura antes del componente/hook acelera TDD sin DOM
date: 2026-06-19
source: claude-code-session
tags: [tdd, react, testing, arquitectura]
---

## Patrón

Antes de escribir un componente React o hook con lógica no-trivial, extrae esa lógica a funciones puras en un archivo `lib/`. Testéalas con Vitest sin `@testing-library` ni mocks de Next.js. Luego el componente/hook solo llama a esas funciones — sus tests son más simples y rápidos.

## Casos de uso

- `getPageRange(page, total) → PageItem[]` — lógica de pills con elipsis, 11 tests sin DOM
- `parsePaginationParams(url, stored) → {page, limit}` — parsing + normalización, 13 tests sin router
- cualquier transformación de datos, formateo, validación, cálculo de layout

## Beneficio concreto

Los tests de funciones puras corren en <100ms y no necesitan jsdom. Los tests de componente (más lentos, más frágiles) solo verifican que la función pura está conectada y la UI reacciona, no la lógica en sí.

## Anti-patrón

Meter `getPageRange` dentro del componente como lógica inline → para testearla necesitas montar el componente con `render()`, simular props, e inspeccionar el DOM. 5× más código, 10× más lento.
