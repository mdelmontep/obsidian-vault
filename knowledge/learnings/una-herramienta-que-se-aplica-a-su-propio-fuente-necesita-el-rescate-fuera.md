---
title: una herramienta que se aplica a su propio fuente necesita el rescate FUERA de ella
date: 2026-08-13
source: claude-code-session agh-iberica
tags: [tooling, arnes, recuperacion, diseno]
---
Al ampliar un arnés de mutación para que barriera también `scripts/`, empezó a mutarse **a sí mismo**
—que era el objetivo— y con eso apareció un modo de fallo que se muerde la cola:

> si muere con un mutante que **no parsea** escrito en su propio fuente, el arranque siguiente falla al
> transformar el fichero **antes de ejecutar una línea**. El diario que sabe restaurarlo está ahí, con
> el original intacto, y no se lee nunca **porque vive dentro del fichero roto**.

Medido, no supuesto: mutante inválido + diario preparado → `TransformError` y herramienta inservible.
Y el rescate manual obvio (`git checkout -- <fichero>`) lo **bloquea el `git-guard`** global, con razón:
no distingue un mutante abandonado de trabajo sin commitear.

**Regla general: el mecanismo de recuperación no puede vivir dentro de lo que puede romperse.** Vale
para cualquier herramienta que edite su propio código o su propia config — formateadores, codemods,
migradores de sí mismos, un hook que se reescribe. El rescate va en un **fichero aparte que no importa
NADA** del original (ni un tipo: un `import` lo transformaría también y caería por lo mismo que viene a
rescatar) y con su propia entrada en `package.json`.

**El precio y cómo pagarlo sin que se pudra:** duplicar el nombre/forma del diario. Su candado ata las
dos por **construcción**, no comparando constantes: el test **escribe** el diario con la función real
del arnés y lo **lee** con la del rescate. Si una de las dos cambia de forma, cae.

Y verifícalo en el camino real —brickear a propósito y rescatar—, no solo con el test.

Caso real: AGH #1124 → `npm run mutate:restore`. Ver
[[verificar-que-un-test-tiene-dientes-con-una-mutacion]].
