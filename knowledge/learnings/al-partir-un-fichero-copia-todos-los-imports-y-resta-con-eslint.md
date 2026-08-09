---
title: al partir un fichero, copia TODOS los imports y resta con el JSON de eslint
date: 2026-08-09
source: claude-code-session
tags: [refactor, typescript, eslint, metodo]
---

Partir un fichero de 3.000 líneas en piezas exige resolver qué importa cada una. **Adivinar los que faltan no escala**: un generador que analizaba símbolos se dejó fuera `RejillaLinea`, `precioMaterialNetoUnit`, `totalLinea` y varios componentes hermanos, metió valores como `import type`, y hubo que abandonar el intento.

Al revés sí funciona, y es verificable: cada pieza nace con la **cabecera de imports COMPLETA** del original (aunque sobren 50) y luego se quitan los sobrantes con el informe JSON de ESLint, que sabe exactamente cuáles no se usan:

    npx eslint <dir> -f json  →  filtrar '@typescript-eslint/no-unused-vars'
                              →  quitar cada símbolo de su import
                              →  repetir hasta 0 (una pasada bastó: 496 quitados)

Dos trampas al cortar por rangos de línea:
- **Incluye el JSDoc entero** del bloque. Un `/**` sin cerrar se come la siguiente declaración y TypeScript miente: dice «no exporta X» teniendo el `export` delante.
- Un `perl -0pi` que reemplaza prefijos debe ir **de más largo a más corto**, o `.vot-org` se come el prefijo de `.vot-org-name` y deja `.org-name` a medias.

Verifica verbatim con `diff` contra `git show HEAD:<fichero>`, no a ojo — y ancla la comparación en la primera línea **con contenido**, o una línea vacía te da un falso «difiere».
