---
title: cron health flapea si deduces "recuperado" de "ya no está en rojo" y pillas un run en vuelo
date: 2026-06-24
source: claude-code-session
tags: [monitoring, crons, alerting, tufacturaia]
---

Un sweep de salud que materializa/resuelve incidencias deduciendo "recuperado" de la
*ausencia* de rojo flapea cuando vigila un cron que falla en serie: si lo lee a mitad
de su siguiente intento (`status=running`, dura ~1s) y la función de salud devuelve
ámbar (no rojo) para un run en vuelo, el sweep lo toma por recuperado → resuelve la
incidencia → al siguiente tick la ve en `error` → la reabre → **un email por ciclo**.

Pista diagnóstica: las resoluciones caen siempre en horas redondas (:00/:30) — colisión
del tick del cron con el del sweep.

Fix de raíz: ante un run en vuelo, la salud la define el último run **terminado** (el
último veredicto real). `running` sobre `error` sigue rojo hasta que un run termine en
éxito; `running` sobre `success` o primer run = ámbar. Mantener cuelgue = running >
intervalo máx. Pedir ≥2 runs (un índice único in-flight garantiza ≤1 running).

"Recuperado" debe ser señal POSITIVA (un éxito), no la mera desaparición del rojo.
Relacionado: [[alert-collector-cron-vs-live-dedup-gap]].
