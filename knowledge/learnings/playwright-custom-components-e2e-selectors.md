---
title: playwright — selectores fiables con componentes custom (checkbox, select portal)
date: 2026-06-30
source: claude-code-session
tags: [playwright, e2e, react, shadcn]
---

## Checkbox custom (visually hidden input)

El input nativo está oculto dentro de un `<label>` wrapper. Clickar el input directo puede no disparar el `onChange` de React en headless.

**Fix:** clickar el `<label>` contenedor + esperar con `waitForFunction`:
```
label.mod-config-toggle (wrapper) → click aquí, no en #mc-field-id
await page.waitForFunction(() => document.querySelectorAll('.disabled-class').length >= N)
```

Nota: en **agent-browser** (CDP) el click sobre `[role="option"]` NO funciona igual — ver [[agent-browser-select-custom-click-opcion-no-registra-usar-teclado]].

⚠️ **2026-07-25 — ese selector es un contrato, y está señalado para morir.** `label.mod-config-toggle` envolviendo el checkbox es exactamente el **doble etiquetado** que hace que el nombre accesible salga "Label Activado" y **cambie al alternarlo**. El saneamiento de módulos IA lo sustituye por `<Toggle>` (`issues/modia-015-*`) y el botón `/guardar/i` del mismo spec desaparece al pasar a autoguardado (`issues/modia-025-*`). Regla que sale de aquí: **un assert de E2E sobre un nombre de clase convierte el markup en contrato**, y el refactor que lo rompa debe actualizar el spec en el MISMO commit. Al escribir el assert, preferir rol + nombre accesible; si hay que usar la clase, dejar comentado por qué.

## Select con FloatingPortal (Floating UI / shadcn)

El trigger es `<button role="combobox">`. Las opciones se montan async en body via portal.

**Fix:** esperar `[role="listbox"]` antes de leer opciones:
```
await trigger.click()
await page.locator('[role="listbox"]').waitFor({ timeout: 3000 })
const options = await page.locator('[role="option"]').allTextContents()
```

## Input controlado React — confirmar antes de guardar

`fill()` dispara el evento pero React puede no haber procesado el estado aún al hacer click en Guardar.

**Fix:** `await expect(input).toHaveValue(newValue)` entre `fill()` y el click del botón.

## Label vs valor interno en select

El texto visible de las opciones (`label`) puede diferir del `value` interno. Testear contra el texto visible, no el value.

## filter({ hasNotText }) con badges async

Badge renderizado async puede no estar en DOM cuando el filter evalúa → candidata pasa el filtro pero el botón confirm queda disabled tras el click.

Fix: `await page.waitForTimeout(500)` después de que el modal sea visible, antes del filter. Guard adicional: `await btn.isEnabled().catch(() => false)` tras click → cancelar y probar siguiente item. Preferir `{ hasNotText: /regex/i }` sobre string literal (case-insensitive).
