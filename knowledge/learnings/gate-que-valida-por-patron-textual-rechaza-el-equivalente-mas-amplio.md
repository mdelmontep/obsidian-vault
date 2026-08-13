---
title: un gate que valida por patrón textual rechaza el equivalente semántico más amplio
date: 2026-08-13
source: claude-code-session facturaia
tags: [hooks, gate, metodo, postgres, harness]
---
`revoke-guard` exige `REVOKE EXECUTE ON FUNCTION …` y bloquea el commit si no lo
encuentra. Escribir `REVOKE ALL ON FUNCTION …` —que revoca **más**, incluido
EXECUTE— lo hace saltar igual: busca el literal, no el efecto. Me pasó a mí y a
un subagente el mismo día, en dos migraciones distintas.

Patrón: todo guard que valide por regex sobre el fuente tiene esta clase de falso
positivo. Cuando salte, **la salida no es discutir con el hook**: es escribir la
forma que espera. Su contrato es el texto, y el texto también lo lee el humano
que audite la migración dentro de un año.

Al escribir un guard así, dos cosas ayudan: que el mensaje de error cite el
literal exacto que quiere (este lo hace, por eso se arregla en un minuto), y
tener claro que solo mide forma — un `REVOKE ALL` que faltara lo dejaría pasar
si el fichero contiene el literal en un comentario.

Ver [[supabase-rpc-security-definer-execute-public]] ·
[[postgres-revoke-public-no-elimina-grants-individuales]]
