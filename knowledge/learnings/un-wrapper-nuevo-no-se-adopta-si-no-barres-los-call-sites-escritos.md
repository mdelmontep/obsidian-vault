---
title: un wrapper nuevo no se adopta si no barres los call-sites escritos
date: 2026-08-03
source: claude-code-session
tags: [claude-code, harness, secretos, adopcion, 1password]
---
El 3-ago monté `opsa` (wrapper de `op` con service account) para quitar el Touch ID. Funcionaba —
`opsa whoami` daba `SERVICE_ACCOUNT` a la primera— y aun así seguía pidiendo sign in **todo el día**.
Causa: nadie lo invocaba. Los permisos de `settings.json` decían `Bash(op read:*)`, los runbooks,
los agents y **15 memories** decían `op`. El agente ejecuta lo que está ESCRITO, no lo que existe en
el PATH.

Patrón: crear la herramienta es el 20% del trabajo; el 80% es barrer los call-sites que la nombran.
La herramienta nueva compite contra el hábito escrito, y el hábito escrito gana siempre.

Checklist al introducir un wrapper/alias/binario que sustituye a otro:
1. `grep -rn` del comando VIEJO en permisos, hooks, skills, agents, commands, runbooks y memories.
   Excluir copias (`worktrees/`, `.next/standalone/`, backups) para no editar fantasmas.
2. Reescribir cada uno, y **verificar el alcance antes** — el sustituto rara vez cubre el 100% del
   original (aquí: solo lectura, y ciego a las bóvedas personales).
3. Hook `PreToolUse` que bloquee el viejo y remita al nuevo, con las excepciones donde el nuevo NO
   llega. Sin hook, en un mes vuelve — los modelos leen, los hooks bloquean.
4. La memoria/doc que anuncia la herramienta **no basta**: solo carga en el cwd donde se escribió.

Ver [[service-account-de-1password-exige-vault-explicito-en-item-get]] ·
[[op-read-secreto-nunca-en-comando-bash-ni-desde-memoria]]
