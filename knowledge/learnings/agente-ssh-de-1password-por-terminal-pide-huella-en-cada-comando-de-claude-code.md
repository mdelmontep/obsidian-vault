---
title: agente ssh de 1password por terminal pide huella en cada comando de claude code
date: 2026-10-13
source: claude-harness (sesión SSH vía 1Password, Mac)
tags: [1password, ssh, claude-code]
---
- **Síntoma**: con el agente SSH de 1Password, cada `ssh` que lanza Claude Code pide Touch ID, aunque acabes de aprobar.
- **Causa**: Claude Code abre una shell nueva en cada llamada a Bash. Si el permiso se da por terminal (`Ask approval for each new` = *application and terminal session*), cada llamada cuenta como terminal nueva.
- **Fix**, en la app del Mac, Settings → Developer → SSH Agent:
  - `Ask approval for each new` = **application**.
  - `Remember key approval` = un tiempo fijo (4 h o 12 h) en vez de «until 1Password locks».
  - El aviso de huella trae la casilla «Approve for all applications».
- El permiso se pierde igualmente si 1Password se autobloquea (Settings → Security → Auto-lock).
- **No hay aprobación desde la app del móvil**: solo en el Mac, con Touch ID, contraseña o Apple Watch.
- Fuente: https://developer.1password.com/docs/ssh/agent/security
- Relacionado: [[1password]] (`opsa` para secretos, sin huella).
