---
title: un campo de texto libre que viaja a la traza es un canal de egress, no un detalle de logging
date: 2026-07-30
source: claude-code-session agh-iberica
tags: [rgpd, observabilidad, typescript, arquitectura]
---
Una señal de telemetría tenía `reason?: string` y el pipeline lo reenviaba **verbatim** a la
traza — a doce líneas de un campo hermano (`errorClass`) que sí pasaba por un guard de
pertenencia. Al añadir una señal nueva, el valor natural para ese `reason` era el
identificador que **el LLM había generado desde el turno del usuario**: contenido de usuario
entrando en una traza cuyo tracing de contenido está deliberadamente apagado. Nadie lo
habría llamado «egress»; se habría llamado «poner el motivo en el log».

Regla: en un proyecto con política de datos, **todo campo que llega al backend de trazas es
un enum cerrado o es un canal de egress**. Y hacen falta los dos candados, porque cubren
cosas distintas:
- **el tipo** cierra los emisores: `reason?: MiEnum` derivado de `const REASONS = [...] as const`
  (`type R = (typeof REASONS)[number]`) → un motivo nuevo no compila si no se declara;
- **el guard en el borde** (`isReason(v): v is R`) cierra la entrada por bolsa sin tipar: un
  payload rehidratado, un fake, otro productor. Motivo fuera de taxonomía → se **omite** el
  campo y el `kind` sigue viajando: la métrica se cuenta, el texto no.

Olores de que estás ante esto: un campo `reason`/`detail`/`message` junto a otro que sí se
valida · un `string` libre en la firma de una señal «PII-free» · interpolar en el log algo
que salió del modelo o del usuario. Verificar el candado con un valor falso (→ error de tipo)
y con un valor de texto plausible (→ no aparece en la traza).
