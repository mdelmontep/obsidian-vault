---
title: un hook que deniega con la receta ahorra la confirmación humana
date: 2026-10-16
source: facturaia (hook gate-remoto-guard, 15-oct)
tags: [claude-code, hooks, harness, permisos]
---
Un PreToolUse que responde `ask` ante una forma «rara» de un comando para a Manuel en CADA llamada
(«gate-remoto va en segundo plano», 20 diálogos en una tarde de trenes). El modelo no aprende nada
de un `ask`: solo espera.

Patrón que funciona:
- Forma canónica (`cd X && ~/bin/gate-remoto -- npm|npx|node …`) → `allow` explícito.
- Forma no canónica → `deny` con el comando correcto LITERAL en el mensaje: el modelo lo reescribe
  en la siguiente llamada sin humano.
- `ask` solo para lo que de verdad pide juicio humano (irreversible, prod).

Al parchear un hook, probar los dos caminos: uno que DEBE pasar y uno que DEBE denegar.
Ver [[semaforo-que-envuelve-un-comando-que-vuelve-a-pedirle-slot-se-interbloquea]] · [[claude-code-harness]]
