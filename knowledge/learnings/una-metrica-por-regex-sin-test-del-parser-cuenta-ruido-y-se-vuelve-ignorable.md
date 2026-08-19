---
title: una métrica por regex sin test del parser cuenta ruido y acaba enseñando a ignorar el gate
date: 2026-08-02
source: claude-code-session
tags: [gates, ci, regex, testing]
---
Un trinquete que mide con regex sobre el texto crudo cuenta lo que **parece** el patrón. Si el repo
documenta con `#1155` (número de PR), un `HEX_RE` de 3/4/6/8 dígitos lo lee como color: cuatro
nibbles hex válidos.

Caso TuFacturaIA: `ratchet:design` daba rojo por dos citas a un PR en un comentario de
`button.module.css`, sin un solo color crudo en el fichero. Quitar comentarios antes de contar retiró
**8 ficheros enteros** de la lista de infractores (39 → 31). No era un caso aislado.

**Segunda familia de falso positivo, medida el 19-ago: la INTERPOLACIÓN legítima.** No hacen falta
comentarios para acusar al inocente, basta que el gate no entienda cómo se escribe el repo. Dos casos
del mismo gate en el mismo día: `class="${i === 0 ? 'a' : 'b'}"` se reportaba como botón sin clase
(borraba el `${…}` y veía cadena vacía), y un CSS inyectado como `` `${BASE}/x.css` `` se daba por no
inyectado porque el resolutor solo entendía comillas simples. Fix: rescatar los literales de dentro de
la interpolación y resolver la plantilla con las constantes del propio fichero; y si no se puede
resolver, **no afirmar nada** en vez de acusar.

- Fix: normalizar antes de medir (fuera comentarios, strings y `url()`) y **testear el parser** con
  los falsos positivos concretos, no solo el caso feliz.
- Lo caro no es el conteo inflado: un guard que grita por algo que no es deuda **enseña a ignorar el
  rojo**, y entonces ya no guarda nada.

Ver [[un-script-gate-con-guard-de-entrypoint-degrada-a-no-op-silencioso]] ·
[[un-guard-que-grepea-el-texto-del-fichero-no-distingue-uso-de-asercion]].
