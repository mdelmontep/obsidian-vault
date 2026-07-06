---
title: retell/voz — deletrear con nombre de letra (uve, o, zeta), no letras peladas
date: 2026-07-07
source: claude-code-session
tags: [retell, voz, tts, español]
---
Al deletrear un dato crítico en voz para que el usuario OIGA errores de ASR, mandar las LETRAS PELADAS («V, O, Z») falla: el TTS las agrupa y las pronuncia como palabra, y en español b/v son homófonas → «voz» deletreado «V-O-Z» suena «be, boz» y el usuario «corrige» algo que ya estaba bien. El propio deletreo (que existe para que los errores se oigan) fabrica el malentendido.

Fix: deletrear con el NOMBRE de la letra en es-ES: «voz» → «uve, o, zeta»; «test» → «te, e, ese, te». Mantener el pacing (una coma/pausa entre letras). Es copy de voz en código (función `spellOut`), no `pronunciation_dictionary` del agente.

Caso real AGH (#248/#249): «es voz con v» — el agente aplicó la corrección a la palabra equivocada porque el deletreo homófono le hizo creer que había error.
Ver [[retell-boosted-keywords-letras-españolas-stt]].
