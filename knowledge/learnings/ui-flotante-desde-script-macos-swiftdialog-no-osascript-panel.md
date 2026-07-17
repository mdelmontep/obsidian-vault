---
title: UI flotante propia desde un script (macOS) — usa swiftDialog (app real), no una ventana osascript/WKWebView
date: 2026-07-17
source: claude-code-session
tags: [macos, osascript, ui, claude-code, scripting]
---
Para un banner/tarjeta custom desde un script (p.ej. estado de build), NO crees un NSPanel/WKWebView con `osascript`:
- Lanzado desde el contexto de Claude Code (o headless), el `osascript` reporta `panel.isVisible=true` pero NO pinta nada — un WKWebView transparente no llega a renderizar sin el run loop de una app real; queda una ventana invisible.
- `NSScreen.mainScreen` cae en la pantalla del portátil, no en el monitor donde miras. Si aun así pintara, aparece en otra pantalla. Usa la screen bajo el ratón (`NSEvent.mouseLocation`).
- Una `.app` hecha a mano no siempre arranca con `open` (LaunchServices la ignora en silencio; log vacío).

Fix: usa algo que ES una app real (swiftDialog `dialog`, `brew install --cask swiftdialog`, instala con sudo) — se lanza a la sesión gráfica y renderiza fiable. Pega: no ajusta la tarjeta al contenido (padding + tamaño mínimo). Para un "toast" que abrace el texto no hay vía fiable por script → mejor un badge de barra de menú (SwiftBar). Ver [[fia-gate]].
