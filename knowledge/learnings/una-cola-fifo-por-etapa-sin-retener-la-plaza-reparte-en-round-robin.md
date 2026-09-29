---
title: una cola fifo por etapa sin retener la plaza reparte en round-robin y nadie termina
date: 2026-09-29
source: facturaia (arnés fia-gate, ~/.claude/gate)
tags: [semaforo, gate, colas, concurrencia]
---
Un trabajo de N etapas que pide plaza en cada etapa y vuelve al final de la cola hace que K trabajos se turnen etapa a etapa: todos acaban a la vez, al final. En facturaia, con cinco gates encolados, no hubo ni un merge en todo el día.

- **Arreglo parcial (b2e785e, `FIA_GATE_SEQ_FILE`):** heredar el número de la primera etapa solo sirve mientras el tique está en la cola. En el hueco entre dos etapas `mem` (una etapa `directo` o `cpu`) otro gate se lleva la plaza. La auditoría del mismo día reprodujo A→B→A→B.
- **El test lo pasaba** porque encolaba la etapa 2 sin hueco. Un test de turno tiene que dejar un hueco sin tique entre etapas.
- **Arreglo real:** retener la plaza (o una reserva con dueño) durante todo el trabajo, no solo la posición en la cola.

Hermano: [[una-clave-de-cache-calculada-antes-de-la-cola-caduca-durante-la-espera]] · [[fia-gate]]
