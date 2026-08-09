---
title: el plan gratuito del proveedor se manifiesta como fallos dispersos, no como un aviso
date: 2026-08-09
source: claude-code-session
tags: [supabase, github, infra, backups]
---
Tres síntomas distintos en TuCRMIA resultaron ser el mismo hecho: la organización estaba en plan **free**.
CI de Actions parado por facturación, `password_hibp_enabled` devolviendo **402** al aplicarlo, y —el caro—
**ninguna copia de seguridad de la base de producción**, porque el free de Supabase no las incluye.

Ninguno de los tres se presenta como «estás en free». Se diagnostican por separado y se arreglan por
separado, y el de las copias no se manifiesta nunca hasta que hace falta restaurar.

Patrón: al auditar infraestructura, **preguntar por el plan de la cuenta antes que por la configuración**.
Una llamada: `GET api.supabase.com/v1/organizations/<slug>` → `"plan":"free"`. Y desconfiar del documento:
el `ESTADO.md` del proyecto llevaba una semana afirmando «Pro sin PITR» sobre una cuenta free — que no es
Pro sin PITR, es sin copias.

Relacionado: [[github-free-org-privado-sin-branch-protection-ni-rulesets]].
