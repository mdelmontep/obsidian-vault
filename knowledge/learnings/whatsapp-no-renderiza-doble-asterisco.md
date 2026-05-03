---
title: whatsapp no renderiza markdown estandar (** doble asterisco aparece literal)
date: 2026-05-03
source: claude-code-session
tags: [whatsapp, ai-agent, formato]
---

WhatsApp tiene su propio markdown reducido. `**double**` aparece literal con asteriscos. Sintaxis correcta:

- Negrita: `*texto*`
- Cursiva: `_texto_`
- Tachado: `~texto~`
- Mono: `` `texto` ``

## Fix en AI Agent que envía a WhatsApp

Regla explícita en system prompt:

> "NO uses markdown estándar (`**`, `__`). En WhatsApp solo `*negrita simple*` con un asterisco a cada lado."

Aplica también a templates HSM Kommo: si pegas un texto con `**` en el editor, se enviará literal.

## Síntoma

Cliente recibe `**Te confirmo la visita**` en vez de **Te confirmo la visita**.
