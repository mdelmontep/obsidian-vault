---
title: arnés de medición del agente de voz de Centro Elphis
date: 2026-08-29
source: centro-elphis
tags: [retell, voz, testing, harness]
---
Vive aquí porque Elphis **no tiene repo local**: si se queda en un scratchpad, la siguiente sesión
reconstruye el gate desde cero. El token de Retell NO está aquí — se lee de
`~/Projects/elphis-psicologia/infra/tests/.token-retell`.

## Orden de uso

1. `python3 crear.py 31 P2,P3c` — crea un borrador desde la base indicada, aplica los parches que no
   se salten, y **verifica contra el servidor**. Nunca publica. Aborta si producción se ha movido.
2. `python3 gate.py <candidato.json>` — **39** inviolables (transfer de crisis al 717, aviso de IA
   del art. 50, fórmula RGPD literal, tarifas, conjunto de nodos, tools, aristas, cifras del
   global_prompt). El veredicto es la PRIMERA línea; las líneas `pendiente - F4:` son informativas,
   no fallos. `exit 1` = no se toca nada.
   Los cambios estructurales a propósito se declaran en `declarado.json` (aristas nuevas/borradas y
   cifras); **lo que no esté ahí, bloquea**. Vaciarlo al empezar un candidato nuevo — pero dejar lo
   que siga sin estar en el snapshot base.
3. `python3 medir.py <etiqueta> <suite.json> <flow_id> [version]` — corre una suite y guarda el crudo.
4. `python3 contar.py` — los contadores sobre las transcripciones (guion literal, doble despedida,
   coste antes del consentimiento…). Agrupa por prefijo hasta el último guion: `cf-v46-final-r5` →
   `cf-v46-final`. **No preguntes al juez** para esto: mintió ("insiste en pedir el nombre" sobre una
   llamada donde nunca se pidió).
4b. `python3 tabla.py <rama-a> <rama-b>` — el veredicto del juez por caso, agregando rondas, para
   comparar dos candidatos. El campo es `status` y vale **`pass` / `fail` / `error`**, no
   `successful`: leerlo mal da 0/12 en las dos ramas y parece una catástrofe. Un `error` es fallo del
   arnés o del servicio, no del agente — va fuera del denominador, contado aparte como `(eN)`.
5. `python3 tf.py <borrador.json> [--neutro]` — pone el flow de TEST en el estado del borrador y
   verifica que el servidor guardó eso. Los `transfer_call` conservan el número REAL porque es lo que
   hay en producción; las suites son `simulation`, no marcan. `--neutro` apunta las tools a una URL
   muerta (para pruebas de chat, donde no hay `tool_mocks` y `crear_lead` pegaría a producción).
6. `./ROLLBACK.sh <version>` — baja el pin del trinquete y verifica **lo que SIRVE el DDI**, no lo
   que está publicado. Aborta si esa versión no está publicada en Retell.

## Publicar NO es desplegar

El DDI `+34910054950` lleva `inbound_agents[{agent_version: <entero>}]`, no `latest_published`
(el DDI de psicología sí usa `latest_published`; no se confundan). Así que `publish-agent-version`
por sí solo **no cambia lo que atiende el teléfono**, y el trinquete `guard-retell-pin`
(`FByKU2XI4woyEV8a`, T1 cada 5 min) repone el DDI al valor del pin si alguien lo mueve a mano.

Desplegar son tres pasos, en este orden:
1. Crear el borrador (`create-agent-version` con `base_version`) + `PATCH /update-conversation-flow`
   con el candidato + verificar contra el servidor + gate. **Ojo**: ese PATCH escribe
   `skippable: false` en TODOS los nodos, así que la verificación tiene que normalizarlo o da
   falso negativo.
2. `POST /publish-agent-version/{agente}` con **`{"version": N}` en el cuerpo**. Como query
   param devuelve `400 Unknown query parameter 'version'` (13-sep-2026). Y comprobar después
   que `max(v.version for v in get-agent-versions if v.is_published)` es N: un POST que no
   lanza excepción no demuestra que haya publicado.
3. **Subir el pin en Postgres** — sin esto no hay despliegue:
   `UPDATE idempotency_log SET response = jsonb_set(response,'{pin}','N'::jsonb), created_at = NOW()
   WHERE key = 'guard-retell-pin:config'` (base `elphis_app`, contenedor
   `elphis-n8nwithpostgres-wtqddl-postgres-aux-1`).

Rollback = el mismo paso 3 con la versión vieja. Ver [[elphis-guard-retell-pin]].

**13-sep-2026: `ROLLBACK.sh` llevaba meses mintiendo.** Republicaba una versión vieja y verificaba
la versión PUBLICADA — que sí cambiaba— así que imprimía «OK: sirviendo v21» con el DDI intacto en
la versión mala. Un rollback que reporta éxito sin hacer nada es peor que no tenerlo: en una
emergencia se da por resuelto. La comprobación que faltaba es `get-phone-number`, no
`get-agent-versions`.

## Reglas que costaron caro

- **El control de una medida es otro borrador, nunca la versión publicada.** El no-op idéntico a v29
  daba 64 %, la v29 publicada 83 %. → [[un-borrador-y-la-version-publicada-no-son-comparables-el-control-es-otro-borrador]]
- **`get-agent` sin `?version` devuelve el BORRADOR**, no lo servido. Lo servido es
  `max(v.version for v in get-agent-versions if v.is_published)`.
- **La suite tiene ±2 casos de ruido.** Ninguna decisión con una sola corrida.
- **Y el ruido no lo cancela alternar por rondas.** La deriva del servicio de Retell llega en bloques
  de ~8 min y cada medición dura ~4: una tanda intercalada reparte, no anula. El 12-sep atribuí a mis
  cambios de prompt 4/4 fallos que la bisección (6/6 pases en tres variantes) y una matriz 2×2 (12/12)
  demostraron que eran del servicio.
- **`medir.py` sella el sha256 del flow leído del servidor justo antes de crear el batch** (`flow_sha`
  en el fichero de la corrida). Dos corridas con el mismo sha midieron lo mismo; la etiqueta no prueba
  nada, se pone a mano.
- **Un gate que solo pasa no prueba nada.** Verificado por mutación: 6 mutantes reales, 6 mordidas.
  Ojo con los equivalentes: «cambiar el precio 60» no muerde porque «60» no aparece en el prompt.
  → [[un-mutante-que-no-muerde-puede-no-haber-mutado-nada]]

Estado y decisiones del agente en [[clientes/centro-elphis/index|el hub]].
