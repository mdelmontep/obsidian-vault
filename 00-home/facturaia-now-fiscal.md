---
title: FacturaIA — NOW Fiscal y VeriFactu
updated: 2026-09-25
tags: [facturaia, now, fiscal]
---

# NOW — Fiscal y VeriFactu

Extraído del dashboard de [[facturaia]] el 22-sep-2026: el NOW tenía 59 frentes y 22 KB,
la mitad del arranque de cada sesión. Aquí viven los 9 de esta área, íntegros.

Vuelve al hub: [[facturaia]]

- 🟢 **El devengo, cerrado de punta a punta y en prod (13→20-sep)** — abono periodificado por fecha de expedición (#2807, mig 922, ADR-100), y el 347, el libro registro y el asiento contable leyendo ya esa fuente (#2833-#2835, #2831). Fuera, con issue: los devengos especiales del 75.Dos y 75.Uno.8º (**#2810 · #2808 · #2786**). Detalle → [[facturaia-historico-snapshot-2026-09-14]]
- 🟠 **Ticket 182 · fecha de operación en todas las superficies: cerrado lo construible y su code review (26-sep)**: #2839-#2841, #2947-#2953 y los arreglos del review #2956 (ADR-106 con norma), #2964 (un solo 422 y la vista previa de obra valida), #2974 (el «hoy» en día de Madrid) y #2975 (candados del abono que muerden). **Queda**: #2934 y #2936 (cuelgan de #2786); #2940 punto 1 (periodificar por cobro las certificaciones, cambia el 303); **decisión fiscal**: obra solo de mano de obra con `fecha_operacion` vacía declara tarde el IVA si cruza trimestre, y hace falta un flag de «aportación de materiales» en la obra (ADR-106); smoke del MCP con `fecha_operacion` en sesión nueva.
- 🟠 **Siete decisiones fiscales abiertas, con encargo escrito (23-ago)** — para decidirlas con fuente primaria: `docs/architecture/PROMPT-decisiones-fiscales-con-norma.md` (#2135). Reparto: mías la cola fiscal + #2133; #2131 y #2136 en prod.
- 📅 **303: el 3T vence el 20-oct.**
- ⏸️ **EN STANDBY por decisión de Manu (24-ago): los dos trámites del certificado FNMT de AgentesiaLab** — el `.p12` para VeriFACTU (bloquea el SELLADO, no la emisión) y el 036 de alta en el ROI. Ninguno lo puede hacer un agente. Detalle → [[facturaia-historico-detallado]]
- 🟠 **Arnés y WORM: 3 de 5 tracks cerrados (20-ago)** — **queda**: key de B2 sin `deleteFiles`, sellar al exportar (**tuyo**, producto) y puerto por checkout en E2E. → `PROMPT-continuacion-20-ago-arnes-y-worm.md` · [[hook-que-resuelve-git-en-el-cwd-de-la-sesion-juzga-el-repo-equivocado]]
- 🟠 **Barrido T1: del item 1 solo queda el punto 4, la deriva de perfil (18-ago)** — comparar `perfilFiscalHash` desde el cron choca con que el calculador es fuente única en TS: decisión de arquitectura, no parche. Lo cerrado → [[facturaia-historico-eventos]] · `docs/architecture/PROMPT-fiscal-inventario-cobros-t1.md`
- 🟠 **Fiscal, orden vivo: #1933 y #1934 EN PROD (migs 722/741/742, 22-ago) → queda #1899** — el #1934 registra justificante y aceptada/rechazada en `resultado_aeat`; el #1899 (rectificativa) es `ready-for-human`, falta payload real. → [[facturaia-historico-snapshot-2026-08-19]] · [[ADR-055-la-rectificativa-del-303-va-detras-de-capturar-el-justificante]]
- 🟠 **#1668: solo queda la decisión de producto** — el manual ya no promete de más (corregido en #1976); lo abierto es si hay que sellar al EXPORTAR → §Decisiones pendientes. **#1669 staging: DECIDIDO dejarlo como está** (46 migraciones de retraso, cero consumidores). → [[facturaia-historico-snapshot-2026-08-19]]
- 🟠 **Decisión de producto pendiente: exigir certificado activo para `verifactu_activo=true`** — hoy `PUT /api/settings/verifactu` deja activarlo sin certificado, y entonces el worker hace `if (!cert) continue` en silencio y las facturas se quedan en `pendiente_envio` para siempre. Notificar sin ese gate dispararía sobre orgs a mitad de configurar.
