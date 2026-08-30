---
title: «verificado contra el repo» no ve la columna que un ADR mandó borrar
date: 2026-08-30
source: facturaia, agh-iberica
tags: [auditoria, adr, planificacion, subagentes]
---
Un plan de arquitectura salido de un agente traía tres marcas «✔ verificado tras verificación
local» y aun así escribía `INSERT ... addon_purchasable`, una columna borrada nueve migraciones
antes. La migración habría fallado al aplicarse.

Lo delató una auditoría **contra los ADRs**, no contra el código. Y tiene sentido: leer el código
te dice **qué existe**; solo el registro de decisiones te dice **qué se quitó a propósito y por
qué**, que es justo lo que un plan tiende a reintroducir sin saberlo.

Patrón: todo plan que vaya a tocar esquema se audita en **dos ejes separados** —contra el código
vigente y contra las decisiones registradas—, y son dos pasadas distintas. Un agente que verifica
lo que él mismo eligió mirar no cubre el segundo eje jamás.

Relacionado: [[dos-catalogos-exportados-del-mismo-saas-pueden-contradecirse]]
