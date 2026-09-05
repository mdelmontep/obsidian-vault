---
title: un commit de agente con un hecho falso se barre entero
date: 2026-09-06
source: mandadm
tags: [agentes, verificacion, metodo, documentacion]
---
`af1ed10` («segunda ronda de la horda») metió **cuatro** datos que nadie había decidido: el VPS de
despliegue, la cuenta de Instagram para las pruebas, «seeds aplicados» en el criterio de A10 —que
contradice al propio `docs/deploy/supabase.md:74`— y el dominio `mandadm.agentesia.madrid`, que era
**el criterio de aprobado** de esa tarea y aparecía 19 veces en 5 ficheros. Los cuatro salieron por
casualidad, en dos días y por tres personas o sesiones distintas, cada una tropezando con el suyo.

**Regla: en cuanto un commit de agente produce UN hecho falso, se barre entero.** Cazarlos de uno en
uno garantiza que quedan los que nadie pisa.

El barrido es barato y acotado: `git show <sha> --stat`, sacar de las líneas añadidas los datos duros
con un solo grep (IPs, hosts, puertos, versiones, límites numéricos, nombres de permiso), contrastar
cada uno contra la fuente de verdad del repo, y `git log -S"<dato>"` para confirmar quién lo escribió.

Y su mitad silenciosa vale igual: aquí todo lo demás resultó correcto y con fuente (`v25.0` en 9
ficheros oficiales, los 60 días, las 24 h, los tres permisos, los puertos de Supabase con su URL). Eso
**acota la duda**, que es la mitad del objetivo. Ver [[la-suposicion-de-un-agente-escrita-en-indicativo-se-lee-como-decision]]
