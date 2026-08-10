---
title: Aula
date: 2026-08-10
updated: 2026-08-11
tags: [proyecto, aprendizaje, nextjs, supabase, dokploy]
---

# Aula

Aula personal para aprender los sistemas propios (TuFacturaIA, TuCRMIA, AGH) y la terminología que
los rodea. **Las lecciones no existen hasta que se piden**: un runner de Claude las escribe abriendo
los repos de verdad, y cada afirmación va con su cita `fichero:línea`.

Repo `~/Projects/learn-agentesia` (git local, sin remoto). Next 16 + Supabase.
**Publicada** en `https://aula.185.99.186.76.sslip.io` · API en `aula-api.185.99.186.76.sslip.io`.

## Estado (11-ago)

- 🟢 **Publicada y funcionando** — Supabase autoalojado en `dokploymanu` (`/opt/aula/`), cuatro
  contenedores en vez de once. Contenido mudado con el dueño reescrito. HTTPS por `sslip.io`, sin
  tocar DNS. → [[supabase-selfhosted-cuatro-contenedores-y-seis-errores-enganosos]]
- 🟢 **Nivel reescrito: «desde la calle»** — las lecciones hablaban por encima. La causa no era el
  nivel sino el bloque «quién te lee» del prompt, que decía "sénior, eso NUNCA se explica".
  Ahora ninguna palabra técnica aparece antes de que se entienda la idea que nombra.
  → [[el-bloque-quien-te-lee-de-un-prompt-pisa-las-instrucciones-de-nivel]]
- 🟢 **«¿Esto qué es?»** — marcar texto en una lección y preguntarlo sin salir. Los términos del
  glosario salen subrayados y responden al instante; lo demás lo mira el runner en contexto y, si es
  vocabulario, entra en el glosario y de ahí al repaso.
- 🟠 **Contenido en curso** — 10 lecciones de 29 temas; el runner sigue encolando.
  Arranque: `npm run runner:remoto -- --vigilar` (trae la clave por SSH, no toca el disco del Mac).
- ⚪ **Sin correo**: no hay SMTP. El acceso es `npm run entrar:remoto`, enlace de un solo uso, y la
  sesión dura semanas. Conectar Resend está pendiente de decidir.

## Gates propios (los tres nacieron de un fallo real)

- `npm run enlaces` — recorre el sitio con sesión y falla si algo da 404, diciendo desde qué página.
  → [[dos-entidades-con-slug-propio-el-enlace-cruzado-no-lo-ve-ningun-test]]
- `npm run movil` — todas las pantallas en 393 px; falla si alguna no cabe.
  → [[overflow-wrap-anywhere-no-break-word-o-el-movil-encoge-el-texto]]
- `npm run gate` — lint + typecheck + tests + build, en el pre-commit.

## Trampas ya pisadas

- [[funcion-que-devuelve-tipo-compuesto-con-return-null-llega-como-fila-de-nulos]] — el runner
  petaba al vaciar la cola, que es lo que hace en modo vigilancia.
- [[filtrar-por-linea-un-volcado-con-valores-multilinea-borra-datos]] — la mudanza de contenido.
- [[redirigir-a-un-fichero-escribe-el-error-dentro-del-fichero]] — `gen:types` sin `DOCKER_HOST`.
- [[otra-sesion-con-pkill-mata-tu-servidor-y-parece-un-bug-del-producto]] — parar SIEMPRE por puerto.

El razonamiento largo de cada decisión (repaso espaciado, dominio, maestría que caduca, intercalado)
vive en `learn-agentesia/CLAUDE.md`, que es el sitio al que ir antes de tocar nada.
