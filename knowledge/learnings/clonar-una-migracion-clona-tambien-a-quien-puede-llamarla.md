---
title: clonar una migración clona también a quién puede llamar a su función
date: 2026-08-20
source: facturaia
tags: [supabase, seguridad, migraciones, rls]
---

Al clonar una migración probada (aquí `categoria_regla_upsert`, mig 372, para hacer
`ocr_regla_upsert`) se copia el bloque de permisos con ella. Y ese bloque **no es parte del
patrón: depende de quién la llame en el caso nuevo.**

La gemela concedía `EXECUTE` a `authenticated` porque la invoca una acción humana con sesión.
La nueva solo la llama un endpoint con `service_role`, así que ese `GRANT` sobraba — y siendo
`SECURITY DEFINER` y scopeada por el `p_org_id` que recibe, convertía la función en un IDOR:
Supabase publica lo concedido a `authenticated` en `POST /rest/v1/rpc/<fn>`, invocable con el
anon key que viaja en el bundle del navegador. Cualquiera con sesión podía escribir en la
organización de otro.

Regla: al clonar, el `GRANT` se **rederiva** de quién llama, nunca se copia. Y si la función
es `SECURITY DEFINER` y se scopea por un argumento, `authenticated` es sospechoso por defecto.

Lo cazó el hook `revoke-guard`, no una lectura del diff. Ver [[el-arnes-se-mide-a-si-mismo]].

**El espejo, 5-sep-2026 (facturaia, migs 846 → 849/850).** Arrastrar el `REVOKE` cierra lo que
otra migración abrió a propósito. La 846 reemitió `factura_rectificado_eur` copiando el par
`REVOKE/GRANT` de la 820 y deshizo la decisión razonada de la 826 sin nombrarla; el dashboard de
todos los clientes murió con `permission denied`. Y una `SECURITY INVOKER` ejecuta el cuerpo con
los permisos de QUIEN LLAMA, así que el permiso hace falta sobre la cadena entera: la puerta
figuraba abierta y aun así fallaba, porque el eslabón de nivel 2 (`reparto_por_pesos`) **nació
revocado**. Corolario: al clonar no basta rederivar el `GRANT` de la función que tocas — hay que
mirar a quién llama ella por dentro. Ver
[[una-consulta-que-devuelve-cero-filas-no-recorre-la-cadena-de-permisos]].
