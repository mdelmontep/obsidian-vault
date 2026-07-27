---
title: un check de coherencia solo puede AFIRMAR un desajuste con respuesta afirmativa de la fuente; no poder preguntar es otra categoría
date: 2026-07-26
source: claude-code-session
tags: [observabilidad, alertas, stripe, billing, facturaia, diseño]
---

Todo check que compara BD contra un sistema externo tiene tres resultados, no
dos: **coherente**, **desajuste confirmado** y **no se pudo verificar**. Colapsar
el tercero en el segundo produce alertas que mienten en la dirección peligrosa,
porque el operador actúa sobre datos que están bien.

Caso FacturaIA 2026-07-26: `checkPriceCoherence` etiquetaba cualquier `!res.ok`
de Stripe como `kind: 'missing'`. Sin `STRIPE_SECRET_KEY` en el entorno, el
cliente REST devuelve `ok:false` **sin llamar a Stripe**, así que el panel
mostraba 12 incidencias ALTAS "el precio no existe en Stripe", una por cada fila
`active` de `plan_prices`. No había ni un desajuste: verificado luego contra
Stripe real, los 12 precios existen, están activos y cuadran al céntimo.

Lo grave no es el ruido, es que **la alerta induce la acción destructiva**: ante
"los 12 precios no existen" lo natural es recrearlos, y eso deja precios
duplicados en Stripe y suscripciones vivas apuntando a prices archivados. En
producción el mismo falso positivo lo dispara una clave rotada (401) o un 429.

Reglas que salieron:

- El estado "desajuste" exige confirmación explícita de la fuente. Para Stripe,
  `missing` = `404` **y** `code === 'resource_missing'`; un 404 pelado, no.
- Lo no verificable viaja en un campo aparte (`unavailable: {reason, status,
  unchecked}`) y se pinta como UNA incidencia media de "check no verificado",
  nunca N altas. Un fallo sistémico no debe escalar con el número de filas.
- Distinguir el fallo que afecta a TODAS las filas (clave ausente, 401: cortar el
  barrido en la primera, seguir solo repite el error N veces) del puntual (429:
  anotar y continuar, o pierdes desajustes reales de las filas siguientes).
- El pico de la pirámide: un smoke que lee "0 desajustes" cuando en realidad no
  pudo preguntar está dando verde a ciegas. Si el barrido no se completó, falla.

Síntoma que delata este bug antes de investigar: **fallan TODAS las filas y todas
con el mismo `kind`**. Un desajuste real es parcial y mezcla tipos.
Ver [[observabilidad-fallback-conservar-error-canal-primario]] ·
[[alerta-por-conteo-de-estado-debe-acotar-a-entidades-activas]] ·
[[no-verificar-una-clave-read-only-escribiendo-con-ella]]
