---
title: un plan que delega una capacidad en un sistema que aún no existe deja el producto sin puerta
date: 2026-08-03
source: claude-code-session
tags: [arquitectura, producto, adr, planificacion]
---
Un ADR decidió que el producto no tiene registro propio: la organización nace cuando el cliente activa el
módulo en «la plataforma». Correcto para el producto final. **Esa plataforma no estaba construida**, y
nadie escribió qué pasaba mientras: con catorce migraciones aplicadas, la API respondiendo en producción
y 705 pruebas en verde, **nadie podía entrar** — ni un cliente ni nosotros. Las organizaciones existentes
se habían insertado con SQL a mano.

Al escribir un ADR que delega una capacidad en un sistema externo, añadir siempre la fila **«qué pasa
hasta que exista»**, aunque la respuesta sea «a mano». Si no, el hueco no aparece en ninguna lista: no es
una tarea pendiente, es una ausencia.

Y el sustituto manual no se tira después: es la herramienta con la que se atiende al cliente que llama
por teléfono y con la que se arregla un aprovisionamiento a medias. El endpoint del panel, cuando llegue,
llama a esa misma lógica.

Señal para buscarlo: un camino crítico cuyo primer paso lo ejecuta alguien que no eres tú.
