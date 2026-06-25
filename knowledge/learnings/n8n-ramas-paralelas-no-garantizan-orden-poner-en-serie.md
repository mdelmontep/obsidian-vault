---
title: n8n ramas paralelas no garantizan orden de ejecución, poner en serie
date: 2026-06-25
source: claude-code-session
tags: [n8n, workflow, expresiones, bug]
---

n8n NO garantiza el orden de ejecución entre ramas hermanas (dos nodos que cuelgan del mismo ancestro en paralelo). Si un nodo B referencia `$('A')` por expresión y A cuelga en paralelo de un ancestro común (no aguas arriba de B en serie), B puede ejecutarse ANTES que A → `ExpressionError: Node 'A' hasn't been executed` → el nodo peta y se corta toda la cadena posterior.

**Fix correcto cuando A SIEMPRE debe ejecutarse** (no es opcional): ponerlo **en serie aguas arriba de B**, no en paralelo. NO usar `$if($('A').isExecuted, ...)` — eso solo silencia el error y deja el dato vacío (fallback).

`$if(isExecuted)` es solo para ramas condicionales o dos triggers que convergen, donde A legítimamente puede no correr. Ver [[n8n-expresion-nodo-no-ejecutado-falla-silencioso]] y [[n8n-nodos-compartidos-entre-ramas-requieren-if-isExecuted]].

**Caso real**: Simarro reserva (`iMoTKZWxYLymGuHF`) — `Get dirección Retell` colgaba en paralelo de `Preparar Datos Retell`; `Create Calendar Retell` lo referenciaba y corría antes → no creaba evento/tarea/email. Fix: `IF ocupado → Get dirección → Create Calendar`.
