---
title: "efecto que recarga por entidad + setters que mergean = estado stale de la entidad anterior"
date: 2026-06-12
source: claude-code-session
tags: [react, multi-org, state]
---

Un `useEffect` con deps `[entityId]` que recarga datos NO basta si los setters dentro
de `load()` solo AÑADEN claves (`setX(prev => ({...prev, k: v}))`): las claves que la
nueva entidad no emite conservan el valor de la anterior. Caso ticket facturaia
cac5eefc: al cambiar de org, `/agentes` seguía pintando whatsapp/email "Conectado"
de la org previa porque la nueva no escribía esas claves.

**Fix**: primera línea de `load()` = reset explícito de TODO el estado per-entidad
(`setLoaded(false)`, `setConfig({})`, paneles expandidos, confirms...). Excluir
estado per-user o el que ya se reemplaza entero.

**Detectar**: grep de `prev =>` / spread de prev en componentes cuyos efectos
dependen de org/tenant/entity id.
