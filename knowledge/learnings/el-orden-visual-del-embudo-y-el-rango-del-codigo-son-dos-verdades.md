---
title: el orden visual del embudo y el rango del código son dos verdades distintas
date: 2026-09-08
source: centro-elphis
tags: [crm, clientify, embudo, integracion]
---
Un bot que sube etapas usa un `RANK` en su código; el CRM ordena las columnas por `position`. Nadie
sincroniza las dos, y al divergir el deal **retrocede a los ojos del cliente** mientras el código cree
que avanza. En Elphis el código tenía Profesional(3) < Enlace(4) y Clientify mostraba Enlace(3) <
Profesional(5): exactamente al revés.

- Síntoma: «el CRM se comporta raro» sin ningún error en logs. La escalera funciona; la vista miente.
- Los huecos y empates en `position` (0,1,2,3,5,6,6) son la pista: los deja la UI al crear etapas.
  Con empate, el desempate lo elige el servidor — salió «Visita Realizada» antes que «Programada».
- Fix barato: mover `position` para que coincida con el RANK ya desplegado y probado, en vez de tocar
  código. `PUT /deals/pipelines/stages/<id>/` con los 4 campos escribibles; no mueve ningún deal.
- Verificar con censo de deals por etapa antes y después: si un solo deal cambia de columna, el
  cambio no era cosmético. Ver [[clientify-discovery-elphis]].
