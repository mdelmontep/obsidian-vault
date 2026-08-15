---
title: create or replace de función: copiar de la versión vigente, no de la del issue
date: 2026-06-21
source: claude-code-session
tags: [supabase, migraciones, agentes]
---

Al reescribir una función SQL vía `CREATE OR REPLACE` en una migración nueva, partir del **cuerpo de la última migración que la define**, no de la que menciona el issue ni de memoria. Un agente reescribió 3 funciones `auto_mark_*` de conciliación (FacturaIA) partiendo de mig 155/266 e ignoró los fixes posteriores (278/279, cuadre de divisa `COALESCE(total_eur, total)`) → los revirtió en silencio; typecheck y tests pasaban igual (la regresión es semántica, no de tipos).

Fix:
- `grep -rln "FUNCTION public.<nombre>" supabase/migrations/` → tomar el número MÁS ALTO como base.
- `diff` verbatim base-vs-nueva → probar que solo añades lo tuyo, sin perder lógica.
- Vale doble cuando el cuerpo lo escribe un subagente: exígele el diff de evidencia y reverifícalo tú.

**Vuelto a pisar el 15-ago (TuCRMIA, `rgpd_redact`), y el atractor era un TERCERO que esta nota no
nombraba**: no partí «de memoria» ni «de la del issue», sino **de la migración donde la función NACE**,
que es donde uno la busca y donde está su cabecera explicativa. Una migración posterior la había
ampliado; el `create or replace` la sustituyó y **borró en silencio un paso de supresión de PII**.

Lo que lo cazó no fue ninguna lectura: fue una **aserción que EJECUTA** la función (`db:replay`) escrita
por la ampliación anterior. Corolario para el fix: la red de esta clase de regresión es una aserción
ejecutada, no un diff — el diff sólo funciona si te acuerdas de hacerlo, y el atractor de arriba es
justamente que no te acuerdas.

Ver [[postgres-rpc-firma-identica-create-replace]] · [[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]].
