---
title: un JSON intermedio correcto no prueba que el destinatario reciba nada
date: 2026-08-20
source: tecnocloud
tags: [n8n, gates, verificacion, email]
---

Reordené una cadena de n8n para que el email saliera antes que la escritura en Sheets. Verifiqué la
salida del Code node: impecable, todos los campos con su valor. El email llegó a soporte **sin
teléfono y sin resumen** durante dos días.

Lo roto no era el dato, era la **plantilla del destinatario**: el HTML leía `{{ $json["Teléfono"] }}`
con acento, que eran los nombres de las COLUMNAS del Sheet, y funcionaba solo porque antes recibía el
item de Sheets. Al cambiar el orden pasó a recibir el del Code (`Telefono`, sin acento) → vacío.
`Nombre` coincidía en ambos y era el único campo visible, lo que hacía el fallo aún más confuso.

Dos reglas:
- Una referencia **implícita** (`$json.campo`) es una dependencia oculta del nodo anterior: cualquier
  reordenación la rompe en silencio. Referencia siempre el nodo productor por nombre.
- El gate correcto no es «el nodo emite bien», es **resolver las expresiones del destinatario contra
  los datos de una ejecución real**. Herramienta: `~/.claude/bin/n8n-verificar-refs <base> <wf> [exec]`,
  sale con 1 si alguna queda vacía. Ver [[publicar-un-agente-no-basta-el-numero-puede-fijar-su-version]].
