---
title: escribir la doc de exportación de un sistema lo audita entero
date: 2026-08-03
source: claude-code-session
tags: [metodo, diseno, auditoria, deuda]
---
Encargo: «saca los tokens para exportar el diseño a otras webs». Para documentar cada componente hay
que leer **el CSS entero de cabo a rabo**, y eso destapó siete defectos vivos que años de trabajo
fichero-a-fichero no habían visto: 47 azules a mano que ignoraban el color de marca por org, un botón
destructivo sin regla de estilo, una variable CSS inexistente, un token declarado en ningún sitio, un
`@keyframes` duplicado y dos guards de movimiento reducido que mostraban información falsa.

Por qué funciona: trabajar sobre un fichero solo obliga a mirar ese fichero. **Documentar para que otro
lo copie** obliga a mirarlo todo y, sobre todo, a *justificar* cada valor — y un valor que no sabes
justificar suele ser un error, no una decisión. La pregunta «¿qué copio?» recorre el sistema completo;
la pregunta «¿qué arreglo?» no.

Aplicable a cualquier sistema con superficie amplia y dueños difusos (design system, capa de tokens,
cliente de API, esquema de eventos). Barato: el entregable vale por sí solo, la auditoría sale gratis.
**Separar los PRs**: la doc por un lado, los arreglos por otro, o ninguno de los dos es revisable.

Ver [[una-metrica-por-regex-sin-test-del-parser-cuenta-ruido-y-se-vuelve-ignorable]]
