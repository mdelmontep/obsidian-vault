---
title: instalar op CLI en Mac Apple Silicon sin Homebrew (arquitectura darwin_arm64, no apple_arm64)
date: 2026-07-24
source: claude-code-session
tags: [1password, macos, cli, homebrew]
---
En un Mac nuevo sin Homebrew, el binario oficial de `op` (1Password CLI) se descarga directo de `cache.agilebits.com` sin pasar por brew.

Trampas:
- El nombre de arquitectura es **`darwin_arm64`**, no `apple_arm64` (probé ese primero, 404).
- El número de versión hay que sacarlo de `https://app-updates.agilebits.com/product_history/CLI2` — no asumir una versión, cambian rápido y las URLs viejas dan 404.
- Patrón final: `https://cache.agilebits.com/dist/1P/op2/pkg/v<version>/op_darwin_arm64_v<version>.zip`

Instalación sin sudo: descomprimir, copiar el binario `op` a `~/.local/bin/op`, `chmod +x`, y `xattr -d com.apple.quarantine` (si no, macOS Gatekeeper lo bloquea al ejecutar). No requiere admin ni Homebrew.
