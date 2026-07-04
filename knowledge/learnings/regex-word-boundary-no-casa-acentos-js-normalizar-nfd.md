---
title: en JS \b no casa junto a acentos — normaliza NFD antes de matchear comandos
date: 2026-07-02
source: claude-code-session
tags: [javascript, regex, i18n]
---

Matchear comandos/intención en español con `/\b(sí|no|ya está)\b/i` falla silenciosamente: en JS el `\b` es ASCII, así que las letras acentuadas (í, á, é) NO son word-chars → no hay boundary junto a ellas y "sí"/"ya está" no matchean. Bug sutil: pasa con tests en minúscula-sin-acento y muerde en producción con acentos reales.

Fix: normaliza antes de testear —
`text.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"")` → "sí"→"si", "ya está"→"ya esta"— y define los matchers en ASCII.

Ojo aparte (colisión comando vs dato): para comandos que compiten con texto libre dictado (fin de flujo "ya está" vs un cliente "Grupo Fin"), NO uses `contains`; exige **match exacto** del mensaje normalizado contra un set de comandos.

Caso real (#86, 2026-07-04): reapareció en el MISMO módulo — un matcher (`STOPWORD_FIRST`) seguía aplicándose al texto crudo, así que "sí, confirmo" escapaba el guard y rompía la siembra-por-voz. Lección: normaliza en TODOS los matchers con `\b`, no solo en algunos; es fácil arreglar uno y dejar otro.
