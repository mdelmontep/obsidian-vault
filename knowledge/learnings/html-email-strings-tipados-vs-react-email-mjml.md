---
title: 5-10 templates email — html strings tipados gana a react email o mjml
date: 2026-05-25
source: claude-code-session
tags: [email, arquitectura, decisiones]
---

Para 5-10 templates email transaccionales simples, el overhead de React Email o MJML no se justifica:

- **React Email** (~250 KB deps + `@react-email/render` con `react-dom/server`): emails se envían desde server actions / route handlers (no RSC streaming). Tree React solo produce un string que pasa a Resend. En stacks con Dokploy/Alpine/Puppeteer ya hay fricción Docker — menos deps = menos sorpresas en build.
- **MJML**: parser/compilador runtime o build-step adicional. Sintaxis declarativa que abstrae primitives. Cuando necesitas hacks específicos (MSO conditional, VML bulletproof buttons, dark-mode `[data-ogsc]` Gmail iOS, tablas Outlook, inline CSS forzado) la abstracción estorba.

**Patrón ganador para 5-10 templates**: HTML strings con helpers tipados.

```
templates/
  types.ts        (TemplateData<K> discriminated union, RenderedEmail)
  theme.ts        (resolveTheme desde org config)
  layout/         (base, header, footer, button MSO, info-block)
  emails/         (factura-enviada, otp, team-invite, ...)
  index.ts        (renderEmail<K>(kind, data): RenderedEmail)
```

Pros: control byte-a-byte, debugging cross-client por output crudo, snapshots vitest diffs legibles, type-safety con discriminated union sin runtime cost, cero deps nuevas, integra con escape helpers de seguridad.

Umbral de cambio: 30+ templates o editor visual admin demandado → entonces React Email reduce mantenimiento. Ver [[ADR-021-html-email-strings-vs-react-email-mjml]].
