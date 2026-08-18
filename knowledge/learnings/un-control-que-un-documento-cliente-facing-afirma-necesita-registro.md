---
title: un control que un documento cliente-facing afirma necesita registro con fecha, no una descripción
date: 2026-08-18
source: claude-code-session agh-iberica
tags: [compliance, rgpd, metodo, documentacion, cliente]
---
Una afirmación de **control** no se descubre falsa por un test en rojo: solo cuando alguien la audita.

Medido (AGH). `arquitectura-rag-enterprise.html` —el documento que AGH enseña a **su propio compliance**— afirma «API pública con **DPA + zero-retention**» y lo lista como control **existente** en cuatro sitios; lo repiten el ADR, el PRD y el `CLAUDE.md`. Grep de todo el repo por `DPA|zero.?retention|ZDR|encargado del tratamiento`: **todos los aciertos DESCRIBEN el escalón, ninguno REGISTRA que el contrato exista** — ni referencia, ni fecha, ni dónde vive. Lo más cerca de un registro era un paréntesis en una nota de sesión: *«el texto ya cruza a OpenAI (DPA)»*. **Un paréntesis no es un contrato.**

- Todo control que un documento cliente-facing afirme necesita **registro con fecha y ubicación** (1Password / Drive). Si no lo tiene, la urgencia **no** es firmarlo: es **que el documento no lo afirme** mientras no exista.
- El riesgo no escala con el tamaño del cliente sino con **quién lee el documento**: aquí, el departamento de seguridad de una multinacional, que es exactamente quien va a pedir ese papel.
- Al verificar un DPA/ZDR de proveedor de LLM, comprueba las **tres** por separado: contrato firmado · zero-retention **activo en la organización** (no es el default, suele pedirse) · **que la key de prod pertenezca a esa organización** (una key personal bajo otra org no hereda nada).
- Y una precondición escrita como **casillas dentro de otro issue** se archiva al cerrarlo: invisible para `gh issue list`. Si su autor escribe «no es de este issue», nace como issue propio **en ese momento**.
- Cuando un frente RGPD tiene cuatro issues abiertos (permiso de egress, cláusula, retención, borrado por sujeto), **es una reunión, no cuatro** — repartirlos es lo que hace que ninguno avance.

Ver [[un-comentario-no-puede-afirmar-el-estado-de-un-panel-de-deploy]] · [[campo-de-texto-libre-que-viaja-a-telemetria-es-un-canal-de-egress]] · [[una-obligacion-legal-no-puede-colgar-del-prompt-del-llm]]
