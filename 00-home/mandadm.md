---
title: MandaDM
date: 2026-09-05
updated: 2026-09-10
tags: [proyecto, propio, instagram, meta, nextjs, supabase]
---

# MandaDM

Automatizaciones de Instagram para clientes sobre la **API oficial de Meta**: responder a comentarios
con un DM, respuestas a historias, campañas y captura de email. Lo que hace Manychat, sin Manychat:
no tiene ningún acuerdo especial, todo está en la API pública (12 afirmaciones verificadas contra la
documentación oficial, en el repo).

Repo `~/Projects/mandadm` → `github.com/AgentesIA-MAdrid/mandadm` (privado). **Fuente de verdad del
plan: `docs/plan/ESTADO.md`** (fases A-G, cada tarea con su «hecho cuando»). `docs/plan/API-META-VERIFICADA.md`
es la única referencia de endpoints y límites; `docs/decisions/ADR-001` fija la vía.

## Estado (10-sep)

- 🟢 **DESPLEGADO (10-sep, `d4788ce`)** en `https://mandadm.185.99.186.76.sslip.io` con certificado
  real de Let's Encrypt. Seis contenedores sanos en `/opt/mandadm` del host `185.99.186.76`
  (`db` · `auth` · `rest` · `kong` · `web` · `worker`), **compose a pelo por SSH, NO en el panel de
  Dokploy** — no hay API key en ninguna bóveda que `opsa` alcance. Supabase autoalojado y recortado
  (postgres + gotrue + postgrest + kong; sin realtime/storage/studio/analytics), `ADR-005` en el repo.
  TuCRMIA comprobado intacto; Traefik descubre las etiquetas solo, nunca hizo falta recargarlo.
  **A10 hecha**, con los tres «hecho cuando» medidos. B1 (webhook) verificado contra el despliegue:
  token correcto → 200 con el challenge exacto, token falso → 403, HMAC válido → 200, firma falsa → 403.
- 🔴 **La migración revocaba permisos que en producción no existían.** Supabase concede `arwdDxt` a
  `anon`, `authenticated` y `service_role` en toda tabla nueva de `public` vía `alter default
  privileges`; medido antes del arreglo: `authenticated` podía UPDATE de `ig_user_id`, y una tabla
  como `_migrations` nacía con `anon=arwdDxt` **y sin RLS** — la anon key pública podía leer y borrar
  el libro de migraciones. Arreglado con `deploy/autohospedado/init/zz-mandadm.sh` (corre el último
  por orden alfabético, como `supabase_admin`). Después: 0 grants de `anon` en `public` y
  `GET /rest/v1/accounts` con la anon key → **401 `42501`**. El gate del repo no puede cazarlo nunca.
  → [[un-postgres-desechable-no-mide-lo-que-concede-la-plataforma]]
- 🟢 **Fase A · Preparar**: A1 (verificación de negocio, Cabamatica Soluciones en la cartera
  AgentesiaLab), A4 (app `mandadm` en Meta con Instagram Login), A5 (los tres permisos
  `instagram_business_*`) y A8 hechas. Credenciales en 1Password, bóveda `MandaDM`, ítem «Meta app mandadm».
