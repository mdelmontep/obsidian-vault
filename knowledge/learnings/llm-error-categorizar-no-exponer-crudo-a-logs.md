---
title: LLM — categorizar error en buckets accionables, NO loggear objeto crudo
date: 2026-05-19
source: facturaia auditoría cruzada Sprint 3
tags: [llm, seguridad, observabilidad, ux]
---

`console.error('[ai] failed', err)` con objeto `err` crudo es un **leak potencial**: errores de `fetch` Node 22 / undici incluyen `cause` con URL del provider; errores del SDK Anthropic/OpenAI pueden incluir headers reflejados (`x-api-key`), body de respuesta con datos cliente, IPs, claves truncadas. Va a logs Dokploy/Vercel persistentes consultados por cualquiera con acceso al panel.

Patrón seguro: **categorizar antes de loggear**.

```ts
type LlmErrorKind = 'timeout' | 'rate_limit' | 'auth_error' | 'provider_unreachable' | 'unknown'

function categorizeLlmError(err: unknown): LlmErrorKind {
  if (!err) return 'unknown'
  const e = err as { name?: string; status?: number; code?: string; message?: string }
  const msg = (e.message ?? '').toLowerCase()
  if (e.name === 'AbortError' || msg.includes('timeout')) return 'timeout'
  if (e.status === 429 || msg.includes('rate limit')) return 'rate_limit'
  if (e.status === 401 || e.status === 403) return 'auth_error'
  if (e.code === 'ECONNREFUSED' || e.code === 'ENOTFOUND' || msg.includes('fetch failed')) {
    return 'provider_unreachable'
  }
  return 'unknown'
}

// Log seguro: SOLO propiedades primitivas + message truncado.
console.error('[ai] failed', {
  kind,
  name: e?.name,
  status: e?.status,
  code: e?.code,
  message: e?.message?.slice(0, 200),
})
```

Beneficios:
1. **No leak**: nunca el objeto `err` entero a logs.
2. **UX**: cada kind → mensaje específico al user (`errorIssueFor(kind)`): "espera 30s" para rate_limit, "avisa soporte" para auth_error, "provider caído" para unreachable. No "algo falló" genérico.
3. **Cache invalidation**: TTL distinto por kind. Auth_error nunca se cachea (rotar key debe surtir efecto inmediato). Rate_limit/timeout cachean 30s (no martillear provider).
4. **Métricas accionables**: count por kind muestra qué provider está degradado.

Caso real TuFacturaIA: `ai-validate.ts` validación VeriFACTU pre-emisión. Antes: modal "No se pudo ejecutar la validación asistida" genérico + reintentos idénticos llamaban al provider. Ahora: cache LRU sha256 hash + mensaje específico por kind + log estructurado.
