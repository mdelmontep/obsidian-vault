---
title: npm audit fix --force puede downgradear majors — usar overrides
date: 2026-06-17
source: claude-code-session
tags: [npm, seguridad, dependencias]
---
`npm audit fix --force` resuelve vulns transitivas retrocediendo la dep padre
a una major MÁS VIEJA si es el camino fácil. Casos reales: proponía exceljs
4.4.0→3.4.0 y next 16→9 para parchear uuid/postcss transitivos. Nunca correr
--force a ciegas: leer qué "Will install". Para vulns en transitivas, atajar
con `overrides` en package.json (p.ej. {"uuid":">=11.1.1","postcss":">=8.5.10"})
forzando solo la transitiva a versión parcheada, sin tocar la dep directa.
`npm audit fix` SIN --force sí es seguro (solo bumps de lockfile compatibles).

Ver [[verificar-modelos-anthropic-vigentes-via-get-v1-models]]
