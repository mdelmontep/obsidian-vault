---
title: npx skills add rompe packs de skills con instalador propio
date: 2026-07-28
source: claude-code-session
tags: [claude-code, skills, gotcha]
---

El CLI `skills` solo copia el subdirectorio de cada skill (`skills/<n>/`) del
repo. Si el pack lleva su runtime FUERA de esa carpeta —`scripts/`, `hooks/`,
`extensions/`, `schema/`, `requirements.txt` en la RAÍZ— te deja los markdown
actualizados y el pack sin ejecutar nada. Falla en silencio: la skill "existe".

Caso real: `npx skills add AgriciDaniel/claude-seo -g` sobre el pack SEO (25
skills) → borró `.venv`, `scripts/` y `hooks/` al sustituir el directorio por
un symlink a `~/.agents/skills/seo`.

Regla: antes de trackear una skill con el CLI, mirar si el repo trae
`install.sh` / `pyproject.toml` en la raíz. Si lo trae, usar SU instalador y
**no** meterla en `~/.agents/.skill-lock.json` (un `skills update` futuro la
vuelve a romper).

Ver [[brew-expone-python312-no-python3-y-el-python3-del-sistema-es-39]]
