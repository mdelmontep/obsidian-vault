---
title: n8n que reimplementa lógica backend se salta sus defensas
date: 2026-05-27
source: claude-code-session
tags: [n8n, seguridad, backend, sanitizacion]
---

Cuando un workflow n8n replica lo que ya hace un endpoint backend (sanitización, validación, permisos), lo hace sin heredar esas defensas. Divergencia silenciosa hasta que alguien audita.

**Caso real**: `ingesta/route.ts` sanitiza `filename` con `/[^a-zA-Z0-9.\-_]/g`. El nodo `Preparar Datos Ingesta` en n8n construía el mismo `storage_path` con `filename` crudo de Meta → path traversal posible.

**Patrón**: toda lógica de negocio que vive en backend Y en n8n crea dos fuentes de verdad. La de n8n no tiene tests, no tiene PR review de seguridad, y se actualiza por parches.

**Fix/regla**:
1. Si n8n consume un endpoint interno, que el endpoint haga la sanitización — n8n solo pasa el dato crudo.
2. Si n8n DEBE construir paths/IDs directamente, replicar la misma regex que el backend con comentario explícito `# mismo patrón que <ruta>`.
3. En auditorías: buscar `storage_path`, `destPath`, `filename` en jsCode y verificar que hay `.replace(...)` antes del uso.

Ver [[n8n-dollar-json-tras-http-es-respuesta-http-no-item-original]] (patrón similar: n8n asume contexto que el backend gestiona).
