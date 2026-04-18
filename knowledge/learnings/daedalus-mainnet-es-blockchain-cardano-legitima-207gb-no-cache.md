---
title: daedalus mainnet es blockchain cardano legitima 207gb no cache
date: 2026-04-15
source: claude-code-session
tags: [macos, cardano, cleanup, falso-positivo]
---

**No proponer borrar `~/Library/Application Support/Daedalus Mainnet` en auditorías de disco sin confirmar antes.**

Daedalus es el wallet oficial full-node de Cardano: descarga la **blockchain completa** para poder validar transacciones localmente sin depender de servidores de terceros. En abril 2026 ocupa **~207 GB** en el Mac de Manu — el mayor consumidor individual de Application Support por 20x.

### Por qué es un falso positivo en auditorías

Cuando corres `du -sh ~/Library/Application Support/*` y aparece una carpeta de 200+ GB, es tentador proponer borrarla como "cache masivo". **Error**. Daedalus necesita esa cadena sincronizada para funcionar, y si la borras:

1. Pierdes acceso al wallet hasta resincronizar (días de descarga)
2. Sin la **seed phrase de 24 palabras** guardada, no puedes restaurar el wallet en otra instancia

### Si de verdad quieres liberar esos 207 GB

1. **Confirmar primero que la seed phrase de 24 palabras está guardada fuera del Mac** (papel, gestor de contraseñas con backup, caja fuerte)
2. Migrar los fondos a un wallet ligero: **Yoroi**, **Eternl**, **Lace**. Estos no sincronizan la cadena entera, solo consultan a nodos remotos
3. Una vez los fondos estén en el wallet ligero, Daedalus es prescindible y se puede desinstalar

### Regla para sesiones futuras

Si en una auditoría de disco aparece `Daedalus Mainnet` grande, **no es basura**. Es el indicador de que Manu sigue usando Cardano con full-node. Preguntar antes de tocar, y solo tras confirmación explícita de que la seed phrase está segura.
