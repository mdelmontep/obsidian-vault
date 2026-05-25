---
name: cookie-impersonate-leak-fuera-de-admin
description: Cookies de impersonation/contexto deben borrarse del request, no solo de la response
metadata:
  type: feedback
---

En Next.js middleware/proxy, si solo borras una cookie en `supabaseResponse.cookies.delete()`, la cookie SIGUE viajando en LA request actual (browser ya la envió). El handler la lee y opera con ese valor. Solo la SIGUIENTE request del browser no la traerá.

**Why:** Caso real 2026-05-21 TuFacturaIA — cookie `impersonate_org` setteada en `/admin/orgs?impersonate=X` sobrevivía a navegación a `/settings`. El POST a `/api/team/members` la leía → orgId resuelto a la org impersonada → invitación creada en la org equivocada (Sandbox aparente, AgentesiaLab real). El middleware sí "borraba" la cookie en la response, pero el handler ya la había leído.

**How to apply:** Cookies de contexto/impersonation deben confinarse al path donde tienen sentido. Si el path actual NO matchea el scope (`/admin/*` para impersonate, `/checkout/*` para session token, etc.), borrarlas EN AMBOS lados: `request.cookies.delete('X')` (para que el handler no las vea) Y `response.cookies.delete('X')` (para que el browser no las reenvíe). Sin la primera, hay leak silencioso en la request actual. Vale para cualquier cookie de scope estrecho (impersonation, dry-run mode, etc.).
