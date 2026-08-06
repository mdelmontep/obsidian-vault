---
title: "«Closes #N (3 de 4)» cierra el issue entero: la keyword no admite matices"
date: 2026-08-07
source: claude-code-session
tags: [github, proceso, issues]
---
Escribí en un commit `Closes #1007 (3 de 4)` para una PR que resolvía tres de las cuatro partes y que
**declaraba en su cuerpo que no cerraba el issue**. GitHub **no lee el paréntesis**: ve la keyword y
cierra. El issue quedó cerrado con la parte que exigía una decisión de diseño y una migración fuera
de toda cola.

Es el **reverso** del gotcha conocido (`Cierra #N` en español no cierra nada), y el reverso es peor:
un issue que sigue abierto **se ve** al repasar el backlog; uno cerrado de más **desaparece**, y lo
que quedaba vivo solo sobrevive si alguien recuerda que existía.

**Regla:** si una PR no cierra el issue **entero**, no lleva keyword. Ni con paréntesis, ni con
«parcial», ni con «mitad». Se enlaza sin keyword (`Parte de #N`) y se cierra a mano cuando de verdad
esté cerrado.

**Verificación:** al terminar una tanda, `gh issue view N --json state` sobre **todos** los issues
tocados, no solo sobre los que esperabas cerrar. El fallo se detecta en 5 segundos y solo si se mira.
