---
title: en no-restricted-imports la negación no re-incluye si el directorio padre quedó excluido
date: 2026-08-02
source: claude-code-session
tags: [eslint, typescript, arquitectura, gates]
---
Los `group` de `no-restricted-imports` son **gitignore-style**, y ahí rige la regla de gitignore:
*no se puede re-incluir un hijo si su directorio padre está excluido*. Una allowlist escrita a lo
intuitivo se ignora **en silencio** y la regla bloquea imports legítimos.

```js
group: ['@/lib/**', '!@/lib/ui/**']        // ❌ la negación no aplica
group: ['@/lib/**', '!@/lib/ui', '!@/lib/ui/**']  // ✅ padre ANTES que contenido
```

Caso TuFacturaIA (frontera de `components/ui/`): 37 falsos positivos hasta añadir el `!` del
directorio. Los ficheros sueltos de un nivel (`!@/lib/numbers`) sí funcionaban, lo que despista más
todavía: parecía que la sintaxis era correcta.

Regla: al escribir una allowlist con negaciones, **probar los dos signos** — que lo prohibido dé
rojo y que lo permitido no. Ver [[un-guard-que-grepea-el-texto-del-fichero-no-distingue-uso-de-asercion]].
