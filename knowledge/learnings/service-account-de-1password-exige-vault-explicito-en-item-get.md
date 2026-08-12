---
title: el service account de 1Password exige --vault explícito en item get
date: 2026-08-03
source: claude-code-session
tags: [1password, secretos, gotcha, claude-code]
---
Con un service account (`OP_SERVICE_ACCOUNT_TOKEN`, aquí vía el wrapper `opsa`), **`op item get`
falla si no le pasas `--vault`** — incluso buscando por ID de ítem, que con `op` interactivo basta.

El error es engañoso: dice que el ítem «isn't an item», que se lee como "no existe" o "no tengo
permiso", no como "te falta un flag". Perdí varias comprobaciones dando por inaccesibles ítems que
sí lo eran (`kknqs4zua3eje5drm6u25csaxu` en FacturAIA, `ssh AGH` en AGH Iberica).

- `opsa item get <id|título> --vault <bóveda>` → obligatorio.
- `opsa item list` y `opsa read "op://<bóveda>/<ítem>/<campo>"` → NO lo necesitan (la ruta `op://`
  ya lleva la bóveda dentro).
- **`op://` rechaza títulos con caracteres fuera de ASCII básico** («invalid character in secret
  reference», caso real 12-ago: `Dokploy API · tufacturaia` por el `·`) → usar el ID del ítem en la
  referencia: `opsa read "op://FacturAIA/<item-id>/credential"`.

Corolario al escribir runbooks: si un comando `op item get` no lleva `--vault`, funciona hoy con
huella y reventará el día que se automatice. Ponerlo siempre.

Alcance del service account `claude-code-mac`: 16 bóvedas de `agentesialab.1password.eu`, SOLO
lectura, **caduca 2026-11-01**. No ve `my.1password.com` ni los vaults built-in
`Private`/`Employee`/`Shared`.

Ver [[un-wrapper-nuevo-no-se-adopta-si-no-barres-los-call-sites-escritos]]
