---
title: swiftbar/xbar dibuja templateImage a puntos=píxeles; fija el bitmap para retina
date: 2026-07-22
source: claude-code-session
tags: [macos, swiftbar, xbar, menubar, icon]
---
SwiftBar/xbar renderiza `image=`/`templateImage=` (base64 PNG en la 1ª línea del plugin) a su tamaño en PUNTOS, y por defecto **puntos = píxeles** (72 dpi). NO lo escala a la altura de la barra → un PNG grande sale GIGANTE (no cabe).

Para un icono pequeño Y nítido: renderiza en alta densidad (p.ej. 8x) y fija el tamaño físico del bitmap ANTES de codificar:
`rep.size = NSSize(width: wpt, height: hpt)` en `NSBitmapImageRep` → escribe el chunk pHYs/dpi y NSImage lo lee como retina @Nx. El knob de tamaño = altura en PUNTOS, no los píxeles. Verificar: `sips -g dpiWidth <png>` debe dar >72 (aquí ~1036 = 14.4x).

Gotchas SwiftBar: `| templateImage=…` necesita espacio DESPUÉS del pipe (título vacío antes); título vacío + imagen que no renderiza = ítem invisible. `swiftbar://refreshallplugins` solo re-ejecuta los plugins YA cargados — un fichero de plugin NUEVO exige relanzar SwiftBar para reescanear la carpeta. Icono template = negro + alpha (se tinta solo claro/oscuro).

Producto real construido con esto: `~/Tapa` (toggle de reposo al cerrar la tapa). Ver [[macos-disablesleep-no-se-lee-con-pmset-usar-ioreg]].
