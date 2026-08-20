---
title: un código de exención (E1-E6) no puede expresar una operación no sujeta, y el modelo lo acepta callado
date: 2026-08-20
source: facturaia
tags: [fiscal, verifactu, sii, iva, modelo-de-datos]
---
La AEAT tiene DOS ramas excluyentes, y un modelo de línea que solo guarda `exencion_codigo` (E1-E6) solo sabe hablar de una:

    <Sujeta><Exenta>          → OperacionExenta   E1..E6
    <Sujeta><NoExenta>        → CalificacionOperacion  S1 (sin ISP) · S2 (con ISP)
    <NoSujeta>                → N1 (art. 7/14) · N2 (reglas de localización)

**El caso que lo revienta**: servicio B2B a una empresa de otro Estado UE. No es exento, es **no sujeto** — el art. 69.Uno.1º LIVA lo localiza en el país del cliente, así que es **N2** (casilla 59 del 303). Tampoco es S2: S2 es cuando la operación SÍ se localiza en España y el sujeto pasivo se desplaza al destinatario (art. 84.Uno.2º).

En TuFacturaIA se emitía como **E5**, que es «entrega intracomunitaria de **BIENES** exenta» (art. 25 LIVA). O sea: una entrega de bienes exenta declarada por cada suscripción de software europea. No era cosmético — el mapeador de VeriFactu convierte cualquier `exencion_codigo` en `<OperacionExenta>`.

- El XSD del SII lo separa explícitamente: `NoSujetaType` tiene `ImporteTAIReglasLocalizacion`; `SujetaType` tiene `Exenta`. Si tu modelo no distingue esas dos ramas, le falta un campo.
- Ante un IVA 0 sin código que encaje, **no facturar** y aparcar con motivo + alerta. Un documento fiscal falso es peor que ningún documento.
- Y el motivo del hueco va separado del genérico «sin desglose»: aquí no falta el dato del proveedor, falta la casilla propia.

Relacionado: [[verifactu-xml-desglose-obligatorio-xsd-rechaza-sin-el]] · [[enum-legal-hardcodeado-en-ui-falsifica-motivos]] · [[facturaia]]
