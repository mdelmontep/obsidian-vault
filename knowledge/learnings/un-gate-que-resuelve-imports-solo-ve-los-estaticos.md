---
title: un gate que resuelve imports por AST sólo ve los estáticos de nivel superior
date: 2026-08-16
source: claude-code-session
tags: [gates, ast, typescript, seguridad]
---
Un ayudante que contesta «¿quién importa X?» recorriendo `sourceFile.statements` y filtrando
`ImportDeclaration` ve **sólo las importaciones estáticas de nivel superior**. Quedan fuera:

- `await import('x')` — es una `CallExpression` con `ImportKeyword`, dentro de una expresión.
- `require('x')` — una llamada corriente.
- Y las tres formas de atar el nombre: desestructuración, módulo entero, y **el import por efecto**,
  que no ata nada y aun así ejecuta el módulo (para «¿esto entra aquí?» la respuesta es que sí).

Medido en TuCRMIA: con `const { createClient } = await import('@supabase/supabase-js')` plantado en
una acción de servidor, el gate salía con **0** — un endpoint público fabricándose el cliente que
salta RLS, con lint y typecheck en verde.

Arreglar en el ayudante compartido, no en el gate que lo destapó: allí eran **seis** los gates que
preguntan lo mismo, y los seis heredan la cobertura de golpe.
