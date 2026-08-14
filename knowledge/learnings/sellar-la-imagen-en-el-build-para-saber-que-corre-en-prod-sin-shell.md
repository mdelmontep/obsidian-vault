---
title: sellar la imagen en el build para saber qué corre en prod sin shell
date: 2026-08-14
source: claude-code-session
tags: [docker, dokploy, deploy, verificacion]
---
Verificar un deploy **por contenido** solía exigir SSH al host (mirar el log del deploy, `grep` dentro
del contenedor). Cuando el SSH cae —cinco veces seguidas en AGH, puerto cerrado desde esa red— no
queda ninguna vía, y un `200` de la app **no prueba nada**: es el síntoma exacto de servir la imagen
vieja con el clone roto.

**Patrón:** un `RUN` en el `Dockerfile`, **después del `COPY` y antes del `CMD`**, hashea el contenido
que acaba de entrar en la imagen y lo deja en un fichero; un endpoint HTTP lo sirve. Comparas el
digest de prod con el que calculas en local sobre un árbol limpio: si coinciden, el deploy llegó.

**Lo que lo hace funcionar, y es contraintuitivo:** el runtime **no puede mirar `process.env`**. Una
env var del panel (Dokploy) es de *runtime* y **sobrevive a la imagen**, así que bastaría teclear un
SHA para que una imagen vieja cantase el commit nuevo — el fallo que se quiere detectar. Tampoco vale
leer `git` en runtime (el `.dockerignore` excluye `.git`). El valor tiene que salir del **build**.

Dos gotchas medidos:
- **`docker info` → DOWN no significa daemon parado**: con colima puede ser el *contexto*
  (`DOCKER_HOST=unix://$HOME/.colima/default/docker.sock`). Casi deja sin construir una imagen.
- **Los patrones del `.dockerignore` van anclados a la raíz**: `node_modules` **no** tapa
  `sub/node_modules`.

La lista de qué sellar **no se escribe a mano**: se deriva del `.dockerignore`, o diverge el mismo día.

**Usado dos veces el 14-ago, y la 2ª es mejor evidencia que la 1ª:** ahí el digest **cambió solo** (una
PR del tren tocaba contenido sellado) *y* coincidió con el local — que se mueva **y** case vale más que
un control artificial. Dos corolarios al leerlo: un commit **docs-only no mueve el digest**, y eso es
correcto por diseño, no un deploy que falta; y el `builtAt` que acompaña al sello **no sirve para fechar
deploys** — salió a ~10 s del merge las dos veces, cifra plausible solo con la capa del `npm ci`
cacheada, que no lo está si el diff toca `package.json`.
