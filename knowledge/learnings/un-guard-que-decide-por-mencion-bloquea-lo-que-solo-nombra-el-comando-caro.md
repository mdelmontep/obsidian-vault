---
title: un guard que decide por mención bloquea lo que solo NOMBRA el comando caro
date: 2026-08-14
source: claude-code-session agh-iberica
tags: [hooks, harness, guards, metodo]
---
Un `PreToolUse(Bash)` que protegía una corrida cara buscaba el nombre del script **en cualquier
posición del comando**. Resultado: rechazaba un `git commit -m "…<script>…"`, que no gasta un
céntimo. Un guard que salta cuando no debe **se aprende a rodear** (con `-F`, con otro wording), y el
día que sí ibas a gastar el reflejo ya está entrenado.

**Fix:** tokenizar el comando **respetando las comillas** (`shlex.split`, así el cuerpo de un `-m
"…"` es UN token) y contar solo lo que aparece **en posición de comando**: al principio, o tras
`&&`, `||`, `;`, `|`, saltando asignaciones de entorno (`VAR=x cmd`). Límite aceptable y declarado:
un separador pegado sin espacios (`a&&b`) no se parte.

Dos reglas que salieron con él:
- **Un guard global no debe citar una cifra que vive en un repo.** Si el dato tiene fuente única en
  el proyecto, el hook la **lee** del repo que está guardando y, si no la encuentra, remite a ella —
  copiarla en el hook es una copia más que ningún candado del repo puede vigilar.
- **Su suite en verde no basta: probarlo en el camino real.** Los casos que valen son los que
  **discriminan** (mencionar no bloquea / ejecutar sí), no los que pasan trivialmente.

Ver [[un-guard-que-detecta-por-contenido-caza-los-comentarios-que-lo-niegan]] ·
[[una-lista-en-un-comentario-no-protege-busca-una-invariante-cruzada]].
