---
title: la integración entre dos productos propios no se cobra como acceso a la api
date: 2026-08-17
source: claude-code-session
tags: [packaging, precios, saas, integraciones, facturaia, tucrmia]
---

Al conectar dos productos de la misma casa, el reflejo es reutilizar el derecho que ya
existe («acceso API»). Eso pone el vínculo detrás del plan más caro y mata el paquete: el
cliente ya paga el producto B, y encima tiene que subir de plan en A para que se hablen.

Cómo lo hace la industria (verificado 17-ago-2026):
- **Zoho Books ↔ Zoho CRM** (el comparable exacto): integración **nativa, sin derecho de
  API**, funciona incluso con el CRM en plan Free. Lo que recorta el plan bajo no es el
  vínculo sino su *alcance* — en Free no sincroniza productos porque esa edición no tiene
  el módulo Products.
- **HubSpot**: API en todos los planes, Free incluido; lo que escala con el tier es el
  **rate limit**, no el permiso.
- **Salesforce**: el contraejemplo — API por edición y add-on de +25 $/usuario/mes.

Patrón: la API pública se monetiza (por tier, rate limit o add-on), pero **el vínculo de
primera parte va por un derecho propio y se cobra en el producto que activas, no en el que
conectas**. El alcance lo recorta sola la matriz de planes que ya tienes, sin código.

Antes de decidir «¿lo regalo o lo cobro?», mide qué es hoy ese derecho: en FacturaIA
resultó que `api_access` no era un add-on comprable, no era visible (`features.visible=
false`) y ni siquiera se pintaba en el highlight del plan. Lo que se cobraba era el delta
de plan, no la feature. Ver [[acotar-una-api-por-scopes-no-la-acota-usa-allowlist-de-endpoints]].
