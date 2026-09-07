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

- **También los CAMPOS con tilde** («Token de larga duración», caso Kommo 3-sep-2026): `opsa read "op://…/<campo>"` falla igual → `opsa item get <id> --vault <bóveda> --format json` y sacar el campo por `label` con python, sin imprimir el valor.

- **Y las BÓVEDAS con `/` en el nombre** (caso `Dani/Borja/Manu`, 7-sep-2026): la barra es el
  separador de la ruta `op://`, así que la referencia se parte y **devuelve vacío sin error** —
  el modo de fallo peor de los tres, porque un `len($PW)` de 0 pasa por «no está» en vez de por
  «mal escrito». Mismo fix: `opsa item get <id> --vault "Dani/Borja/Manu" --fields label=password --reveal --format json`.

Corolario al escribir runbooks: si un comando `op item get` no lleva `--vault`, funciona hoy con
huella y reventará el día que se automatice. Ponerlo siempre.

Alcance del service account: desde el **5-sep-2026** es `Claude` (sustituye a `claude-code-mac`),
**18 bóvedas** de `agentesialab.1password.eu` incluida MandaDM, y con permiso de **lectura y
escritura** — la anterior era solo lectura. Caducidad real en `OPSA_TOKEN_EXPIRES` dentro de
`~/.local/bin/opsa`, no de memoria. Sigue sin ver `my.1password.com` ni los vaults built-in
`Private`/`Employee`/`Shared`, y **escribir** (`item create/edit/delete`) sigue siendo `op`.

Ver [[un-wrapper-nuevo-no-se-adopta-si-no-barres-los-call-sites-escritos]]
