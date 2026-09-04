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
- 🟢 **`/horda` lista**: `.claude/commands/horda.md` construye B-G con hasta 42 agentes bajo un solo
  `/goal`, sin preguntar: un tribunal de 3 agentes decide y lo deja en `ADR-003`. `/code-review` antes
  de la PR y `/obsidian-1` al cerrar. `docs/agents/` y las labels de triage ya existen.
- ⚪ **Sin cliente tester (A6)**: hasta Advanced Access solo funcionan cuentas con rol en la app.
- ⚪ **A7 antes de la fase B**: los webhooks solo llegan a una app publicada → política de privacidad
  y URL de borrado a nombre de Cabamatica Soluciones.

## Tuyo

- Lanzar la horda: sesión nueva en el repo, pegar el bloque «Lanzar de inicio a fin» de `horda.md`.
- Elegir cliente tester; publicar política y borrado (A7); App Review con 3 screencasts (fase D).
- Nombre: OEPM clases 38/42 para «manda», `@mandadm` en Instagram y `mandadm.com` (RDAP, no whois).
- `OPSA_TOKEN_EXPIRES` en `~/.local/bin/opsa` con la caducidad del token de la cuenta `Claude`.

## Decisiones (ADR-001 en el repo)

Instagram Login sin página de Facebook · primer cliente como tester · App Review de los tres permisos
de una vez · n8n + Supabase para un cliente, backend propio al segundo (lo decide el tribunal en ADR-002).

## Learnings nacidos aquí

- [[cuenta-de-servicio-de-1password-no-ve-bovedas-creadas-despues]] · [[security-add-generic-password-interactivo-trunca-el-secreto-a-128]]
- [[un-goal-activo-salta-la-parada-de-ok-del-usuario]]
- [[graph-api-de-instagram-exige-pagina-vinculada-y-la-concesion-es-pegajosa]] (actualizada: Instagram Login no exige página)
- [[dig-ns-vacio-no-significa-que-el-dominio-este-libre]] (whois también miente) · artifacts que desaparecen: `inbox/tablero-artefacto-se-borra-solo`
