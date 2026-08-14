---
title: una corrección de tipos sobre un parser que recibe unknown es inerte — múta la para saberlo
date: 2026-08-14
source: claude-code-session
tags: [typescript, tipos, verificacion, supabase]
---

Los tipos generados de la BD mentían sobre la nulabilidad de tres columnas, así que se escribió el
típico override (`Omit<...> & { col: string | null }`) sobre el tipo del cliente. **Compilaba, se
leía como una protección y no protegía nada**: el consumidor era un parser *parse-don't-validate*
que recibe `unknown` y decide fila a fila, así que **nadie consumía el tipo generado en ese camino**.

Cómo se supo, y es la única forma: **mutarla**. Quitar una columna de la corrección y volver a
correr `typecheck`. Si sigue verde, el override no muerde y sobra.

Regla general: un tipo que compila no es un tipo que protege. Antes de dar por buena cualquier
corrección de tipos —override, `satisfies`, branded type— romperla a propósito y comprobar que sale
en rojo. Es el mismo criterio que ya se aplica a los guards (verlos en ROJO antes de creerlos), y la
misma familia de fallo que un limitador de tasa construido y desenchufado: escrito no es enchufado.
