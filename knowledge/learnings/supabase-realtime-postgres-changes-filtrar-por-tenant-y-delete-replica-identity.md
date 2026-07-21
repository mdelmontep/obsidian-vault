---
title: supabase realtime postgres_changes — filtrar por tenant y ojo con el delete
date: 2026-07-21
source: claude-code-session
tags: [supabase, realtime, performance]
---
`postgres_changes` autoriza CADA cambio contra CADA suscriptor (RLS por-cambio). El throughput escala con el nº de suscriptores, no con el write rate. Sin `filter`, cada cliente recibe y RLS-autoriza los cambios de TODAS las orgs y los descarta → coste inútil. Añadir `filter: 'org_id=eq.<uuid>'` a cada `.on('postgres_changes', ...)` (con guarda `if (!orgId) return`).

CAVEAT DELETE: con `REPLICA IDENTITY` = default (PK), el payload del DELETE trae solo la PK → un `filter` sobre otra columna (org_id) NO casa y el evento no se entrega (el contador no refresca al borrar). `REPLICA IDENTITY FULL` lo arregla pero AUMENTA el WAL — contraproducente si el problema es justo el coste de WAL. Alternativa: aceptar que el borrado no refresca en vivo (auto-sana por refetch al montar/volver a foco).

El coste dominante `realtime.list_changes` (leer WAL por poll) NO baja con filtros: solo baja con menos tablas publicadas o migrando a Broadcast from Database (Supabase lo recomienda >~3000 subs concurrentes). Quitar de la publicación las tablas que ningún cliente escucha (cruzar `pg_publication_tables` con grep de `.on('postgres_changes'`).
