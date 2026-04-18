---
title: guía rápida — cómo usar claude con obsidian
date: 2026-04-17
tags: [home, guia]
---

# Cómo funciona Claude + Obsidian

## Lo básico

Claude lee automáticamente tu CLAUDE.md cada vez que abres una sesión.
En ese archivo están las instrucciones de cómo operar tu vault.
Tú no tienes que recordar nada — solo hablar naturalmente.

## Qué puedes decir (en cualquier sesión)

| Lo que dices | Lo que Claude hace |
|---|---|
| "qué tengo pendiente" | Lee tus prioridades y cuenta notas en inbox |
| "guarda esto en obsidian" | Te propone dónde guardarlo y lo escribe |
| "esto es un learning" | Crea una nota en knowledge/learnings/ |
| "documenta lo de Tecnocloud" | Busca/actualiza la doc del cliente |
| "procesa inbox" | Clasifica las notas sueltas de inbox/ |

## Al terminar una sesión larga

Claude te sugerirá ejecutar `/obsidian-1`. Ese comando:
1. Revisa qué aprendimos en la sesión
2. Propone qué guardar (tú apruebas cada cosa)
3. Actualiza tus prioridades y el hot cache

## Estructura de tu vault

```
Manu/
├── inbox/          ← notas rápidas sin procesar
├── knowledge/
│   ├── learnings/  ← lo que aprendes (errores, fixes, reglas)
│   └── projects/   ← docs por cliente/proyecto
├── 00-home/
│   └── top-of-mind.md  ← tus prioridades actuales
└── Stack/
    ├── hot.md      ← lo reciente (últimas 2 semanas)
    └── index.md    ← índice de todo el conocimiento
```

## Lo que se entrena solo vs. lo que no

| Qué | Se actualiza solo? |
|---|---|
| CLAUDE.md (errores, reglas) | Sí — cada error = regla nueva |
| Learnings en el vault | Sí — /obsidian-1 los captura |
| Hot cache | Sí — /obsidian-1 lo mantiene |
| Nuevos tipos de proyecto | No — hay que crear la carpeta |
| Nuevos comandos | No — hay que crearlos |

## Dos slash commands que tienes

- `/obsidian-1` — fin de sesión: compila todo lo aprendido
- `/obsidian-2` — procesa inbox: clasifica notas sueltas
