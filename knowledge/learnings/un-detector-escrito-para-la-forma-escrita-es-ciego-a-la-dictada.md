---
title: un detector escrito para la forma escrita del dato es ciego a la dictada
date: 2026-08-31
source: agh-iberica
tags: [voz, asr, guards, tests, agentes]
---
Una red de seguridad que busca el dato **por su forma escrita** queda **satisfecha en el vacío** en el canal de voz, donde el ASR transcribe los símbolos como palabras. Sale verde sin haber mirado nada.

Medido dos veces en el mismo repo, con dos campos:
- **Teléfono** (#246): `PHONE_RE` exige **dígitos**, y un teléfono dictado entero en palabras («seis uno siete…») tiene cero. Se cerró con un parser de números hablados.
- **Email** (#1502): `EMAIL_RE` exige una **`@` literal**, y por voz el ASR escribe «arroba» y «punto». Cero matches ⇒ el backstop anti-pérdida no reclamaba nada. **Un campo más tarde, mismo mecanismo, y el fichero ya documentaba el caso del teléfono a cuatro líneas de distancia.**

- Al escribir un detector sobre texto de usuario, listar **las dos formas de cada símbolo** (`@`/«arroba», `.`/«punto», dígito/palabra) — y si el proyecto ya cerró una, **buscar sus hermanas**: el hueco no es del campo, es del método.
- El alcance se elige por **resolubilidad, no por completitud**: en #1502 se reclama el **dominio** (forma rígida, «X punto Y») y **no** la parte local dictada letra a letra, porque los nombres de letra son indistinguibles de sílabas y adivinar produciría **avisos falsos sobre datos correctos** — el modo de fallo que un backstop existe para no tener.
- Y separa las averías antes de arreglar: un dato mal guardado puede ser **fonética del ASR** (irresoluble por parser) o **completion del modelo** (parte local perfecta, dominio cambiado por otro real). Solo la segunda la caza comparar contra lo que el usuario dijo.

Ver [[una-regla-que-solo-vive-en-el-prompt-se-cumple-casi-siempre]] · [[un-gate-que-cruza-dos-listas-es-ciego-a-lo-que-no-esta-en-ninguna]]
