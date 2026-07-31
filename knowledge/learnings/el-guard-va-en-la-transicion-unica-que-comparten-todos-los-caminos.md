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
