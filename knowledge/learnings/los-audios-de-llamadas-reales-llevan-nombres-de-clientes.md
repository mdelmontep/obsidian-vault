---
title: los audios de llamadas reales llevan nombres de clientes
date: 2026-08-01
source: claude-code-session
tags: [rgpd, audio, marketing]
---
Publicar grabaciones reales de un agente de voz como demo en la web parece inofensivo
—suena mucho mejor que un actor— hasta que se transcribe el fragmento: el guion del
agente **pide el nombre completo en el segundo turno**, así que casi cualquier corte de
30 s contiene nombre y apellidos de un cliente de terceros.

Caso real: «Julián Fernández» a los 17 s y «José Emilio Blanco» a los 27 s, ya
commiteados en `main` y a un deploy de estar públicos.

Reglas antes de subir audio de llamadas:
- Transcribir el corte exacto, no la llamada: el problema aparece donde recortas.
- Preferir llamadas cuyo interlocutor sea del propio equipo.
- Si no, cortar antes de la identificación (el fragmento se entiende igual: el problema
  se cuenta antes que el nombre).
