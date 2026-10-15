---
title: la opción ip de daemon.json solo ata a 127.0.0.1 la red bridge por defecto
date: 2026-10-15
source: facturaia (VM gates, Docker rootless, fia-dbtest)
tags: [docker, rootless, supabase, seguridad, red]
---
- **Síntoma**: con `"ip": "127.0.0.1"` en `daemon.json` y Docker reiniciado, `agh-pg` escuchaba en 127.0.0.1, pero el Supabase local (`supabase_kong_*` 54521, `supabase_db_*` 54522, contraseña por defecto) seguía en `0.0.0.0` y `[::]`.
- **Causa**: `ip` solo aplica a la red `bridge` por defecto. `supabase start` crea su propia red (`supabase_network_<proyecto>`, `Options={}`), y en una red de usuario la IP de enlace la decide su opción `com.docker.network.bridge.host_binding_ipv4`. El `HostIp` de los PortBindings estaba vacío: no lo fija el CLI.
- **Fix** (al recrear el stack): `supabase stop` → `docker network create -o com.docker.network.bridge.host_binding_ipv4=127.0.0.1 --label com.supabase.cli.project=<p> supabase_network_<p>` → `supabase start`. Pendiente de comprobar que el CLI reutiliza la red: probarlo antes con un project_id de usar y tirar.
- **Verificar**: `ss -tlnp` debe mostrar los puertos en 127.0.0.1. Desde la VPN salían cerrados, filtrados por fuera; eso no prueba nada desde la LAN de la propia VM.
- Pariente en macOS: [[colima-publica-los-puertos-de-docker-en-toda-la-red-local]]. Disco de la misma VM: [[disco-de-vm-multiusuario-con-docker-rootless-se-mide-por-usuario]].