- 🟢 **Horda corrida de punta a punta, cuatro rondas**: fases B a G construidas, medidas y en verde
  en [PR #1](https://github.com/AgentesIA-MAdrid/mandadm/pull/1) (**sin mergear**, es para leer).
  72 ficheros de test, 713 tests, `./scripts/gate.sh` `0 0 0 0`. 14 decisiones de tribunal en
  `ADR-003`, 18 páginas oficiales de Meta en `docs/meta/`, 31 fixtures.
  Tracker: `artifact/0fabd758-758e-48d1-9426-2955e40dc709`.
  - Ronda 2 (composición): la guarda de la ventana de 24 h era código muerto, el flujo comentario→DM
    moría tras el private reply, y `account_members` permitía escalar a `owner` desde el navegador.
  - Ronda 3: tests que **exigían** el defecto — uno se ponía rojo al terminar A7. `quick_replies`
    fuera del panel (el worker no sabe entregarlo distinto de texto).
  - Ronda 4: el intermitente del worker era un bug de producción, no un flake. C5 construida.
  - Barrido de mutación **9 de 9** contra Postgres real: ninguna protección dio «sin víctima».
- ⚪ **Casi todo queda en `doing`, no en `done`**, y es correcto: el «hecho cuando» de cada tarea de
  B a G está redactado contra Instagram real. Excepción: **B6** (cola y worker), la única de la fase B
  que no necesita Instagram.
- 🟢 **Cuatro tareas salieron de `doing` (6-sep, `58d70dc`)**: C1, E2, F1 y F7 estaban terminadas y
  medidas, escondidas tras una nota copiada («exige Instagram real») que en ese fichero casaba **nueve
  veces**. Solo C4 tenía motivo real, y era otro. → [[una-razon-generica-repetida-en-cada-tarea-no-justifica-ninguna]]
- 🟢 **Bug de caducidad de token arreglado** (`6dccc70`): un token ya vencido se clasificaba «por
  caducar» y avisaba con días negativos; ahora cae en `expired` (el enum ya lo tenía) y el aviso lo
  dice. Mutante muerto en vitest.
- ⚠️ **Los dos commits de arriba NO están pusheados** — `origin/horda/2026-09-05` sigue en `6c5a9e4`.
- 🟡 **`MetaGateway` sin commitear, a propósito**: implementa `fetchCommentTimestamp` con
  `GET /{ig-comment-id}?fields=timestamp`, y ese endpoint **no está en ninguna fuente oficial** — la
  cita que lo respaldaba (`docs/meta/comment-moderation.md:26`) es parte del ejemplo de respuesta de
  `GET /<IG_MEDIA_ID>/comments`, que es el que sí está documentado. Decidir antes de seguir: cambiar
  al documentado, o dejarlo y verificarlo con una llamada real cuando haya cuenta. Arreglar lo demás
  que encontró la revisión (fail-open silencioso del plazo de 7 días, lectura antes de la guarda
  `accountConnected`, dos tests que no muerden) antes de decidir es trabajo tirado.
- 🔴 **A6 es el cuello de botella**: que el cliente acepte la invitación de tester desbloquea la
  comprobación de veintitantas tareas. Sin cliente elegido todavía.
- ⚪ **A10 · cerrada** (`ADR-004` eligió el Dokploy del CRM, `ADR-005` el Supabase autoalojado). El
  dominio quedó en `mandadm.185.99.186.76.sslip.io`; a Meta le vale cualquier HTTPS. Las catorce
  variables no pasaron por el panel: viven en `/opt/mandadm/.env` (600, root), leídas de 1Password.
- ⚪ **A7 ya no espera textos**: `MARCADORES_PENDIENTES` está vacía —NIF, domicilio y proveedor de
  hosting (Tecnocloud, encargado del tratamiento) escritos y verificados por test—. Ya responden 200 en el dominio de arriba; sigue en `doing`
  solo porque falta registrarlas en el panel de la app de Meta.
- ⚠️ **B1 y B3 no se cierran solo con A6**: B1 necesita capturar un POST real (ninguna página dice con
  qué secreto firma Meta `X-Hub-Signature-256`); B3 pide un GET de `subscribed_apps` que Meta no documenta.

## Tuyo

- **Decidir la ruta raíz `/`**: hoy da 404 (no existe `app/page.tsx`, solo `/app` y `/entrar`).
  Tres opciones: 1) redirigir a `/app` (mi recomendación), 2) redirigir a `/entrar`, 3) landing de
  producto. Con la elección lo dejo hecho y desplegado.
- **`ALERTS_EMAIL_FROM/TO/API_KEY` están VACÍAS**: ningún aviso del worker llega a un humano —ni token
  caducado, ni envíos fallando, ni worker parado—. Verificar `agentesia.madrid` en Resend, o reutilizar
  una de las dos keys de FacturAIA.
- **El volumen `mandadm-db` no está en ningún backup.**
- **Adoptar el stack en el panel de Dokploy** (hoy es compose a pelo en `/opt/mandadm`): hace falta una
  API key de Dokploy, que no existe en ninguna bóveda que `opsa` alcance.
- Decidir **qué rama es la buena**: `horda/2026-09-05` (lo desplegado) o `main` con la PR #1 mergeada.
- **Elegir cliente tester y que acepte la invitación (A6)** — la acción de mayor retorno con diferencia.
- **Decidir si se conecta la cuenta de Instagram de TuFacturaIA** para las pruebas de B a G. La horda
  lo dio por hecho y no lo era; lo que hay que sopesar es que el webhook escribe en `events` **todo**
  lo que entra, así que los DMs de leads reales acabarían en la base de MandaDM.
- **Leer la PR #1** y decidir si se mergea. No la he mergeado.
- App Review con los 3 screencasts (fase D); el guion ya está escrito en el repo.
- Nombre: OEPM clases 38/42 para «manda», `@mandadm` en Instagram y `mandadm.com` (RDAP, no whois).
- `OPSA_TOKEN_EXPIRES` en `~/.local/bin/opsa` con la caducidad del token de la cuenta `Claude`.

## Decisiones (ADR-001 en el repo)

Instagram Login sin página de Facebook · primer cliente como tester · App Review de los tres permisos
de una vez · n8n + Supabase para un cliente, backend propio al segundo (lo decide el tribunal en ADR-002).

## Learnings nacidos aquí

Método y arnés (transversales, salieron de la horda):
- [[una-pieza-con-su-suite-en-verde-que-el-sistema-no-llama]] — la lección grande: seis defectos, una
  sola forma. El candado tiene que **descubrir**, no enumerar.
