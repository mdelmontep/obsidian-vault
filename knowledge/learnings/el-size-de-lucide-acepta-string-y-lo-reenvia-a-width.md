---
title: el `size` de lucide acepta string y lo reenvía a width, así que `size="sm"` deja el svg sin caja
date: 2026-08-30
source: facturaia
tags: [frontend, react, iconos, typescript]
---
`LucideProps.size` es `string | number` y el componente lo pasa **tal cual** a `width`/`height`.
Un token nuestro (`size="sm"`) no es una longitud CSS válida: el svg pierde su caja y se estira
hasta llenar el contenedor. TypeScript no lo ve — el tipo lo admite.

Pasa cuando un icono de lucide se saca de un mapa y se llama igual que el componente propio:
`const Icon = SETTINGS_ICONS[id]` … `<Icon size="sm" />`. En TuFacturaIA salieron dos iconos de
14 px ocupando media pantalla, con el gate entero en verde (#2289).

Fix: renombrar el alias (`ItemIcon`), y reservar el nombre `Icon` para el componente propio con un
guard que grepee `(const|let) Icon *=`. Ver [[un-guard-que-lee-el-nombre-de-la-etiqueta-miente-si-el-nombre-es-un-alias]].
