---
title: otra sesión con pkill mata tu servidor y el resultado parece un bug del producto
date: 2026-08-10
source: claude-code-session
tags: [e2e, testing, sesiones-paralelas, metodo, diagnostico]
---
FacturaIA 10-ago: tres tandas E2E completas se cayeron a los 2-6 min con decenas de rojos que
parecían del producto (una acabó con 101 fallos y 384 casos sin correr). No era carga ni memoria.

**Cómo distinguir «me han matado» de «me he caído»** — las tres señales, juntas:
- exit **143** (SIGTERM) o `[?25h` al final del log: alguien mandó la señal, no hubo crash;
- **RSS bajo** y CPU normal en el momento de morir (medido: 629 MB / 46 %);
- `log show --last 30m | grep -i jetsam` **vacío** → macOS no lo mató por memoria.

La causa, capturada literal en el `ps` de otra sesión de la misma máquina:
`pkill -f "next-server"; sleep 2; lsof -ti:3007 | xargs kill -9; (npm start &)`.
**Cambiar de puerto NO protege** (medido: un servidor en el 3010 murió igual): el `pkill` es por
nombre de proceso. Matar por puerto sí acota, y es lo que la línea siguiente ya hacía.

**Arnés que lo delata**: anotar en `globalSetup` los PIDs del puerto y compararlos en el teardown →
distinguir «vivo el mismo» / «no responde nadie» / **«responde pero es OTRO proceso»**. `npm run dev`
deja **dos** PIDs en el puerto: comparar conjuntos, no «el primero», o el guard da falsos positivos.
