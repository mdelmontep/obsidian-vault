---
title: la suposición de un agente escrita en indicativo se lee como decisión
date: 2026-09-05
source: mandadm
tags: [agentes, documentacion, metodo, horda]
---
Una horda de agentes rellenó el plan de MandaDM y escribió «se despliega en el VPS `185.47.13.170`» y
«para las pruebas vale la cuenta de Instagram de TuFacturaIA». **Nadie decidió ninguna de las dos**:
eran suposiciones razonables, escritas sin condicional en el fichero que el resto del plan trata como
fuente de verdad. De ahí se propagaron a la política de privacidad, al runbook, al tracker y a dos
documentos más, cada uno citando al anterior. Manuel cazó la primera; la segunda apareció buscándola.

Se detecta con `git log -S"<el dato>"`: si el commit que lo introduce es del agente y no hay ADR
detrás, no es una decisión — es una frase.

**El fix no es cambiar la propuesta**, que suele ser buena: es cambiar lo que el documento **afirma**.
Quién lo escribió, que falta el visto bueno, y la consecuencia concreta de equivocarse (aquí: el
webhook mete en `events` todo lo que entra, así que conectar esa cuenta arrastra a otra base de datos
los DMs de leads reales).

Regla para el arnés: **un agente autónomo no escribe en indicativo lo que no ha medido.** Lo que
suponga va con su autor y su condición, o va a un ADR con las alternativas.
Ver [[un-agente-que-trae-documentacion-transcribe-el-marcador-como-valor]]
