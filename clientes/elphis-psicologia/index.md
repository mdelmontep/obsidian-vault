---
title: Elphis Psicología — HUB
date: 2026-08-24
updated: 2026-08-31
source: elphis-psicologia
tags: [cliente, agentesia, elphis-psicologia, voz, whatsapp, retell, n8n, dokploy, rgpd, agency-portal]
---

# Elphis Psicología · HUB

División de psicoterapia del grupo Elphis (O'Donnell 32, Madrid). **Proyecto DISTINTO de
[[clientes/centro-elphis/index|Centro Elphis]] (adicciones)**: no comparten CRM, agenda,
workflows ni número — solo host Dokploy y dirección. Repo `AgentesIA-MAdrid/elphis-psicologia`
(local `~/Projects/elphis-psicologia`; **arrancar las sesiones desde ahí**, no desde
`~/Projects/elphis` — la atribución de horas y las memorias van por cwd de arranque).
Bloque A (web, marca) = Borja · **Bloque B (agentes) = Manu**. Autoridad documental:
`docs/bloqueantes.md` > `docs/protocolo-crisis.md` > `PRODUCT.md` > spec de julio.

## Estado · 2026-08-31

**El bloque B ya no tiene ninguna pieza a medias.** Todo lo que sigue está vivo en
`n8n-psicologia.elphis.agentesialabs.com` o en Retell, y **cada pieza tiene un
guardián `verify:*-desplegado` que se ha visto rojo mutando el objeto vivo** —no una
copia: el guardián existe porque estas cosas se editan desde un panel con un clic.

- ✅ **Infra** — n8n 2.36.5 + postgres + postgres-aux + redis en Dokploy compartido.
  Esquema cerrado a propósito (3 tablas, sin texto libre: todo es dato art. 9).
  Detalle en `infra/README-deploy.md`. **Migración 02 aplicada el 27/08**: `CHECK`
  en `crm_events.service_slug`, y probada por los dos lados →
  [[la-fila-de-prueba-que-viola-otra-restriccion-finge-que-la-nueva-muerde]]
- ✅ **Agenda (GCal)** — `psico-agenda-*`: check/book/cancel/reschedule + runner.
  L-V 10-21, 50 min / 60 pareja, 24 h de antelación, `service_slug` cerrado.
  Idempotencia doble (Redis INCR/TTL + `bookingKey` releído). Si GCal no responde →
  error honesto, nunca inventa huecos. `infra/README-agenda.md`. →
  [[un-consumidor-del-shape-puede-vivir-fuera-del-repo]] ·
  [[nodo-gcal-de-n8n-no-soporta-extendedproperties]] ·
  [[lock-e-idempotencia-en-n8n-con-redis-incr-sin-set-nx]] ·
  [[parse-roto-de-una-respuesta-200-se-confunde-con-fallo-y-duplica]]
- ✅ **Base de conocimiento** — `infra/kb/conocimiento.md`, generada entera desde
  `web/src/lib/`. `verify:kb` cierra el hueco de que sea la única copia del dato de
  la web que vive fuera de la web. Siete de sus once tests comprueban **ausencias**
  (sábado, «Adicciones», colegiado): una web que no menciona algo no afirma nada,
  un agente al que se lo preguntan está a una inferencia de decir que sí.
- ✅ **Circuito de crisis** — `psico-crisis-{aviso,enviar,reintento}`, ejercido de
  punta a punta con correos y filas de verdad. Aviso por correo sin contenido
  clínico. Entradas: WhatsApp por el cerebro, voz por `psico-voz-crisis`.
- ✅ **Voz (Retell)** — `retell-llm` de prompt único (NO conversation flow),
  gpt-5.1 a 0,2, **v17 servida**. Prompt compuesto desde la KB y el protocolo, nunca
  retranscrito. Sin herramienta de transferencia: prohibirlo en el prompt con la
  herramienta puesta es una prohibición desobedecible. La **voz es dato del repo**
  (`config-voz.mjs`) porque el «suena robótico» vivía solo en el panel.
  **28/08**: entran los hallazgos de conversación medidos en Adicciones —las frases
  entrecomilladas no son un guion, se usa la palabra de la persona, y se acusa lo
  dicho antes de pedir el siguiente dato *sin repreguntar*, que aquí sería recoger
  dato del art. 9 por teléfono. Van **sin medición**: este LLM no tiene suite
  (`list-batch-tests` = `[]`) y los porcentajes de allí no son transferibles. →
  [[un-hallazgo-medido-en-otro-agente-viaja-el-mecanismo-nunca-el-porcentaje]]
  De paso salió el defecto que ninguno de los dos guardianes veía: el prompt mandaba
  colgar con `end_call` (el `type`) y la herramienta se llama `colgar` (el `name`), y
  el test fijaba «dos herramientas» habiendo tres. Guardián nuevo en
  `verify:voz-desplegado`, 2 mutaciones y 2 víctimas sobre el agente vivo
  (`infra/tests/rojo-voz-herramientas.py`). →
  [[un-repo-coherente-consigo-mismo-no-prueba-el-nombre-que-vive-fuera]]
- ✅ **WhatsApp** — `psico-whatsapp-cerebro` vivo y con conversaciones reales
  (Chatwoot en el bucle, Basic Auth: Chatwoot **no firma** en la 4.0.3, medido).
  Prompt y las tres plantillas de Meta generados desde `site.ts`.
- ✅ **Avisador global** — `psico-error-handler-global`, la única alarma. Su
  guardián comprueba que **todos** los workflows activos lo llevan puesto:
  `errorWorkflow` vive en los settings de cada uno y **uno nuevo nace sin avisador**
  (cazó a `psico-voz-crisis` en su primera corrida).
- ✅ **Purga de retención (27/08)** — hacía verdad una frase publicada («30 días con
  borrado automático») borrando de **dos tablas que nadie escribe**, y su
  comprobación contaba filas en esas mismas tablas vacías: verde exista o no la
  purga. La memoria real vive en **Chatwoot**, que no tiene DELETE de conversación
  en la 4.0.3 → se borra el **contacto**, que arrastra las suyas (probado con dato
  sintético). Guardián verde por 8 lados, **10 mutaciones con víctima**, y el arnés
  guardado en `infra/tests/rojo-purga.py`.
- ✅ **Protocolo de crisis v2 (27/08)** — dos erratas de negrita y la escalada de A a
  B, en un solo viaje a la clienta. Redesplegado en las cinco superficies vivas. →
  [[comparar-por-tamano-no-ve-un-artefacto-servido-desde-otra-version]] ·
  [[whatsapp-no-renderiza-doble-asterisco]]
- ⏳ **OAuth Google sin token** — `agenda-e2e.sh` 1/12, el resto cascada del mismo
  fallo (`Unable to sign without access token`). El «Connect my account» del 24/08 no
  cuajó: revisar si el popup se cerró antes o si el client sigue en Testing.
- ⚠️ **PR #30 sigue ABIERTO**, y el trabajo del bloque B **no está en él**: vive en
  `main` local y en el fork. 42 commits locales sin subir a `origin/main` y **16 de
  Borja sin traer** — o sea que este repo local también está *atrasado*, no solo
  adelantado. Antes de afirmar qué dice un fichero: `git log HEAD..origin/main`.
- ⚠️ **`~/Projects/elphis` (carpeta suelta, sin `.git`) sigue viva** y ya atribuyó
  cuatro bloques de trabajo de esta división a `project=elphis` (reatribuidos a mano
  el 24/08). Renombrarla lo cierra de raíz; avisarlo en prosa no.
- 🔴 **Sin copias de seguridad fuera del host** — Wasabi da 403 en TODO el host desde
  hace ≥11 días (afecta también a Adicciones y Chatwoot). Escalado a Borja/Manu.
- 🔴 **Token de Chatwoot sin rotar, y es admin de las DOS cuentas.** Al rotarlo hay
  que actualizar **las dos credenciales a la vez** (`kjk4WH7UDRLfvxXM` aquí,
  `Ayjjj1XUjzCiBEtV` en Adicciones): cambiar una sola deja mudo al otro proyecto.
  El arreglo de fondo es un bot propio limitado a la cuenta 4.

## La puerta que lo cierra todo

**Nada del bloque B se enciende hasta que Alba dé el OK por escrito a la v2 del
protocolo de crisis.** Dio el OK *de palabra* a la v1 el 21/08 y nunca el escrito. El
mensaje listo para que lo mande Borja está en `docs/peticion-firma-alba.md`, e
incluye las otras cuatro preguntas abiertas del §7 para gastar un solo viaje.
`verify:voz-desplegado` comprueba hoy que **ningún número apunta al agente**, y esa
comprobación es parte de la puerta.

## Bloqueos (terceros)

- **Alba**: la firma de la v2 · nº de colegiado (sin él el blog no publica:
  `articleSchema` lanza) · nº de registro sanitario · quién es la asesoría/DPO ·
  horario de sábado · si el protocolo vale igual para Adicciones.
- **Borja**: merge del PR #30 · `PUBLIC_FORM_ENDPOINT` · DPA · Wasabi · móvil real
  de avisos (el 659 877 708 NO vale: emisor de la WABA de Adicciones).
- **Manu**: rotar el token de Chatwoot (las dos credenciales) · backups fuera del
  host · las 4 confirmaciones de la WABA (número virgen · SIP · OTP · SMTP) ·
  password del ítem 1P · el Connect de OAuth · una llamada real que mida el retardo
  de `call_analyzed` y el experimento de `basic_attributes_only`.
