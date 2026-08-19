---
title: un gobernador de CPU ciego a los hooks de git regula el 5 % y multa a quien lo respeta
date: 2026-08-20
source: facturaia
tags: [harness, gates, hooks, cpu, sesiones-paralelas]
---
Un semáforo que serializa comandos pesados interceptándolos en el agente (`PreToolUse` sobre
`npm run build|typecheck|lint`) **no ve el trabajo que ocurre DENTRO de los hooks de git**: el
`pre-commit` corre lint y typecheck, el `pre-push` corre build, y desde fuera todo eso es un
`git commit`, que no matchea el patrón. Si ahí está el 95 % del gasto real —y en un repo con hooks
serios lo está—, el gobernador regula lo que sobra y penaliza justo a quien lo llama directo.

Medido (5 sesiones, 10 cores): cuatro `tsc --noEmit` simultáneos, >40 min cada uno, con el dashboard
diciendo `0/3 corriendo`. Y el swap a 24 GB sobre 16 GB de RAM, con los builds a **0 % de CPU y RSS 0**:
no lentos, congelados esperando páginas. Matar uno desatascó a otro que llevaba 2h30.

Dos correcciones que cambian el arreglo:
- El techo del watchdog es de **EJECUCIÓN**, no de cola: mata con el slot ya tomado. Calibrado para
  una máquina sin contención, garantiza la muerte de quien sí pasa por el gate cuando la contención la
  generan procesos que el gate no gobierna.
- «Swap libre» es mala métrica en macOS: el total es elástico (24 → 16 → 7 GB según demanda). La señal
  útil es **cuántos builds compiten**.

Fix: que los hooks pidan slot, con un `gate_run` que sea NO-OP si el semáforo no está instalado (otra
máquina, CI, un clon sin `~/.claude`) para no meterle dependencias al hook. Y traducir el 143 del
watchdog: decir «errores de TypeScript» sobre un typecheck que ni terminó manda al autor a buscar un
error que no existe. Ver [[el-arnes-se-mide-a-si-mismo]] · [[cpu-contencion-multisesion-falso-positivo-ui-atascada]] · [[facturaia]].
