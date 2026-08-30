---
title: el dev server que mides en localhost:3000 puede ser de OTRO proyecto — verifica el <title>
date: 2026-08-30
source: facturaia
tags: [nextjs, qa, agent-browser, localhost]
---
Con varios Next abiertos, `npm run dev` ve el 3000 ocupado y se va al 3001/3002 **sin que nadie lo lea**: el aviso queda en el log del arranque, no en la sesión. Si luego apuntas el navegador al 3000 por costumbre, mides la app del otro proyecto y todo parece roto de forma coherente — en FacturaIA salió "H1: Entrar" en las 12 rutas y perseguí una sesión que nunca iba a valer, porque la pantalla de login era de TuCRMIA.

Antes de dar por buena cualquier medida en local:
```bash
for p in 3000 3001 3002 3003; do echo "$p -> $(curl -s -m5 http://localhost:$p/ | grep -o '<title>[^<]*')"; done
```
El `<title>` identifica el proyecto en una línea. Vale también para el caso inverso: la app respondía, así que ni un 404 ni un timeout te avisan.

Corolario: en un repo cuyo `.env.local` apunta a producción, comprueba además contra qué BD habla lo que estás midiendo. Ver [[credencial-de-test-guardada-puede-apuntar-a-otro-proyecto-y-a-un-usuario-sin-membresias]].
