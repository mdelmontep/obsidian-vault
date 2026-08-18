---
title: Aula
date: 2026-08-10
updated: 2026-08-18
tags: [proyecto, aprendizaje, nextjs, supabase, dokploy]
---

# Aula

Aula personal para aprender los sistemas propios (TuFacturaIA, TuCRMIA, AGH) y la terminología que
los rodea. **Las lecciones no existen hasta que se piden**: un runner de Claude las escribe abriendo
los repos de verdad, y cada afirmación va con su cita `fichero:línea`.

Repo `~/Projects/learn-agentesia` → **`github.com/mdelmontep/learn-agentesia` (privado)**, creado el 18-ago tras 43 commits sin copia fuera del disco. Next 16 + Supabase.
**Publicada** en `https://aula.185.99.186.76.sslip.io` · API en `aula-api.185.99.186.76.sslip.io`.

## Estado (18-ago)

- 🟢 **Publicada y funcionando** — Supabase autoalojado en `dokploymanu` (`/opt/aula/`), cuatro
  contenedores en vez de once. Contenido mudado con el dueño reescrito. HTTPS por `sslip.io`, sin
  tocar DNS. → [[supabase-selfhosted-cuatro-contenedores-y-seis-errores-enganosos]]
- 🟢 **Nivel reescrito: «desde la calle»** — las lecciones hablaban por encima. La causa no era el
  nivel sino el bloque «quién te lee» del prompt, que decía "sénior, eso NUNCA se explica".
  Ahora ninguna palabra técnica aparece antes de que se entienda la idea que nombra.
  → [[el-bloque-quien-te-lee-de-un-prompt-pisa-las-instrucciones-de-nivel]]
- 🟢 **«¿Esto qué es?»** — marcar texto en una lección y preguntarlo sin salir. Los términos del
  glosario salen subrayados y responden al instante; lo demás lo mira el runner en contexto y, si es
  vocabulario, entra en el glosario y de ahí al repaso.
- 🟢 **Sección «Memoria y recuperación»: 28 temas, publicada y escribiéndose (18-ago)** — de
  «guardar y encontrar son dos problemas distintos» a la memoria con hechos que caducan, más cinco
  temas de molde `sistema` sobre **el montaje real del vault**. Reescrita dos veces el mismo día por
  dos fallos propios que conviene no repetir:
  **(1) jerga en los títulos** — 11 de 19 la traían y el runner los copió: se publicó «Cuándo grep
  deja de buscar» para quien no sabe qué es grep. Ahora hay validador de entrada y de salida.
  → [[una-regla-que-solo-vive-en-el-prompt-se-cumple-casi-siempre]]
  **(2) temas escritos como fallo, no como concepto** — 7 de 19 contaban una avería sin haber
  enseñado el mecanismo. Faltaban además cuatro fundamentos delante (qué es un índice, qué significa
  relevante). El fallo ahora vive DENTRO de la lección de su mecanismo.
  → [[ADR-054-la-busqueda-del-vault-es-lexica-fts5-no-semantica-ni-grafo]]
- 🟢 **Los cinco moldes, por fin en uso (18-ago)** — `encolar-temario.mjs` fijaba `molde: 'concepto'`
  para todo, así que las cinco formas de enseñar eran una. Ahora el molde es propiedad del tema
  (`015_molde_por_tema.sql`): 13 concepto · 6 sistema · 4 práctica · 3 comparativa · 2 chuleta.
  → [[una-opcion-con-el-valor-fijo-en-quien-la-llama-no-existe-aunque-este-programada]]
- 🟢 **UX auditada con 5 agentes y arreglada (18-ago)** — el anillo de foco daba 2,5:1 con 3:1
  exigido y en los campos **empeoraba** al enfocar (2,02:1 contra ~19:1 en reposo); el subrayado de
  los h2 sólo marcaba la última línea; la columna de texto dejaba 428 px muertos; no existía
  `loading.tsx`, `error.tsx` ni `not-found.tsx`; y el buscador mandaba el curso entero al navegador
  (671 KB proyectados → 188 KB de techo). Desplegado y verificado en producción.
- ⚠️ **El runner es un SERVICIO, no un proceso** — LaunchAgent con `KeepAlive`. Matarlo lo reinicia;
  lanzarlo a mano lo duplica (hubo dos, uno con 28 h y código viejo). Pararlo de verdad:
  `launchctl unload ~/Library/LaunchAgents/es.agentesia.aula.runner-remoto.plist`. Log en
  `~/Library/Logs/aula-runner-remoto.log`.
  → [[matar-un-proceso-no-lo-para-si-detras-hay-un-servicio-que-lo-resucita]]
