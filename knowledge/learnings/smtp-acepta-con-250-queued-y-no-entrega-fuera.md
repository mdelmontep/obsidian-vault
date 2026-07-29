---
title: "250 queued" no es entrega — la sonda a una dirección inexistente lo distingue
date: 2026-07-28
source: claude-code-session
tags: [smtp, entregabilidad, email, clinica-zen]
---
`250 Ok: queued as XXXX` solo dice que el MTA **aceptó** el mensaje. La entrega al dominio
destino es posterior y asíncrona: si el servidor no lo saca, no hay error en ninguna parte —
ni excepción en el workflow, ni rebote, ni nada que mirar.

Prueba que lo separa en 3 minutos, sin depender de que nadie mire su bandeja:
1. **A un buzón del propio dominio** → aísla el MTA local de la salida externa.
2. **A una dirección INEXISTENTE de Gmail** → si el mensaje sale de verdad, Gmail devuelve
   `550 5.1.1` en segundos y el rebote aparece en el buzón del `MAIL FROM`. Sin rebote y sin
   entrega = no está saliendo. No molesta a ningún humano.
3. **`RCPT TO` contra el MX del destino** (`smtplib` + `docmd`, sin `DATA`) → confirma que el
   buzón destino existe antes de culpar al filtro de spam.

Caso real (Clínica Zen): interno entregado en 4 s, 3 externos encolados y desaparecidos,
sonda sin rebote → problema del hosting de correo, no del emisor. SPF/DKIM/FCrDNS/RBL
estaban todos limpios, así que revisarlos primero habría costado la tarde. Ver [[clinica-zen]]

**Corrección (29-jul)**: en el caso que originó esta nota el rebote SÍ existía — tardó 7 min
y cayó en la carpeta **Spam** del buzón, no en INBOX. Buscarlo a los 2 min y solo en INBOX
me hizo concluir lo contrario. La sonda es válida; lo que hay que hacer bien es **esperar
(hasta 15 min) y buscar en TODAS las carpetas**, Spam incluida. Un "no hay rebote" prematuro
es tan engañoso como no mirar.
