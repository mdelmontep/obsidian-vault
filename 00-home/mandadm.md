---
title: MandaDM
date: 2026-09-05
updated: 2026-09-05
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

## Estado (5-sep)

- 🟢 **Fase A · Preparar**: A1 (verificación de negocio, Cabamatica Soluciones en la cartera
  AgentesiaLab), A4 (app `mandadm` en Meta con Instagram Login), A5 (los tres permisos
  `instagram_business_*`) y A8 hechas. Credenciales en 1Password, bóveda `MandaDM`, ítem «Meta app mandadm».
- 🟢 **Horda corrida de punta a punta, cuatro rondas**: fases B a G construidas, medidas y en verde
  en [PR #1](https://github.com/AgentesIA-MAdrid/mandadm/pull/1) (**sin mergear**, es para leer).
  72 ficheros de test, 712 tests, `./scripts/gate.sh` `0 0 0 0`. 14 decisiones de tribunal en
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
- 🔴 **A6 es el cuello de botella**: que el cliente acepte la invitación de tester desbloquea la
  comprobación de veintitantas tareas. Sin cliente elegido todavía.
- 🟡 **A10 · desplegar es ahora el cuello de botella real** (5-sep, `ADR-004` en el repo): va al
  **Dokploy del CRM** (`dokploymanu.tecnocloud.es`, host `185.99.186.76`, credenciales en 1Password
  `TUCRMIA`), **no** al VPS de TuFacturaIA que la horda había escrito por su cuenta sin que nadie lo
  decidiera. El DNS deja de bloquear: ese host ya sirve certificado real sobre `sslip.io`, así que
  `mandadm.185.99.186.76.sslip.io` sirve para publicar la app. Las variables **a mano en el panel**:
  la API de Dokploy reemplaza el bloque entero y recargar Traefik tira el CRM con él.
- ⚪ **A7 ya no espera textos**: `MARCADORES_PENDIENTES` está vacía —NIF, domicilio y proveedor de
  hosting (Tecnocloud, encargado del tratamiento) escritos y verificados por test—. Solo falta
  desplegar, o sea A10.
- ⚠️ **B1 y B3 no se cierran solo con A6**: B1 necesita capturar un POST real (ninguna página dice con
  qué secreto firma Meta `X-Hub-Signature-256`); B3 pide un GET de `subscribed_apps` que Meta no documenta.

## Tuyo

- **A10 · encender el despliegue**: en el panel de Dokploy, proyecto `mandadm` y las trece variables
  a mano. Es lo único que abre la URL pública, y con ella A7, B1 y B3.
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

Postgres y límites:
- [[un-revoke-sobre-un-esquema-custom-no-revoca-nada]] · [[un-tope-por-hora-y-otro-por-segundo-miden-ejes-distintos]]
- [[guarda-de-monotonia-entre-dos-relojes-distintos]] — el `$at > last_event_at` comparaba el reloj
  de Meta con el del worker; dejaba la conversación abierta con el enlace ya enviado, para siempre.

Meta:
- [[los-fixtures-oficiales-de-meta-contradicen-la-descripcion-del-campo]] (incluye el error plano de
  `refresh_access_token` y el secreto sin documentar de `X-Hub-Signature-256`)
- [[graph-api-de-instagram-exige-pagina-vinculada-y-la-concesion-es-pegajosa]] (actualizada: Instagram Login no exige página)

De la sesión anterior:
- [[cuenta-de-servicio-de-1password-no-ve-bovedas-creadas-despues]] · [[security-add-generic-password-interactivo-trunca-el-secreto-a-128]]
- [[un-goal-activo-salta-la-parada-de-ok-del-usuario]]
- [[dig-ns-vacio-no-significa-que-el-dominio-este-libre]] (whois también miente) · artifacts que desaparecen: `inbox/tablero-artefacto-se-borra-solo`