- [[un-build-con-directorio-de-salida-fijo-no-aguanta-agentes-en-paralelo]] · [[un-agente-que-trae-documentacion-transcribe-el-marcador-como-valor]]
- [[una-regla-sin-fuente-cuyo-rechazo-es-irrecuperable-falla-abriendo]] — las cuatro preguntas antes
  de añadir una comprobación defensiva.
- [[test-verde-puede-codificar-el-bug-como-esperado]] — ampliada aquí con la forma peor: el test que
  **exige** el defecto (`expect(pendientes.length).toBeGreaterThan(0)`) y la lista de verificación
  derivada de lo que verifica.
- [[el-barrido-que-salta-los-tests-relevantes-dice-sin-victima]] — un «SIN VÍCTIMA» con skips no es
  cobertura ausente, es medición ausente.
- [[el-agotamiento-de-un-pool-se-disfraza-de-lentitud-no-de-error]] — dos rojos del mismo gate con
  conjuntos distintos son no-determinismo; `pg.Pool` encola en vez de fallar.

Del cierre del 5-sep, ya con la horda parada:
- [[la-suposicion-de-un-agente-escrita-en-indicativo-se-lee-como-decision]] — el servidor y la cuenta
  de pruebas: dos frases de agente que el plan entero citaba como decididas.
- [[una-funcion-de-alcance-global-hace-que-dos-ficheros-de-test-se-cuenten-entre-si]] — el barrido de
  alertas, correcto en producción, contaminando dos ficheros que corren en paralelo sobre un Postgres.
- [[un-mutante-con-victima-puede-haber-muerto-en-otra-etapa-del-gate]] — «con víctima» tampoco basta
  si no miras en qué etapa se puso rojo.
- [[una-busqueda-cortada-por-timeout-no-prueba-una-ausencia]] (6-sep) — afirmé una ausencia a otra
  sesión con un `grep` que el timeout había matado; el dato llevaba un mes en un inventario del repo.
- [[un-commit-de-agente-con-un-hecho-falso-se-barre-entero]] (6-sep) — `af1ed10` metió CUATRO datos que
  nadie decidió, incluido el dominio del criterio de aprobado de A10. Se barren de golpe, no uno a uno.
- [[un-200-no-prueba-que-la-pagina-citada-exista]] — en `developers.facebook.com`, `/documentation/<basura>`
  devuelve 200 siempre; así se colaron dos ficheros de `docs/meta/` que eran reconstrucción.
- [[una-observacion-pierde-su-fuente-al-copiarse-a-un-documento-derivado]] — «el panel avisa de que…»
  llegó a las copias sin el «el panel avisa», y ahí empezó a leerse como documentación.
- [[una-razon-generica-repetida-en-cada-tarea-no-justifica-ninguna]] — la misma nota en nueve tareas no
  justifica ninguna; escondía cuatro ya terminadas.

Postgres y límites:
- [[un-revoke-sobre-un-esquema-custom-no-revoca-nada]] · [[un-tope-por-hora-y-otro-por-segundo-miden-ejes-distintos]]
- [[guarda-de-monotonia-entre-dos-relojes-distintos]] — el `$at > last_event_at` comparaba el reloj
  de Meta con el del worker; dejaba la conversación abierta con el enlace ya enviado, para siempre.

Meta:
- [[los-fixtures-oficiales-de-meta-contradicen-la-descripcion-del-campo]] (incluye el error plano de
  `refresh_access_token` y el secreto sin documentar de `X-Hub-Signature-256`)
- [[graph-api-de-instagram-exige-pagina-vinculada-y-la-concesion-es-pegajosa]] (actualizada: Instagram Login no exige página)

Del despliegue (10-sep):
- [[un-postgres-desechable-no-mide-lo-que-concede-la-plataforma]] — la grande: el gate no puede medir
  lo que concede la plataforma, solo lo que concede la migración.
- [[montar-la-carpeta-de-init-tapa-el-bootstrap-de-la-imagen]] — montar el directorio entero de
  `/docker-entrypoint-initdb.d` deja la imagen sin arrancar; se monta el fichero suelto.
- [[auth-uid-autohospedado-solo-lee-el-guc-legacy]] — con `PGRST_DB_USE_LEGACY_GUCS: "false"`,
  `auth.uid()` devuelve null y la RLS no filtra a nadie.
- [[un-runbook-nunca-ejecutado-da-por-rota-una-instalacion-correcta]] — tres afirmaciones falsas en
  `docs/deploy/supabase.md`, corregidas midiendo contra el despliegue real.

De la sesión anterior:
- [[cuenta-de-servicio-de-1password-no-ve-bovedas-creadas-despues]] · [[security-add-generic-password-interactivo-trunca-el-secreto-a-128]]
- [[un-goal-activo-salta-la-parada-de-ok-del-usuario]]
- [[dig-ns-vacio-no-significa-que-el-dominio-este-libre]] (whois también miente) · artifacts que desaparecen: `inbox/tablero-artefacto-se-borra-solo`
