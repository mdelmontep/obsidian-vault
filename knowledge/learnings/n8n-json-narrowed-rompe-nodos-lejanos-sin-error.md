---
title: un nodo que reduce $json (GET con propertyName, etc) rompe en silencio TODO nodo aguas abajo que siga leyendo el trigger original
date: 2026-08-13
source: claude-code-session
tags: [n8n, expresiones, redis, debugging]
---
Extiende el gotcha ya conocido de Set/Redis GET reemplazando `$json` (Stack/n8n.md L32-34): el
riesgo no es solo el nodo inmediatamente siguiente — **cualquier nodo, a cualquier distancia aguas
abajo**, que siga leyendo `$json.campoDelWebhookOriginal` en vez de `$('NodoWebhook').item.json...`
rompe. Y no siempre lanza excepción: si el campo termina en un `IF`/`Switch` de routing, la
condición simplemente evalúa distinto (siempre false, p. ej.) y el mensaje se procesa por la rama
equivocada sin ningún error — indistinguible de "funciona" hasta que alguien mira el dato real.

Caso real Simarro 13-ago: un fix de dedup (Redis GET con `propertyName`) insertado el 12-ago dejó
ROTOS 3 nodos distintos aguas abajo en el mismo workflow (`Chatbot Simarro`) — un Redis SET (key
undefined → excepción real, sí avisó a Slack), un Set de extracción de campos (todo `null`, sin
excepción, el bot procesaba con datos vacíos) y un IF de routing foto-vs-texto (condición siempre
false, sin excepción, meses de fotos mal enrutadas sin que nadie lo notara). Nadie lo detectó hasta
probarlo con un mensaje real — el fix nunca se había ejercitado en producción desde que se escribió.

**Diagnóstico reusable**: recorrer el grafo de conexiones desde el nodo que reduce `$json` (BFS)
y grep todos los parámetros de los nodos alcanzables buscando `$json.<campo que solo existía en
el trigger>` — cualquier hit ahí es sospechoso, confírmalo leyendo runData de una ejecución real.

Ver también [[n8n-execute-workflow-nodo-terminal-ambiguo-con-multiples-ramas]] (mismo día, mismo
workflow, bug distinto pero mismo síntoma raíz: cambiar la forma de $json en un punto de la cadena
sin auditar TODO lo que viene después).
