---
title: un repo puede tener un test que valide la PROSA del CLAUDE.md
date: 2026-08-20
source: agh-iberica
tags: [claude-code, gates, documentacion, agh-iberica]
---

Al reescribir el `CLAUDE.md` de AGH el gate salió rojo por `test/pg-autoskip-claim.test.ts`: exige la **formulación literal** «NO se autosaltan «sin DB»» *dentro* del fichero, porque esa afirmación falsa ya había vuelto al repo cinco veces. Resumir con otras palabras —diciendo lo mismo— lo rompe.

El detector tiene además un caso que lo hace usable: **no caza a quien ya lo dice bien**, porque la formulación correcta contiene la incorrecta citada dentro.

Antes de tocar el `CLAUDE.md` de cualquier repo: `grep -rl "CLAUDE\.md" --include='*.ts' --include='*.mjs' --include='*.sh'` y mirar cuáles hacen `readFileSync` de él. En AGH lo hay; en facturaia y panel-tecnocloud se comprobó y no.

**Un candado sobre la prosa es tan real como uno sobre el código**, y no se descubre leyendo el `CLAUDE.md` — solo corriendo el gate o buscándolo a propósito. Corolario para escribir gates: si una frase concreta importa, se puede fijar con un test; y si se fija, hay que decirlo en la propia frase para que quien la reescriba sepa por qué no puede.

Ver [[claude-code-project-rules-no-se-comparten-si-claude-gitignored]]
