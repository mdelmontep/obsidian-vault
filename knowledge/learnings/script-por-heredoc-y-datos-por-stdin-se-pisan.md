---
title: pasar el script por heredoc y los datos por pipe deja el intérprete leyendo un stdin vacío
date: 2026-08-09
source: claude-code-session
tags: [bash, python, shell, gotcha, hooks]
---
Dentro de un hook:

```bash
clas="$(printf '%s' "$dirty" | python3 - "$H" 60 <<'PY'
...  s = sys.stdin.read()   # ← vacío SIEMPRE
PY
)"
```

`python3 -` lee el **programa** de stdin, y el heredoc es la última redirección, así que gana: el
pipe se descarta y `sys.stdin.read()` devuelve cadena vacía. Sin excepción, sin error: cero filas
procesadas, salida vacía.

Lo que lo hace caro es que el fallo se confunde con el camino de contingencia. Mi hook fallaba
CERRADO cuando el clasificador no decía nada, así que el síntoma fue «sigue bloqueando como antes»
y parecía que el arreglo no funcionaba, no que no se estuviera ejecutando.

Fix: los datos NO por stdin. Por variable de entorno (`ENTRADA="$datos" python3 - ... <<'PY'`, y
`os.environ["ENTRADA"]`), por argv si son cortos, o el script a fichero y stdin libre. Y al probar un
camino de contingencia, comprueba que el camino PRINCIPAL corrió: si «falla cerrado» y «no se ejecutó»
dan la misma salida, no has verificado nada. Ver
[[hook-sobre-recurso-compartido-bloquea-a-quien-cierra-no-a-quien-ensucia]].
