---
title: kommo task types solo se crean desde la UI, no vía API
date: 2026-04-18
source: claude-code-session
tags: [kommo, api, tareas]
---

`POST /api/v4/tasks/types` devuelve 404 o 405 — la API de Kommo no permite crear tipos de tarea personalizados.

Para crear un tipo de tarea:
1. Ir a Kommo UI → Ajustes → Tareas → Tipos de tarea
2. Crear el tipo manualmente
3. Consultar el ID asignado con `GET /api/v4/account?with=task_types`

Los tipos por defecto son: 1=Follow-up (Seguimiento), 2=Meeting (Reunión). Los custom empiezan desde IDs altos (ej: 3968123 en gonzalo).
