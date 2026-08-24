---
title: un marcador de "dato no facilitado" acaba como dato de negocio si no muere en el borde
date: 2026-08-24
source: tecnocloud
tags: [agentes, voz, retell, crm, arquitectura]
---

Tool de LLM con campo obligatorio `string`: el modelo **siempre** rellena algo, así que cuando no
tiene el dato escribe el centinela que le diste (`No facilitado`). Ese literal es un dato válido para
el modelo y basura para la BD. En Tecnocloud viajó entero: `VoiceCallIn.profileName`, el `name` del
`Contact` auto-creado en el CRM (varios contactos distintos llamados igual) y el asunto del ticket
(«Llamada de No facilitado»). 6 de las 15 últimas llamadas.

- **El centinela muere en el borde**: normalizar a `null` antes de persistir nada, con la lista de
  marcadores comparada sin acentos, mayúsculas ni puntuación (`No facilitada`, `N/A`, `Desconocido`…).
- **El placeholder de display se DERIVA, no se guarda como identidad** (`Llamada +34…`).
- **El dato humano ya guardado gana al dictado**: el ASR deforma («Rufío» por «Rufino Vázquez
  Casamayor», «Mariajo» por «María José Ruiz»); promocionar solo si lo guardado es placeholder.
- **Una sola función pura compartida** por servicio y UI, o el asunto y la tarjeta divergen: el
  primer intento dejó un hueco de cadena vacía en el fallback de la UI.

Complementa [[normalizar-dato-dictado-en-la-frontera-del-write-no-en-el-canal]]: allí el dato llega
mal formado, aquí llega **ausente disfrazado de dato**.
