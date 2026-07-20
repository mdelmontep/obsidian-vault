---
title: copiloto multi-dominio: entidad con tabla propia necesita su tool de búsqueda + regla en el prompt (y fuzzy, no ilike)
date: 2026-07-20
source: claude-code-session
tags: [copiloto, llm, tool-routing, fuzzy, obras]
---

Smoke real destapó por qué el copiloto de obras "no encontraba" materiales que SÍ existían:

1. **Enrutado**: una entidad con tabla propia (`obras_materiales`) necesita su PROPIA tool de
   búsqueda (`buscarMaterialesObra`) + una regla explícita en el system prompt. Si no, el LLM cae
   en la tool de catálogo genérica (`buscarCatalogo` → `catalogo_servicios`), CIEGA a esa tabla, y
   responde "no existe / vacío" aunque exista. Añadir la tool sin tocar el prompt no basta: el LLM
   sigue entrando por la puerta equivocada. Hay que acotar también la descripción de la genérica.
2. **Fuzzy, no ilike**: el LLM pasa el nombre con ruido ("200 metros de cable flexible") o typos
   ("base suko"). Un `ilike '%frase%'` literal falla donde una RPC trigram / AND-de-palabras acierta.
   Reutiliza la infra fuzzy existente en los resolvers, no reinventes ni te quedes en ilike.
3. **Nunca auto-elegir** si mueve stock/coste: resolver devuelve unico/varios/ninguno; ante varios,
   listar y que elija el humano (botón de confirmación destructive).

Señal: el bot responde inconsistente ("ambiguo" una vez, "vacío" la siguiente) para el mismo término
existente → el LLM está razonando por su cuenta, no llamando al resolver. Relacionado:
[[resolver-ambiguo-escape-hatch-duplicados-exactos-vs-fuzzy]] · [[copiloto-tool-select-campo-faltante-guard-mudo]].
