---
title: ADR-047 — escalón 1 (OpenAI directo) para el agente de AGH, provisional
date: 2026-08-05
status: accepted
tags: [adr, agh-iberica, rgpd, llm]
---

## Contexto
El agente de AGH corre hoy contra OpenAI vía `MODEL_GATEWAY_URL` (OpenAI-compatible). El cliente final
son multinacionales (Dragados, McDonald's, aseguradoras) y `arquitectura-rag-enterprise.html` define
tres escalones de seguridad. Había que elegir uno **de proveedor** para poder seguir, sin que esa
elección se confunda con el permiso de datos.

## Opciones consideradas
- **1 · OpenAI directo + DPA + retención cero** — cero esfuerzo; el dato sale a EE. UU. bajo contrato.
- **2 · Azure OpenAI / Bedrock región UE** — el dato no sale de la UE; es cambio de `MODEL_GATEWAY_URL`; es lo que el propio documento recomienda por defecto para multinacional.
- **3 · Modelo open-weight autohospedado** — el dato no sale; no requiere permiso de nadie; exige GPU (el Dokploy actual no tiene) y **re-medir el banco de evals**, calibrado sobre gpt-4o.

## Decisión
**1**, de forma **provisional y declarada como tal** (Manu, 05-ago-2026): «de momento OpenAI, y se
cambia si es necesario». El coste de cambiar de opinión es bajo por diseño — ADR-0001 hizo el gateway
provider-agnóstico, así que 1→2 y 1→3 son **configuración, no reescritura**.

## Consecuencias
- No cierra ninguna puerta: el salto a 2 o 3 sigue siendo un cambio de env.
- **NO autoriza el egress de filas de cartera al modelo.** Son dos decisiones distintas: el proveedor
  es nuestro; el permiso es del **cliente final** (AGH es responsable del tratamiento, nosotros
  encargados). El flag `READ_PRESENTER_ENABLED` sigue apagado y la fase de prosa/bucle sigue bloqueada
  por alcance del piloto, DPA/retención y confirmación de diseño. Ver
  [[una-decision-pendiente-sin-issue-no-esta-en-ninguna-cola]].
- Si algún día se mide el escalón 3, el experimento ya está barato: apuntar el gateway a un vLLM en una
  GPU alquilada y correr el banco → un número por eje, no una opinión.
- Lo que el permiso **no** ahorra: slot-filling en vez de prosa libre, diccionario de valores del turno
  y defensas de inyección desde el CRM son necesarios en los tres escalones, porque van de que el
  modelo invente o sea manipulado, no de dónde corre.
