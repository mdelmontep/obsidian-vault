---
title: retell create-knowledge-base requiere multipart no json
date: 2026-05-22
source: claude-code-session
tags: [retell, knowledge-base, api]
---

`POST /create-knowledge-base` con `Content-Type: application/json` devuelve **500 Internal Server Error** silencioso (incluso con payload mínimo válido).

Requiere `multipart/form-data`. `knowledge_base_texts` se pasa como **JSON-string dentro de un form field**, no como nested JSON.

Funciona:
```bash
curl -X POST https://api.retellai.com/create-knowledge-base \
  -H "Authorization: Bearer $RK" \
  -F "knowledge_base_name=EcoBox - Info" \
  -F "knowledge_base_texts=[{\"title\":\"Q1\",\"text\":\"...\"}]"
```

Schema cada text: `{title: string, text: string}`. Devuelve `knowledge_base_id` + status `in_progress` (procesa embeddings asíncrono ~30s-2min).

Attach al flow después: `PATCH update-conversation-flow` con `knowledge_base_ids: ["kb_xxx"]` + `kb_config: {top_k:3, filter_score:0.6}`.

Caso real: EcoBox 2026-05 — perdí 20min con json puro hasta leer docs y cambiar a multipart.

**`knowledge_base_texts` revienta con documentos grandes** (10-sep-2026, Laserys):
`POST /add-knowledge-base-sources/{kb_id}` con un texto de **14 KB** devolvió **500** en tres
formatos distintos, mientras que un array corto pasaba — no es el formato, es el tamaño. La vía que
funciona para un documento entero es subirlo como fichero:

```bash
curl -X POST "https://api.retellai.com/add-knowledge-base-sources/$KB" \
  -H "Authorization: Bearer $RK" \
  -F "knowledge_base_files=@knowledge_base.md;type=text/markdown"     # HTTP 200
```

Borrar la fuente vieja: `DELETE /delete-knowledge-base-source/{kb_id}/source/{source_id}`.
Ver [[la-kb-del-proveedor-y-tu-rag-son-dos-fuentes-y-hay-que-corregir-las-dos]].
