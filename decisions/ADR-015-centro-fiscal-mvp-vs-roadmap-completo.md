---
title: ADR-015 — Centro Fiscal IA arranca como MVP 4 semanas, no roadmap 11 semanas
date: 2026-05-22
status: accepted
tags: [adr, facturaia, fiscal, mvp]
---

## Contexto
Spec original planteaba 6 sprints (~11 semanas dev) + beta privada 2 trimestres + auditoría externa 2k€. Backlog ambicioso (303/390/130/111/115/180/190/347/349/131 + copiloto deducibilidad + Anexo II posicional). 0 clientes pagando hoy el add-on.

## Opciones consideradas
- **A — Roadmap completo 11 sem**: cubrir 100% scope antes de revenue. Riesgo: 6 meses sin validar pricing/scope con clientes reales. Coste oportunidad alto.
- **B — MVP 4 sem (303+130+libro IVA+share asesor)**: cortar 70% scope a v1.5 post-beta. WORM+eIDAS+RC no recortables (legal). 8 sem a revenue.
- **C — MVP 4 sem + entrevistas en paralelo**: arrancar dev mientras se validan 10 entrevistas. Riesgo de tirar 4 sem si pivota.

## Decisión
**B**. MVP 4 sem con scope estricto autónomo ED simplificada (target ~700k SAM ES). Investigación online sustituye entrevistas (research 42 fuentes valida pricing 14,90€ y "no presenta" no mata venta).

## Consecuencias
v1.5 entrega 347/111/115/349/190/copiloto-deducibilidad/A3-Holded en sem 9-14 post-beta. Convenio colaborador social AEAT diferido a 50 clientes pagando (ver [[ADR-017-centro-fiscal-no-presenta-v1]]). Anexo II posicional 303 en PR dedicado con XLSX oficial AEAT — TXT MVP es formato V1 con disclaimer "documento de apoyo". Beta privada 1 trimestre (no 2) + badge "Beta IA" post-GA.