- ⚠️ **La petición del trabajo se congela al encolar** — al reescribir los temas, 16 de 20 trabajos
  pendientes seguían pidiendo la versión vieja. Antes de tocar el temario: retirar los desfasados y
  reencolar. → [[un-trabajo-en-cola-que-guarda-el-texto-y-no-la-referencia-nace-caducando]]
- 🟢 **Lección 2 escrita a mano (`content/0002-memoria-del-vault.html`)** — cómo funciona la memoria
  del vault, qué se descartó y por qué (Notion, BD, embeddings, RRF, GraphRAG) y cuatro variantes de
  uso. Sus citas `fichero:línea` las vigila un gate del vault (`scripts/verificar-citas.mjs`), que
  además sabe corregirlas. → [[una-cita-fichero-linea-caduca-en-silencio-el-gate-debe-corregirla]]
- 🟠 **Contenido en curso** — 10 lecciones escritas de 106 temas; el runner sigue encolando.
  Arranque: `npm run runner:remoto -- --vigilar` (trae la clave por SSH, no toca el disco del Mac).
- ⚪ **Sin correo**: no hay SMTP. El acceso es `npm run entrar:remoto`, enlace de un solo uso, y la
  sesión dura semanas. Conectar Resend está pendiente de decidir.

## Desplegar la app (NO es `docker compose up` a secas)

El stack lo gestiona **Dokploy** con el nombre de proyecto `aula-womwbl`, desde
`/etc/dokploy/compose/aula-womwbl/code/`. El `docker-compose.yml` de `/opt/aula/` es solo el origen
del que se **construye la imagen** (`image: aula-web`, sin `build:` en el de Dokploy).

Un `docker compose up -d --build` desde `/opt/aula` **levanta un stack gemelo** —compose toma el
nombre del proyecto del directorio— y deja dos veces las mismas rutas de Traefik. Pasó el 18-ago.
Ver [[docker-compose-up-sin-p-levanta-un-stack-gemelo-en-vez-de-recrear]]

Secuencia correcta, con vuelta atrás antes de nada:

```sh
scp <ficheros> root@185.99.186.76:/opt/aula/app/...      # puerto 5251
docker tag <id-imagen-viva> aula-web:antes-<fecha>       # red de seguridad
cd /opt/aula && docker compose build web                 # SOLO construye
cd /etc/dokploy/compose/aula-womwbl/code
docker compose -p aula-womwbl up -d --force-recreate --no-deps web
```

Y verificar el CSS servido, no que el contenedor arranque: `curl` la hoja de `/_next/static/` y
grepear un token nuevo. Última imagen de reserva: `aula-web:antes-20260818`.

**Dos bases de datos distintas**: `.env.local` apunta a la de casa; la publicada vive en el
servidor y su clave se lee por SSH (patrón de `scripts/runner-remoto.sh`). `npm run temario` y
`npm run seed` siembran **la de casa**. Sembrar en local y mirar la web publicada es no ver nada.

## Gates propios (los tres nacieron de un fallo real)

- `npm run enlaces` — recorre el sitio con sesión y falla si algo da 404, diciendo desde qué página.
  → [[dos-entidades-con-slug-propio-el-enlace-cruzado-no-lo-ve-ningun-test]]
- `npm run movil` — todas las pantallas en 393 px; falla si alguna no cabe.
  → [[overflow-wrap-anywhere-no-break-word-o-el-movil-encoge-el-texto]]
- `npm run gate` — lint + typecheck + tests + build, en el pre-commit.

## Trampas ya pisadas

- [[funcion-que-devuelve-tipo-compuesto-con-return-null-llega-como-fila-de-nulos]] — el runner
  petaba al vaciar la cola, que es lo que hace en modo vigilancia.
- [[filtrar-por-linea-un-volcado-con-valores-multilinea-borra-datos]] — la mudanza de contenido.
- [[redirigir-a-un-fichero-escribe-el-error-dentro-del-fichero]] — `gen:types` sin `DOCKER_HOST`.
- [[otra-sesion-con-pkill-mata-tu-servidor-y-parece-un-bug-del-producto]] — parar SIEMPRE por puerto.

El razonamiento largo de cada decisión (repaso espaciado, dominio, maestría que caduca, intercalado)
vive en `learn-agentesia/CLAUDE.md`, que es el sitio al que ir antes de tocar nada.
