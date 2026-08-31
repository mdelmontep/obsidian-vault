---
title: un gate que compara contra el `origin/main` de otro repositorio cambia de veredicto solo
date: 2026-08-31
source: tucrmia
tags: [gates, git, monorepo]
---
`sync:shared:check` —la capa compartida entre tucrmia y facturaia— salió verde en la corrida manual
del gate y ROJO en el pre-commit veinte minutos después, sin que yo tocara un fichero. No era un
flake: el `origin/main` de facturaia había avanzado en medio, con un PR que tocaba `tokens.css`.

La lección no es «refresca antes». Es que **un gate cuyo veredicto depende de una referencia móvil
ajena no es reproducible**, y su rojo no se puede leer como «has roto algo». Lo que lo convierte en
medida es fijarlo a un COMMIT y que cada divergencia aceptada cite ese commit; si no, `--accept`
puede sellar un estado que no existe en ningún historial.

Corolario operativo: verde hace veinte minutos no es verde ahora.
Ver [[bloque-generado-para-gate-byte-a-byte-nunca-se-transcribe-de-memoria]].
