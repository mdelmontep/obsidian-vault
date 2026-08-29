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
2. `python3 gate.py snapshots/<flow>.json` — 44 inviolables (transfer de crisis al 717, aviso de IA
   del art. 50, fórmula RGPD literal, tarifas, conjunto de nodos, temperatura). `exit 1` = no se toca nada.
3. `python3 medir.py <etiqueta> <suite.json> <flow_id> [version]` — corre una suite y guarda el crudo.
4. `python3 contar.py` — los contadores sobre las transcripciones. **No preguntes al juez**: mintió
   ("insiste en pedir el nombre" sobre una llamada donde nunca se pidió).
5. `python3 tf.py P1,P4,P5,P6` — pone el flow de TEST en un estado. Su `crisis_transfer` se queda
   SIEMPRE en `+34600000000`: una suite de crisis con el número real llama al Teléfono de la Esperanza.
6. `./ROLLBACK.sh 29` — vuelve a una versión anterior y verifica sola qué queda sirviendo.

## Reglas que costaron caro

- **El control de una medida es otro borrador, nunca la versión publicada.** El no-op idéntico a v29
  daba 64 %, la v29 publicada 83 %. → [[un-borrador-y-la-version-publicada-no-son-comparables-el-control-es-otro-borrador]]
- **`get-agent` sin `?version` devuelve el BORRADOR**, no lo servido. Lo servido es
  `max(v.version for v in get-agent-versions if v.is_published)`.
- **La suite tiene ±2 casos de ruido.** Ninguna decisión con una sola corrida.
- **Un gate que solo pasa no prueba nada.** Verificado por mutación: 6 mutantes reales, 6 mordidas.
  Ojo con los equivalentes: «cambiar el precio 60» no muerde porque «60» no aparece en el prompt.

Estado y decisiones del agente en [[clientes/centro-elphis/index|el hub]].
