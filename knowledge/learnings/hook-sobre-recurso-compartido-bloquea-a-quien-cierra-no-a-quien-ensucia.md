---
title: un guard sobre un recurso COMPARTIDO castiga a quien cierra, no a quien ensucia
date: 2026-08-09
source: claude-code-session
tags: [hooks, claude-code, harness, metodo, sesiones-paralelas]
---
Stop hook que bloqueaba si `~/.claude` quedaba sin commitear. Con varias sesiones abiertas —lo
normal— `~/.claude` es GLOBAL: la que va a cerrar se come el bloqueo por lo que está editando
OTRA. Me pasó el mismo día que lo escribí, y el único camino que dejaba era su propio aviso «si no
es tuyo, dilo y sigue»: un bloqueo que se resuelve ignorándolo se aprende a ignorar siempre.

Patrón: un guard sobre estado compartido necesita **atribución**, no solo detección. La pregunta no
es «¿está sucio?» sino «¿lo ensucié YO en este turno?».

Atribución que funcionó: el `transcript_path` del input del hook es la única evidencia que liga un
cambio a esta sesión. Es mío si esta sesión lo escribió (tools de escritura, o Bash con la ruta en
POSICIÓN de escritura) y nadie lo tocó después: `mtime <= mi última escritura + tolerancia`. La
tolerancia se MIDE (aquí: míos +4…+23 s, ajenos +342…+558 s → 60 s), no se supone.

Y elegir la dirección del fallo: sin transcript, fallar CERRADO (todo mío); lo que no toqué nunca,
solo AVISA. Ver [[un-control-negativo-que-no-discrimina-invalida-el-test-entero]] y
[[script-por-heredoc-y-datos-por-stdin-se-pisan]].
