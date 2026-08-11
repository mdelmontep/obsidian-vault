---
title: el guard va en la transición única que comparten todos los caminos, no en el endpoint
date: 2026-07-31
source: claude-code-session
tags: [arquitectura, guards, api, tests]
---
Cuando una regla de negocio hay que imponerla y existen varios caminos que llevan al
mismo cambio de estado (web, lote, API pública, agente/copiloto), ponerla en el
endpoint garantiza que faltará en los hermanos — es el patrón nº1 de la auditoría de
FacturaIA, con 6 casos.

Busca el paso que **todos** comparten (aquí `sin_aprobar → pendiente`, en el núcleo
`aprobarRecibida`) y pon ahí la comprobación, antes de la primera escritura. Una sola
comprobación cubre los cuatro caminos.

Señal de que acertaste: al añadir el código de error nuevo, el **typecheck** falla en
todos los consumidores del tipo compartido (`Record<ErrorCode, string>` en la API v1 y
en el tool del copiloto) y te los enumera. Si no falla en ningún sitio, probablemente
lo pusiste en una hoja.

Aplicado dos veces con el mismo resultado: guard de importes negativos (`qa-009`,
#1398) y de posible duplicado (`qa-022`, #1411).
Relacionado: [[auditar-un-lado-de-par-simetrico-revisar-el-espejo]].

Tercer caso, otro dominio (AGH #945, 6-ago): un turno interrogativo («¿Vale?», muletilla de acuse)
ejecutaba el lote pendiente. El issue pedía el guard «antes de consultar los sets» — ahí cubría
**una de cuatro** puertas al atajo determinista. Puesto en la costura donde se DECIDE la respuesta,
cubre las cuatro. La pregunta útil no es «¿dónde está el bug?» sino **«¿quién más decide esto sin
pasar por el control?»**.

**Cuarto al décimo caso el mismo día, y ahí cambia la respuesta (FacturaIA 11-ago, barrido
funcional).** La misma forma —«el control existe en una puerta y falta en las hermanas»— salió **siete
veces** en secciones sin relación: fecha de inicio de recurrentes, series reservadas, cadena
VeriFACTU, importe del recordatorio, `requires_recalc` del fiscal, duplicado de recibidas y
conciliación. Y luego una versión con **doce instancias a la vez**: doce crons acumulan contador de
errores y devuelven `ok: true` fijo, con el mecanismo de reportar fallo ya existiendo en
`withCronTracking`.

A partir de cierta cardinalidad, **parchear las N puertas es el atajo**: deja el patrón vivo y el
elemento N+1 nace roto. Lo que cierra la clase es un **test de conformidad sobre el registro** que
recorra los N y exija la forma, con la excepción **declarada por escrito en el propio fichero** cuando
el fail-open sea deliberado. Señal para elegir: si puedes enumerar las puertas desde el repo (un
registry, un `git ls-files`, un enum), el contrato es posible y el parche es deuda. Ver
[[un-guard-enumera-la-clase-que-la-regla-escrita-solo-documenta]].

**Y el corolario que muerde: la EXCEPCIÓN legítima de un contrato deja a ese elemento con la vara más
corta, y suele ser el que más importa** (FacturaIA 11-ago). El contrato de crons exige que cada uno
pase por el wrapper que reporta fallos. `cron-watchdog` está exento **con razón**: el wrapper deja una
fila con lock in-flight hasta terminar, y si el watchdog muriese a mitad su propia fila colgada
bloquearía sus ejecuciones futuras, que es justo lo que él viene a desbloquear. Excepción correcta,
declarada por escrito.

El efecto colateral no lo era: junto con el wrapper se perdió el **aviso** que el wrapper emite. Un
fallo aislado de cualquier otro cron pinga al instante; los del vigilante solo se veían si encadenaba
dos seguidos. Medido: había fallado dos veces en dos semanas, las dos aisladas, las dos invisibles.
Quien vigila a los 45 se vigilaba con el criterio más flojo de los 46.

Regla: al declarar una excepción a un contrato, **enumera lo que el contrato le daba** y repón a mano
lo que siga aplicando. Y sospecha en particular cuando el exento es el vigilante, el healthcheck o el
que audita: la razón por la que no encaja en el molde suele ser la razón por la que nadie lo mira.
