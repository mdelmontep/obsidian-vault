---
title: una consulta que devuelve cero filas no ha recorrido la cadena de permisos
date: 2026-09-05
source: facturaia
tags: [postgres, seguridad, verificacion, tests]
---

Verifiqué un `GRANT` con `SET LOCAL ROLE authenticated` y un `SELECT` sobre la función de
entrada. Salió limpio. Estaba roto: la org de prueba no tenía facturas, así que el planificador
**nunca llegó a ejecutar el `CROSS JOIN LATERAL`** que llama a la función de nivel 2, y su ACL
no se comprobó nunca. Un `GRANT` de nivel 1 con cero filas da verde sobre una cadena cerrada.

Postgres comprueba el permiso de una función **al ejecutarla**, no al planificar. Por tanto:
para medir permisos hay que **sembrar el dato que obliga a recorrer el eslabón profundo** y
afirmar sobre la CIFRA que sale, no sobre la ausencia de error.

Y el candado no se escribe como lista de nombres: se **deriva del catálogo** — un `WITH
RECURSIVE` sobre `pg_proc.prosrc` desde las puertas, parando en el primer `prosecdef` (un
DEFINER corta la propagación por diseño). Así un eslabón nuevo entra por existir, no por que
alguien se acuerde de añadirlo. Mismo criterio que [[el-arnes-se-mide-a-si-mismo]].

**La regla general: cero filas no es una medición, es la ausencia de una.** Aquí la causa fue la
profundidad del plan; el mismo día, otra sesión leyó tres «cero filas» de prod como «no hay
movimientos» cuando en realidad el UUID del predicado se lo había inventado al completar un id
truncado por una compactación — los productos reales tenían 23 y 42 movimientos. Las dos dan
verde sin haber comprobado nada. Antes de concluir de un cero: enseñar que el predicado
selecciona algo real, o contrastar con una medida de otra naturaleza. Ver
[[feedback_conteo_con_grep_falla_en_silencio]].

Ver [[clonar-una-migracion-clona-tambien-a-quien-puede-llamarla]].
