---
title: verificar un push mientras sigue en vuelo lee la punta vieja y parece un push rechazado
date: 2026-09-18
source: agh-iberica
tags: [git, verificacion, hooks, worktrees]
---
Con un pre-push que corre lint/typecheck, un `git push` tarda **minutos**. Si en ese hueco se
comprueba `git ls-remote origin <rama>` para «verificar por contenido», sale la punta **anterior** —
que es exactamente la firma de un push abortado por el hook. Medido el 18-sep en AGH: di por
fallidos dos push que entraron los dos, y el `git push origin HEAD:<rama>` siguiente respondió
`Everything up-to-date` contradiciendo mi propio `ls-remote` de un minuto antes.

- El veredicto se toma **cuando el push ha terminado**, no mientras corre: esperar a que el proceso
  muera (`pgrep -f "git push"`) y sólo entonces comparar `ls-remote` con `rev-parse HEAD`.
- No es lo mismo que [[pipe-a-tail-enmascara-el-exit-code-del-comando]] aunque se parezcan:
  aquél da un falso VERDE, éste un falso ROJO — y el falso rojo empuja a re-empujar, que es
  inofensivo, o a «arreglar» algo que no estaba roto, que no lo es.
- Corolario: `Everything up-to-date` con un `ls-remote` discrepante significa que el `ls-remote`
  es viejo, no que git mienta.

Relacionado: [[el-veredicto-de-un-merge-se-lee-del-estado-no-del-exit-code]].
