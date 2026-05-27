---
title: toggle/switch optimista que no comprueba el error de la mutación miente al usuario
date: 2026-05-27
source: claude-code-session
tags: [react, ux, supabase, facturaia]
---
Un switch que hace `setState(optimista)` y luego `await mutación` SIN comprobar el `error` → si la mutación falla (RLS deniega, red cae, rol sin permiso) la UI queda "movida" pero al recargar revierte. El usuario concluye que la acción "no funciona".

Caso TuFacturaIA: `toggleActivo` del catálogo (cliente Supabase directo, sin check de error) fue una de las causas de la queja "no se pueden quitar los productos" — junto a que el botón Eliminar estaba escondido tras expandir el ítem.

Fix: tras la mutación, si `error` → revertir el estado optimista + mostrar mensaje legible. Mejor aún: rutar la escritura por un endpoint (audit + validación + 409 legible) en vez de cliente directo. Relacionado: [[toggle-ux-only-no-contamina-storage-canonico-fiscal]].
