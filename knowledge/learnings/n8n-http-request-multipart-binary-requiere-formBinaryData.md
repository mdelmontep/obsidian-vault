---
title: n8n http request multipart binary requiere formBinaryData
date: 2026-04-26
source: claude-code-session
tags: [n8n, whatsapp, http-request, binary]
---

# n8n HTTP Request v4.2 — multipart con binary requiere `formBinaryData`

Cuando se envía un archivo binario como `multipart/form-data`, el nombre del campo en el form se controla de forma diferente según el método:

## Método incorrecto (falla)

```json
{
  "contentType": "multipart-form-data",
  "sendBinaryData": true,
  "binaryPropertyName": "data",
  "inputDataFieldName": "file"
}
```

`binaryPropertyName` controla TANTO qué binary property leer del item n8n COMO el nombre del campo en el form. `inputDataFieldName` a nivel de nodo **solo aplica a `contentType: "binaryData"`**, no a multipart. Resultado: campo form = `"data"`, no `"file"`.

## Método correcto

```json
{
  "contentType": "multipart-form-data",
  "sendBody": true,
  "bodyParameters": {
    "parameters": [
      { "name": "messaging_product", "value": "whatsapp" },
      { "name": "type", "value": "application/pdf" },
      { "parameterType": "formBinaryData", "name": "file", "inputDataFieldName": "data" }
    ]
  }
}
```

`parameterType: "formBinaryData"` permite controlar el nombre del campo (`name: "file"`) independiente del nombre del binary en n8n (`inputDataFieldName: "data"`).

**Caso real**: WhatsApp Media API (`POST /{phone_number_id}/media`) requiere campo `file`. Sin `formBinaryData`, devuelve `"(#100) The parameter file is required."`.
