---
title: un token de concurrencia que lee el servidor no protege la pantalla vieja
date: 2026-09-28
source: facturaia
tags: [concurrencia, api, documentacion, obras]
---
**Qué pasa:** la ruta hace un PATCH parcial con este patrón: lee la fila, fusiona el patch y pasa a la RPC `expectedUpdatedAt: fila.updated_at`. Así el conflicto optimista (OB112, mig 967) solo cubre los milisegundos entre esa lectura y el `FOR UPDATE`. Si hay dos pestañas abiertas, gana la última que guarda y nadie ve el aviso.

**El riesgo:** el test, el toast y el código de error existen, así que todo parece protección de pantalla vieja. Los dos manuales llegaron a prometerla al cliente; lo cazó el gate de cierre de #3046 y se corrigió en #3049.

**Regla:** para saber qué cubre un token optimista, mira **quién lo lee**.
- Si lo lee el servidor, solo protege la fusión *read-merge-write*.
- Si lo lee el cliente (el `updated_at` viaja en el body desde lo que se pintó), protege la pantalla. En ese caso hay que refrescarlo tras cada guardado, o el usuario choca consigo mismo.

Documenta el que tienes, no el que suena.
