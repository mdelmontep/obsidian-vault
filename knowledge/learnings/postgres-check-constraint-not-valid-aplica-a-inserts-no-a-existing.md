---
title: Postgres CHECK NOT VALID solo ignora filas existentes — INSERTs nuevos sí lo evalúan
date: 2026-05-18
source: claude-code-session
tags: [postgres, sql, migration, gotcha]
---

`ALTER TABLE ADD CONSTRAINT chk CHECK (...) NOT VALID` NO significa "constraint desactivado". Solo evita escaneo de filas existentes al crear (útil para no bloquear migración en tablas grandes). INSERT/UPDATE nuevos sí evalúan el CHECK normalmente.

Gotcha: si la lógica del CHECK tiene un agujero (caso `OR` que cubre todo accidentalmente), NOT VALID no avisa.

Validación post-mig opcional: `ALTER TABLE t VALIDATE CONSTRAINT chk;`

Aprendizaje: revisa lógica del CHECK aparte del flag NOT VALID.
