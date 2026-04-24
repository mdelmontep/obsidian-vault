---
title: google favicon api patron auto-logo para proveedores
date: 2026-04-25
source: claude-code-session
tags: [api, logos, facturaia, patron]
---

Patrón para auto-asignar logos a proveedores/clientes al crearlos:

## Flujo

1. Al cargar la lista, filtrar entradas con `logo_url = null` (nunca buscadas)
2. Para cada una, llamar a `/api/logo-fetch` con el nombre
3. API extrae slug del nombre (quita S.L./S.A., normaliza acentos, solo alfanumérico)
4. Modo **strict** (auto): solo prueba `{slug}.es` y `{slug}.com`
5. Modo **broad** (manual): prueba variantes (1ra palabra, 2 palabras, nombre completo) × 5 TLDs
6. Si encuentra favicon >750 bytes, guarda la URL del más grande (`best`)
7. Si no encuentra nada, guarda `'not_found'` → no vuelve a buscar

## Sentinel `not_found`

Distingue tres estados sin migración extra:
- `null` → nunca buscado → auto-fetch
- `'not_found'` → buscado, sin resultado → mostrar iniciales, no re-buscar
- `'https://...'` → tiene logo → mostrar imagen

## Display

```tsx
{c.logo_url && c.logo_url !== 'not_found'
  ? <img src={c.logo_url} className="cc-avatar-img" />
  : <div className="cc-avatar">{initials}</div>}
```

## Fallback manual

Modal con búsqueda broad + campo URL directa + subir archivo.

Ver también: [[clearbit-logo-api-ya-no-existe]]
