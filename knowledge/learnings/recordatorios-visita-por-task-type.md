---
title: recordatorios de visita kommo deben filtrar por task_type, no por "cualquier tarea en 24h"
date: 2026-06-02
source: claude-code-session
tags: [kommo, n8n, recordatorios]
---
Workflow que escanea tareas Kommo y avisa 24h/4h antes: si dispara por "cualquier tarea
que venza", colisiona con tareas internas (matching, follow-ups del agente) → recordatorio
de cita FALSO al cliente.

Fix: anclar el aviso a una tarea **Meeting (task_type_id=2)** que el flujo de RESERVA crea
con `complete_till = hora de la visita`; el escáner filtra `task.task_type_id===2`; tareas
de otro tipo (el matching pasó su tarea a Follow-up=1) se ignoran. `complete_till` (timestamp
exacto) da la precisión 24h/4h que un CF de fecha de texto no da. La tarea lleva el lead
intrínseco y le aparece al agente en su lista — mejor que escanear un CF.

Kommo Simarro solo tiene 2 task types: 1 Follow-up, 2 Meeting. Blueprint compartido entre
clientes → revisar [[clinica-zen]] por el mismo bug. Ver [[simarro]] · [[routing-citas-por-agente]].
