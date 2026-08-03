---
title: no-restricted-imports compara el TEXTO del import — ciérralo por importNames
date: 2026-08-03
source: claude-code-session tucrmia
tags: [eslint, arquitectura, gates, seguridad]
---

Un `group` de `no-restricted-imports` se compara contra la **cadena literal** del import. Una
frontera escrita solo con alias deja dos puertas abiertas, las dos comprobadas con un fichero de
prueba y `eslint` devolviendo 0:

```ts
import { clienteDeServicio } from '../../core/db/servicio'  // ruta relativa: no casa '@/core/db/*'
import { getClient } from '@/core/api/v1'                   // reexportado desde un módulo libre
```

La primera es lo que escribe el auto-import del editor. La segunda **no se arregla añadiendo esa
ruta**: sería la tercera variante de la misma regla, señal de que la lista se va a quedar corta
otra vez ([[un-detector-que-enumera-sintaxis-se-queda-corto-comprueba-la-identidad]]). Se cierra
por identidad del nombre:

```js
{ group: ['*', '**/*'], importNames: ['clienteDeServicio', 'getClient'], message: '…' }
```

Y para las rutas relativas, añadir el patrón sin alias (`**/core/db/*`) al mismo grupo.

Corolario de zonas: la excepción legítima va en **bloque propio**, no en `ignores` — en config
plana `ignores` levanta el bloque ENTERO, así que la ruta exceptuada pierde también las
prohibiciones que sí debía conservar. Ver
[[eslint-no-restricted-imports-la-negacion-no-reincluye-bajo-un-padre-excluido]] ·
[[acotar-por-tipo-que-tablas-puede-tocar-una-zona-del-codigo]]
