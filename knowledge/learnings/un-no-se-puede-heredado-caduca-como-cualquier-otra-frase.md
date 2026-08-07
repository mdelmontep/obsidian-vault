---
title: un «no se puede» heredado caduca como cualquier otra frase — vuelve a preguntarle a la máquina
date: 2026-08-07
source: claude-code-session
tags: [metodo, debug]
---
Un bloqueo documentado se cita después como si fuera física. Dos casos el mismo día, con resultados
opuestos, y por eso vale la pena volver a intentarlo siempre:

- **HTTPS**: «el cupo de Let's Encrypt está agotado» era cierto; «así que hace falta comprar dominio»
  no se seguía de ahí. Cuatro días perdidos. Ver [[traefik-me-no-emite-certificado-por-cupo-compartido-agotado]].
- **Un `grant` de Postgres**: se volvió a intentar y seguía imposible — pero preguntando *por qué* en
  vez de *si*, la respuesta pasó de «falló» a «no falta un permiso, falta la PROPIEDAD de la tabla, y
  `create policy` la exige». Eso convierte un ticket de soporte de tres correos en uno.

La diferencia entre las dos preguntas: **«¿se puede?» devuelve un booleano que envejece; «¿por qué no?»
devuelve un hecho que se puede contrastar.** Pregúntale al sistema (`pg_auth_members`, `openssl
s_client`, la API), no a la nota de la semana pasada.
