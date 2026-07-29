---
title: una orden imposible en su entorno no hace que el agente diga "no puedo", explora hasta que lo matan
date: 2026-07-29
source: claude-code-session
tags: [claude-code, agentes, prompt, runner, facturaia]
---

El runner de tickets moría por timeout a los 30 min. La causa no era "el prompt poco exigente"
sino dos órdenes irrealizables en ese contenedor: dejar una captura de pantalla en una imagen
**sin navegador** (Dockerfile: git, gh, psql, curl) y `npm run build`, que muere por OOM contra
los 3G. Un humano contesta "aquí no se puede"; un agente persigue la orden (instalar Playwright,
reintentar el build) hasta que lo mata el reloj.

Peor: **la misma instrucción vivía en dos capas y divergieron**. El prompt del ticket exigía el
build; el `--append-system-prompt` lo prohibía y a la vez abría con "sigue el prompt al pie de la
letra". Resolver esa contradicción también cuesta turnos.

Regla: **cada instrucción en una sola capa**. Calidad del código → `CLAUDE.md` del repo (el agente
lo carga solo). Límites del entorno → system prompt del runner (el texto del ticket no lo puede
contradecir). El encargo → el prompt de la tarea. Y antes de pedir algo, comprueba que su entorno
puede hacerlo: `docker` sin navegador no hace capturas por mucho que se lo pidas.

Ver [[mide-el-reparto-de-fallos-antes-de-arreglar-el-que-te-cuentan]] · [[actions-sin-billing-hooks-locales-unico-gate]]
