---
title: zod .uuid() exige los nibbles del rfc 4122 y postgres no — los ids de fixture revientan la api
date: 2026-07-28
source: claude-code-session
tags: [zod, postgres, e2e, fixtures, supabase]
---

Postgres acepta como `uuid` **cualquier** grupo de 32 dígitos hex. Zod NO: `z.string().uuid()`
valida el RFC 4122, o sea versión (13º nibble ∈ 1-8) y variante (17º ∈ 8/9/a/b).

Consecuencia: los ids "legibles" de fixture se guardan sin queja y la API los rechaza.

```
e2e00001-0000-0000-0000-000000000001 → Postgres OK · Zod false   (versión 0, variante 0)
e2e00001-0000-4000-8000-000000000001 → Postgres OK · Zod true    (versión 4, variante 8)
```

Síntoma real (FacturaIA, `conciliacion-ciclo`): `POST /asignar` devolvía `validation_failed` y el
modal pintaba "Datos inválidos. Revisa los campos." con un payload que la propia UI había armado.
Un test que llevaba **saltando** empezó a correr al sembrar datos y lo destapó.

Al hacer fixtures deterministas, mantén el prefijo legible pero pon `-4xxx-8xxx-`.
Detección: `id::text !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'`.

Ojo a la incoherencia que esto destapa: un mismo endpoint puede validar el id de la **ruta** con un
regex laxo de forma hex y el del **cuerpo** con `.uuid()` estricto → acepta el id en una posición y
lo rechaza en la otra. Ver [[error-de-validacion-de-un-payload-que-arma-la-propia-ui-no-es-revisa-los-campos]] · [[facturaia]]
