---
title: hot cache — archivo 2026-09-05
date: 2026-09-05
source: mandadm
tags: [stack, index, archivo]
---

# Hot cache — lo movido el 2026-09-05

Siete entradas cuyo learning tiene más de cuatro semanas (mayo-3 de agosto), sacadas de `Stack/hot.md`
para pagar la entrada nueva de `/goal` sin subir el presupuesto de arranque. Wikilinks intactos.

- **BSD `sed` ignora `\b` en silencio: sustituye cero veces y sale en verde** — un barrido de 52 referencias que no tocó ninguna, con exit code 0. Toda sustitución masiva se verifica volviendo a grepear el patrón viejo, o se hace con `re.subn` de Python, que devuelve el recuento. Ver [[macos-shell-bsd-sed-label-una-linea-y-while-read-ultima-linea]]
- **Arreglar un flake en UN fichero garantiza que vuelva por el hermano** — 7 de 9 nacieron sin el `pool.on("error")` copiado a mano; se cierra con un punto único que DISCRIMINE y un barrido que impida el noveno. Ver [[vitest-unhandledrejection-run-rojo-pese-a-0-fallos]]
- **Una ejecución en verde no prueba que el efecto ocurriera** — `success` = «no explotó»: mide que el nodo de efecto CORRIÓ (268 verdes, 0 envíos). Y el `else` de un `switch` sobre un valor de LLM tiene que AVISAR. Ver [[ejecucion-en-verde-no-prueba-el-efecto]] · [[el-else-de-un-clasificador-que-rellena-un-llm-debe-avisar-no-callar]]
- **Rama nueva desde `main` local sin fetch** — nace vieja y pisa lo mergeado: usar `origin/main`. Fichero reescrito >2 veces → merge, no rebase; sus rojos se clasifican. Ver [[rama-nueva-desde-un-main-local-sin-fetch-revierte-trabajo-ajeno]] · [[rama-que-reescribe-el-mismo-fichero-varias-veces-se-integra-con-merge]] · [[los-tests-rojos-que-hereda-un-merge-se-clasifican-uno-a-uno]]
- **`create or replace` con otra firma crea una sobrecarga y `db push` dice `Finished`** — el fix se despliega muerto. Verifica `pg_proc`: UNA fila. Ver [[postgres-rpc-firma-identica-create-replace]]
- **Un comentario que afirma una invariante es una deuda de test** — grepea la afirmación contra el código antes de fiarte; si nadie la comprueba, no es cierta. Ver [[un-comentario-que-afirma-una-invariante-es-una-deuda-de-test]]
- **Herramienta nueva sin barrer sus call-sites escritos NO se adopta** — el agente ejecuta lo ESCRITO (permisos, runbooks, memories), no lo del PATH. Ver [[un-wrapper-nuevo-no-se-adopta-si-no-barres-los-call-sites-escritos]]
