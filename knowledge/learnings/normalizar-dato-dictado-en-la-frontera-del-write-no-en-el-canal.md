---
title: normalizar datos dictados en la frontera del write, no en el canal
date: 2026-07-06
source: claude-code-session
tags: [agentes, voz, arquitectura, agh-iberica]
---

Agente multi-canal: un dato mal formado por ASR (teléfono dictado como palabras «seis uno
siete…», email con casing raro) puede llegar por VOZ **y** por texto → normalízalo en la
**frontera del dato/write**, no en el adaptador de canal. Un canal no debe conocer el formato
de negocio de cada campo.

Reglas que funcionaron (AGH #199):
- Un solo **chokepoint** antes de proponer/persistir (aquí `HitlBrain.propose`) cubre todas las
  rutas: write nuevo, re-propuesta de corrección, corrección a último cliente.
- **Idempotente**: si el valor ya viene en formato válido (trae dígitos), no lo toques → no rompes
  el input tecleado.
- **Estrecho para no dar falsos positivos**: actúa solo sobre el campo semántico (`phone`), no
  sobre texto libre; ante cualquier token no esperado, devuelve verbatim.
- Parser de números ES: combina palabras solo mientras la magnitud decrece (centenas→decenas→
  unidades) → cubre dígito-a-dígito y agrupado con la misma lógica. Acentos: [[regex-word-boundary-no-casa-acentos-js-normalizar-nfd]].
