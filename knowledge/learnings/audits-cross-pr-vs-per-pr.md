---
name: audits-cross-pr-vs-per-pr
description: Auditar PRs individuales no detecta bugs por composición. Patrón process — tras N PRs que tocan el mismo subsistema, hacer audit adicional cross-PR con agentes centrados en interacciones.
date: 2026-05-20
source: claude-code-session
tags: [process, audit, multi-agent]
---

**Síntoma**: 4 audits per-PR (3 agentes paralelos cada uno) pasaron con 0-5 bloqueantes cerrables. Tras 5 PRs sobre el mismo módulo (multi-org + equipo + bot WhatsApp), audit GLOBAL cross-PR detectó 2 bloqueantes nuevos NO visibles per-PR: loop redirect `/login↔/dashboard` por interacción signOut/JWT/layout-server entre PR-1 + PR-3a.

**Patrón**: lanzar audit adicional con 3 agentes paralelos centrados en COMPOSICIÓN — escenarios completos que cruzan archivos de varios PRs. Ejemplos a auditar siempre: race entre signOut/JWT/layout, sticky bot vs `active_org_id` vs cookie `impersonate_org`, force_reactivate vs auditoría log, lifecycle complete (invitar → aceptar → switch → eliminar → reactivar).

**Falsos positivos esperados**: cross-PR genera ~50% FPs por agente porque desconoce contexto granular. Filtrar agresivamente. Vale la pena: 2 bloqueantes reales evitados > coste de 3 agentes adicionales.

**Patrón "componentes huérfanos" (Centro Fiscal 2026-05-22)**: en composición multi-agente paralela, un agente puede escribir componentes premium (virtualizados, drill-down, drawers) que OTRO agente no monta porque reimplementó versiones simples en la página padre. Check obligatorio del auditor cross-PR: `grep -rE "import.*from.*<carpeta-componentes>" <carpeta-pages>` y verificar que cada componente exportado tiene ≥1 import real. Caso: 2D-3 escribió `CasillasTabla` + `FacturasIncluidas` + 2 drawers; 2D-1 reimplementó simple en `detalle-vista.tsx` sin importarlos. 5 componentes pulidos huérfanos hasta que la siguiente ola lo cazó.
