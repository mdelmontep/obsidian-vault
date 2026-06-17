---
title: decomiso de bot monolítico bloqueado por nodos de creación compartidos
date: 2026-06-17
source: claude-code-session
tags: [n8n, copiloto, migracion, arquitectura]
---

Al migrar un bot monolítico n8n a tools de un copiloto **acción por acción** (flip incremental), NO puedes decomisar el bot hasta migrar TODOS los tipos.

Motivo: los nodos de **creación de documentos suelen estar compartidos** entre tipos. En FacturaIA, `Generar Factura` / `Crear … en BD` / `Preparar Datos Generar` sirven factura (flipada) Y presupuesto/proforma (no flipados) — branchean por `.tipo` internamente.

Dos capas distintas tras un flip:
- **Prompt**: las ramas del tipo flipado quedan inertes (la PRECEDENCIA ya enruta a `accion_copiloto`). Borrables y reversibles, pero solo cosméticas.
- **Nodos**: compartidos → **load-bearing**. Borrarlos rompe los tipos aún no migrados.

Fix/patrón: antes de planear un decomiso, **traza el grafo** (qué nodos son tipo-específicos vs compartidos). El decomiso real está bloqueado por migrar los tipos restantes, no por el último flip. Deja las ramas dormidas como red de revert mientras bakea.

Relacionado: [[retell-subagent-nodes-dividen-agentes-monoliticos-en-especializados]] · [[n8n-nodos-compartidos-entre-ramas-requieren-if-isExecuted]]
