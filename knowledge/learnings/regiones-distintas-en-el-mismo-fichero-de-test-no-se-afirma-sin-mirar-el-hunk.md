---
title: «tocan el mismo fichero pero en regiones distintas» no se afirma sin mirar el hunk
date: 2026-07-30
source: claude-code-session agh-iberica
tags: [git, colaboracion, metodo]
---
Dije dos veces —con confianza y sin mirar el hunk— que dos PRs mías «tocan los mismos dos
ficheros en regiones distintas, deberían combinar solas». No combinaron: al mergear la
primera, la segunda quedó CONFLICTING porque los **tests nuevos de ambas caían en el mismo
punto de inserción**, el final del `describe`. Quien mergea planificó con mi frase y acabó
resolviendo a mano y aterrizando por fast-forward.

Un fichero de test no es un lienzo con regiones: es un **imán de inserción**, casi todo lo
nuevo entra por el final del bloque. Así que «ficheros distintos → sin conflicto» no se
traslada a «regiones distintas del mismo fichero de test → sin conflicto».

- Antes de afirmarlo: `git diff <base>...<rama>` de las dos y mirar el punto de inserción
  real. Si son tests del mismo fichero, asumir que **sí** conflictúan.
- Si no lo has mirado, di «no lo sé». Es más útil que una predicción que se cumple a medias.

**Corolario del mismo día:** un commit empujado a una PR **ya mergeada** no existe — quedó
huérfano y su contenido fuera de `main`, sin error visible. Antes de añadir a una PR en cola
de merge: `git fetch` y comprobar que sigue abierta; ventana estrecha → rama nueva. Lo que
lo hizo recuperable: escribir el snapshot **por líneas** y la nota en **fichero nuevo**, así
re-aplicar sobre el `main` nuevo fue un cherry-pick limpio (y hubo que hacerlo dos veces).
