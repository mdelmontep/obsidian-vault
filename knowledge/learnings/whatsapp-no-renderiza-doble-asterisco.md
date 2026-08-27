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

## Si el MISMO texto sale por varios canales, quita el énfasis (27-ago, Elphis Psicología)

Traducir `**024**` a `*024*` arregla WhatsApp y rompe los demás: el mismo guion se ve
también en el panel de Chatwoot y en un correo en texto plano, donde `*024*` es un
asterisco suelto a cada lado. **`024` a secas se lee igual de bien en los tres**, y no
depende de cómo convierta Markdown cada capa intermedia — algo que a veces no se puede
medir todavía. Sin adorno, el texto es correcto bajo todas las hipótesis.

Y si el texto está **aprobado por el cliente**, el arreglo no es en código: se emite la
versión siguiente del documento y se vuelve a pedir el OK. Juntar todos los defectos
conocidos en la misma versión — de uno en uno se pagan dos viajes por un carácter.
