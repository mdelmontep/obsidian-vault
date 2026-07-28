---
title: brew expone python3.12 pero no python3, y el del sistema es 3.9
date: 2026-07-28
source: claude-code-session
tags: [macos, python, homebrew, claude-code, gotcha]
---

`brew install python@3.12` deja `/opt/homebrew/bin/python3.12` pero **no** crea
`python3`. El `python3` que resuelve el PATH sigue siendo `/usr/bin/python3` =
**3.9.6**. Cualquier tool que exija ≥3.10 falla aunque el intérprete correcto
esté instalado, y el mensaje engaña ("Python 3.10+ required. Tried python3, python").

Diagnóstico: `which -a python3` (una sola entrada, `/usr/bin`) +
`ls /opt/homebrew/bin | grep python`.

Fix sin tocar el `python3` del sistema: fijar la ruta por env var del propio
tool, en `~/.claude/settings.json` → `env`, no en el `.zshrc`:

```json
"env": { "CLAUDE_SEO_PYTHON": "/opt/homebrew/opt/python@3.12/bin/python3.12" }
```

Alternativa global (más invasiva): symlink en `~/.local/bin/python3`.

Ver [[npx-skills-add-rompe-packs-con-instalador-propio]]
