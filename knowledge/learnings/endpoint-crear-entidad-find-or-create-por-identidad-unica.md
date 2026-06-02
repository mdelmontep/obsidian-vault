---
title: endpoint que crea entidad con identidad única debe find-or-create, no insert ciego
date: 2026-06-02
source: claude-code-session
tags: [supabase, postgres, fiscal, endpoint, patron]
---

Endpoint que crea una entidad con `crear:true` (cliente, proveedor…) sobre una
tabla con índice único de identidad (NIF/CIF, normalmente `lower(nif)`) **no
debe hacer INSERT ciego**: si la identidad ya existe, viola el constraint y
devuelve un 500 opaco ("Failed to create client").

Patrón correcto:
1. Buscar por la identidad única primero (case-insensitive, igual que el índice).
2. Si existe **y el nombre coincide** (normalizado: trim+lower+espacios) → reutilizar.
3. Si existe **con otro nombre** → NO crear el documento. Devolver error tipado e
   informar al usuario: el DNI puede ser de otra persona ya registrada, y
   facturar a un nombre que no pidió es un error fiscal.

Caso real 2026-06-02 (TuFacturaIA voz/WhatsApp): el AI Agent manda `crear:true`
cuando no encuentra al cliente por NOMBRE, pero el NIF ya existía con otro nombre
→ dup key → factura fallaba con 500. Enlaza con [[upsert-atomico-rpc-vs-check-then-act-evita-lost-update]]
y [[cliente-react-bypasa-endpoint-canonico-bug-fiscal-latente]].
