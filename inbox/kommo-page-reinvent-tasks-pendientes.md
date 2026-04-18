---
title: kommo page — mapping de bloques WhatsApp Gonzalo a secciones
date: 2026-04-16
source: claude-code-session
tags: [inbox, kommo, frontend, pendiente, agentesia-web]
---

Reinvent del `/servicios/kommo` en `new-project-setup`. La primera narrativa "Antes: 7 pestañas. Después: 1 panel." **fue rechazada** por el usuario ("no me gusta el antes/después"). Segunda versión: posicionamiento SaaS premium omnicanal + IA, con textos literales de los 6 bloques de WhatsApp de Gonzalo del 15-abr-26.

## Estado

- ✅ `HeroSwarm.tsx` reescrito (2ª vez) — hero editorial premium: eyebrow pill "Kommo · CRM Omnicanal con IA", H1 "Plataforma de Atención al Cliente **Omnicanal impulsada por IA**" (gradient en segunda parte), subtitle con bloque 1 de Gonzalo, dos CTAs, mockup grande de bandeja unificada (6 tabs de canales + sidebar con 4 conversaciones + panel activo con burbujas + footer "IA sugiere"), pills flotantes en los laterales

## Textos literales de Gonzalo (15-abr-26)

**Bloque 1** — "Transforma la manera en la que te comunicas con tus clientes. Nuestra plataforma de atención al cliente omnicanal abre un mundo de posibilidades para conectar mejor. Operativa 24/7 y en todos los canales digitales posibles, ofrece una atención integral y coherente que mejora la experiencia del usuario, atrae y fideliza"

**Bloque 2** — "Un sencillo escritorio unificado para administrar y monitorizar las interacciones a través de nuestra plataforma multicanal de atención al cliente, con toda la información y experiencia previa del usuario. Una valiosa información sobre sus hábitos, preguntas, respuestas o decisiones que te permitirá ofrecer una atención coherente, personalizada y de alta calidad. Descubre cómo esta herramienta puede impactar positivamente en tus resultados y en la imagen de tu marca. La plataforma multicanal KOMMO es clave para la fidelización y la captación de nuevos clientes."

**Bloque 3** — "Multicanalidad: Trabajamos con los principales canales digitales y RRSS. [Features: transcripción multilenguaje +30 idiomas, búsqueda inteligente NPL, configuración de roles por servicios/campañas, extracción +40 métricas operacionales, actualizaciones periódicas incluidas, sumarización automática, clasificación y categorización automática]. VOZ · SMS · EMAIL · SOCIAL MEDIA · MENSAJERÍA · WEBCHAT"

**Bloque 4** — "WhatsApp: Aprovecha uno de los sistemas de mensajería más populares para ofrecer un servicio de alta calidad y mejorar la experiencia general del cliente. Un servicio al cliente omnicanal que permite a los agentes acceder al historial completo de interacciones previas, independientemente del canal utilizado."

**Bloque 5** — "NO PIERDAS UN SOLO CLIENTE POR ESTAR FUERA DE HORARIO. Responde de forma automatizada a través de una plataforma intuitiva y de uso muy sencillo. Ofrece una atención permanente, optimizando la percepción que tus clientes"

**Bloque 6** — "REGISTRA TODA LA INFORMACIÓN AUTOMÁTICAMENTE EN TU CRM KOMMO. Toda la información del cliente y los detalles de las interacciones se almacenan de forma automática. Dispón de un registro completo de las conversaciones y conoce mejor a tus clientes mediante un histórico de sus interacciones"

## Mapping propuesto (acordado con el usuario)

| Sección (archivo) | Bloque | Imagen |
|---|---|---|
| `HeroSwarm.tsx` ✅ | 1 (subtitle) | mock renderizado — pendiente: hero más "humano" con foto real |
| `ChannelsGrid.tsx` | 3 (intro + 6 canales) | logos SVG locales |
| `CustomerJourney.tsx` → Escritorio Unificado | 2 | `foto-web-section-2.webp` + mock unificado |
| `AIFeaturesBento.tsx` → WhatsApp Showcase | 4 | `iphone-frame.png` + mock WhatsApp (generar con nano banana) |
| `MetricsSunburst.tsx` → 7 features IA | 3 features | iconos lucide |
| `AlwaysOnStrip.tsx` | 5 | reloj digital + opcional imagen noche |
| `KommoFinalCTA.tsx` | 6 + CTAs | opcional screenshot Kommo dashboard |

## Pendiente de decisión del usuario

1. **Nano Banana disponibilidad** — falta `pip install google-genai pillow` + `export GEMINI_API_KEY` en el shell del usuario para poder generar la imagen de chat WhatsApp y la foto humana del hero desde Claude Code. Alternativa: Google AI Studio gratis o fotos existentes de `/public/images/` (clientes reales de Agentesia).
2. **Hero más humano** — clarificar si quiere (i) añadir foto al lado del mockup, (ii) reemplazar el mockup por foto + mini-mock flotante, o (iii) volver a un split con foto más humana que `foto-web-section-2.webp`.
3. **Screenshot Kommo dashboard real** para sección CRM final — si lo pasa, mejor que un mock.

## Reglas que aplican

- Consistencia con el resto del site: fondo `hsl(210 40% 98%)`, gradient `#8271ff → #03C3FF`, nada de fondos oscuros
- Respetar `CLAUDE.md` sección Frontend/Motion: nada de `repeat: Infinity` en superficies grandes, blurs ≤ 8px y one-shot
- Animaciones viewport-gated con `useInView(ref, { once: true, margin: "-80px" })`
- `debug-kommo.mjs` en la raíz del repo corre Playwright en mobile (375) + desktop (1440) con scroll-through y verifica overflow
