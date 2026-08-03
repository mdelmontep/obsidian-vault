---
title: una guarda que mata el proceso deja huérfano lo que ya está en vuelo
date: 2026-08-03
source: claude-code-session
tags: [seguridad, fail-closed, produccion, trading]
---

Añadir un `SystemExit` al arranque para impedir una acción peligrosa parece fail-closed y no
lo es del todo: mata también el **plano de control**. En cryptobruj, abortar si falta
`LIVE_CONFIRMED` habría dejado el bot en crash-loop (`restart: unless-stopped`) con una
posición real abierta: sin watchdog del SL, sin kill por drawdown y sin panel para cerrar a
mano. El SL vivía en el exchange y aguantaba, pero la supervisión desaparecía justo con
dinero expuesto. Y el disparador no tiene que ser un deploy: vale un OOM o un reboot.

Regla: **fail-closed sobre INICIAR lo peligroso, nunca sobre SUPERVISAR lo que ya está en
vuelo.** La guarda va en el cuello por el que pasa la acción (aquí `place_order`), no en el
arranque; el proceso sigue vivo gestionando salidas, avisa, y expone el estado degradado
(`/health` → `entries_blocked: true`) para que sea visible desde fuera.

Corolario: una variable nueva que el panel de producción todavía no tiene convierte el
siguiente redeploy en crash-loop. Comprobar qué falta en el entorno real ANTES de mergear.

Ver [[no-hardcodear-el-modo-lo-hace-inverificable-desde-el-repo]] · [[cryptobruj]]
