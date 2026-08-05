---
title: el rojo de CI tiene dos causas y se distinguen contando pasos ejecutados
date: 2026-08-05
source: claude-code-session
tags: [ci, github-actions, metodo, verificacion]
---
«El CI está en rojo» no es una causa. Hay **al menos dos** y se tratan al revés, así que la regla del
equipo tiene que discriminarlas o no se puede aplicar. La discriminación más barata no es leer el log:
es **contar pasos ejecutados** por la API.

Caso real (agh-iberica, 5-ago), dos runs del mismo repo el mismo día:

| run | duración | pasos ejecutados | qué es |
|---|---|---|---|
| PR ajena | 3 m 8 s | **13** | corrió: 0 tests fallidos, y el exit 1 lo pone un `57P01` de teardown → flake conocido |
| mi PR | **11 s** | **0** | el job **nunca arrancó** (cuota/runner/permisos): no hay tests ni teardown que interpretar |

```bash
gh api repos/OWNER/REPO/actions/runs/<id>/jobs --jq '.jobs[]|"pasos: \([.steps[]]|length)"'
```

- **0 pasos** → rojo estructural. No dice nada del diff.
- **≥1 paso y 0 tests fallidos** → flake de infraestructura (teardown, BD efímera).
- **≥1 paso y ≥1 test fallido** → **rojo REAL**. Es el caso que una doc mal escrita hace ignorar.

Por qué importa: el mismo día, el equipo corrigió la doc que decía «Actions no arranca por billing,
ignora su rojo» —era falsa, corría en 3 m— y la sustituyó por «confirma que es el flake». Esa regla
**no se puede aplicar a un run de 11 s**: no hay log de tests que mirar. Una regla de clasificación que
no cubre uno de los casos empuja a mergear a ciegas exactamente igual que la que sustituyó.

Y el corolario que se lleva la señal gratis: si el CI monta la BD real, **es la única superficie que
ejecuta los tests que el gate local se autosalta sin base de datos**. Ignorar su rojo por costumbre es
tirar la única cobertura de esos tests.
