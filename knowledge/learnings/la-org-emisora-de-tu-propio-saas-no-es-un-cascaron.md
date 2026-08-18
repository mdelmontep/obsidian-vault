---
title: al facturar tu SaaS con tu propio producto, la org emisora no es un cascarón
date: 2026-08-18
source: claude-code-session
tags: [facturacion, dogfooding, multitenant, cuotas]
---

Dogfooding de facturación: tu SaaS emite sus propias facturas de suscripción desde dentro del
producto. La trampa es dar por hecho que la organización emisora es un buzón técnico. Medido en
TuFacturaIA el 18-ago: `AgentesiaLab SL` ya tenía 13 facturas emitidas de la consultora, la serie
A por el número 68 y 148 recibidas. Es una cuenta de trabajo real.

Tres cosas que se heredan y hay que decidir a propósito, no por omisión:

- **La cuota del plan aplica.** El gate de emisión es el mismo para esa org que para un cliente:
  si se agota el cap mensual, quien deja de recibir su factura es **quien ya te ha pagado**. Se
  cierra con un override de límite para esa org, no añadiendo un «saltarse la cuota» al creador de
  documentos — esa puerta acaba usándose desde otro sitio.
- **La serie se comparte** con la facturación del otro negocio si no eliges una dedicada: un hueco
  por un fallo del webhook es un hueco en la numeración de la empresa entera.
- **Lo que presume tu producto tiene que estar encendido AHÍ.** Si vendes cumplimiento (VeriFACTU,
  firma, sellado) y tu propia org lo tiene apagado, mudar la emisión a casa no compra la
  conformidad que motivaba el cambio: solo mueve el incumplimiento de sitio.

Ver [[facturar-lo-ya-cobrado-sin-registrar-el-cobro-lo-mete-en-reclamacion]].
