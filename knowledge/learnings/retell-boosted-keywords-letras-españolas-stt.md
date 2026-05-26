---
title: Retell boosted_keywords con letras españolas mejora STT de matrículas
date: 2026-05-25
source: claude-code-session
tags: [retell, stt, spanish, accessibility]
---

Sin `boosted_keywords`, el STT de Retell (sea ElevenLabs Scribe o el motor por defecto) confunde habitualmente: "zeta" → "seta/zelda", "efe" → "f/efe/e", "hache" → "ace/h", "uve" → "u/uve doble". Esto rompe la captura de matrículas y deletreo de emails.

Fix: añadir al agent el array `boosted_keywords` con las letras escritas tal cual se pronuncian en castellano:

```json
[
  "a","be","ce","de","efe","ge","hache","i","jota","ka","ele","eme",
  "ene","eñe","o","pe","cu","erre","ese","te","u","uve","doble uve",
  "equis","i griega","zeta",
  "cero","uno","dos","tres","cuatro","cinco","seis","siete","ocho","nueve",
  "matrícula","peritaje","Mapfre","Mutua","AXA","Allianz","Cesvimap"
]
```

También añadir términos del dominio (compañías de seguros, marcas de coche, palabras técnicas) y nombres propios del agente/empresa.

Caso real: EcoBox 2026-05-25 — "tres dos cinco cero zeta efe" entendido como "tres dos cinco cero seta f" antes; tras boost, parsea limpio.
