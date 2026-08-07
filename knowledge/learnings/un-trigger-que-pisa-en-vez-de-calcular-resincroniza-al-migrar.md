---
title: un trigger que PISA en vez de calcular resincroniza datos al migrar
date: 2026-08-07
source: claude-code-session
tags: [postgres, migraciones, triggers, datos]
---

Una migración de unidad dividía el catálogo por un factor. Los materiales con
tipo los bajaba el trigger de propagación... pero ese trigger **no divide,
pisa**: `SET tiempo_mo_horas = NEW.horas`. A los que ya diferían de su tipo les
metía el valor del tipo y **los resincronizaba de paso**.

Resultado: **188 materiales cambiaron de precio** en una migración que prometía
no mover ninguno. Lo paró su assert (187,44 → 187,50) y la transacción entera
hizo rollback.

**La regla**: antes de apoyarte en un trigger para propagar una conversión, mira
si CALCULA o si COPIA. Si copia, no propaga tu transformación: propaga el valor
de la fila padre, y de camino corrige toda desincronía preexistente. Una
migración de UNIDAD no debe cambiar VALORES, aunque el cambio «mejore» el dato.

**El arreglo**: soltar ese trigger durante la conversión y convertir cada fila
por su propio valor. La desincronía se conserva exactamente, en la unidad nueva.

**Cómo detectarlo antes**: cuenta las filas hijas cuyo valor difiere del padre.
Si no es cero, el trigger te va a resincronizar. Aquí eran 1.329.

Relacionado: [[alter-column-type-choca-con-cualquier-trigger-update-of]] ·
[[un-guard-que-se-apoya-en-una-medicion-externa-no-es-un-guard]]
