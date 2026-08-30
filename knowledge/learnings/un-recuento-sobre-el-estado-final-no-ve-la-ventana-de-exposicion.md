---
title: un recuento sobre el estado final no ve la ventana de exposición
date: 2026-08-31
source: facturaia
tags: [learning, auditoria, seguridad, sql, verificacion, metodo]
---

Una auditoría que mide el **estado final** de cada objeto responde «¿está bien
hoy?». No responde «¿estuvo mal alguna vez?», y las dos preguntas se parecen lo
bastante como para que el número de la primera se lea como respuesta a la
segunda.

Caso, 31-ago-2026 en `facturaia`. El informe del barrido afirmaba **«0 casos de
`DROP FUNCTION`+`CREATE` sin `REVOKE`»**, y declaraba honestamente su método:
mirar el estado final a lo largo de las migraciones. Con ese método el 0 es
correcto. Con `git log -S` sobre la firma aparece lo que tapa:

- `602_fefo_firma_correcta.sql:287` recrea `aplicar_movimientos_lotes(uuid)` como
  `SECURITY DEFINER` con solo `grant execute … to service_role`, sin `REVOKE`.
- `754_albaranes_documento_propio.sql:1095` la revoca.
- Entre una y otra: **152 migraciones ejecutable por `anon` y `authenticated`**
  en producción.

Y el repo ya tenía un hook (`revoke-guard`) puesto exactamente por esto. El hook
no lo cazó porque nació después; la auditoría no lo cazó porque midió el presente.

**La regla:** para una propiedad de seguridad, «cuántos hay mal» se mide sobre el
estado, pero «cuántas veces estuvo mal» se mide sobre la historia. Si la
propiedad es *nunca debe estar expuesto*, la evidencia es `git log -S` /
`git log -p` sobre el símbolo, no un `grep` del árbol de hoy.

**Corolario, y es lo que hace caro el error:** un informe fechado que entra al
repo se convierte en referencia, y su «0» se cita luego como si nadie tuviera que
volver a mirar. Reverificar antes de mergear costó una hora y encontró seis
afirmaciones que no se sostenían — entre ellas dos recuentos (251 tablas con RLS
cuando una se había borrado; «1 de 235 funciones» cuando la migración citada
arregla 25). Lo que caduca es el ESTADO, no el análisis: se anota al pie con
fecha y evidencia, no se corrige el texto por encima.

De los hallazgos del subagente que hizo la reverificación, **dos venían con el
número mal** (24 en vez de 25; un recuento de ficheros distinto del real). Se
verificaron los dos lados antes de escribir nada.

Relacionado:
[[el-gate-escrito-justo-despues-del-arreglo-mide-cero-casos]],
[[dos-series-de-adr-con-el-mismo-prefijo-la-cita-resuelve-al-documento-equivocado]],
[[el-limite-silencioso-una-respuesta-que-llega-al-tope-parece-completa]].
