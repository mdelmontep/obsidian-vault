---
title: presupuesto-desarrollo — modo solo total con horas y reparto back end / front end
date: 2026-10-15
source: agentesia-lab (P2026-0017 Orión Dental)
tags: [inbox, skills, presupuestos]
---
Para el P2026-0017 se parcheó una copia del motor (guardada en `~/Documents/Orion/motor/presupuesto_desarrollo.py`) (la skill de `~/Projects/agentesia-skills` tenía cambios sin commitear de otra sesión). El parche añade `horas` por módulo (columna HORAS EST. en modo `solo_total`) y, si cada módulo trae `back` y `front`, las columnas BACK END / FRONT END con sus totales; comprueba que `back + front == horas`. Propuesta: portarlo a la skill junto con la tarifa de 30 €/h (18,75 € de coste + costes operativos + 20 % de margen).
