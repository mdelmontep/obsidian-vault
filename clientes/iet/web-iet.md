---
title: web iet
date: 2026-05-27
source: rediseño iet.es
tags: [iet, web, astro, tailwind, seo, frontend]
---

# Web IET — Documentación técnica

Rediseño completo de `iet.es` desde cero. Web corporativa B2B (instalaciones eléctricas y telecomunicaciones). Estática, enfocada a SEO y a verse "dramáticamente bonita" manteniendo la marca. Hub del cliente: [[00-home/iet|IET]].

## Stack

- **Astro** (estático, ideal SEO + hosting Apache del cliente) + **Tailwind v4** (plugin Vite, CSS-first `@theme`).
- **Fuentes auto-hospedadas** (sin Google Fonts en runtime): `Space Grotesk` (titulares) + `Geist` (texto), vía `@fontsource-variable/*`.
- **Iconos**: `astro-icon` + Phosphor (`@iconify-json/ph`).
- **Sitemap**: `@astrojs/sitemap`. **Motion**: CSS puro (sin React/GSAP/Framer) — mejor peso y SEO.
- Node 26, npm 11. Build → `dist/` (HTML + assets). `site: https://www.iet.es`.

## Sistema de diseño (`src/styles/global.css`)

- **Color**: rojo de marca `#DA2C2B` (muestreado del logo con Pillow), único acento. `#B81F1E` para hover. Grises neutros. Fondo off-white `#F5F5F4` (no blanco puro). Tokens semánticos en CSS vars (`--ink`, `--surface`, `--line`...) listos para dark mode futuro.
- **Tipografía**: display Space Grotesk, body Geist. (Open Sans del sitio viejo descartada, está vetada por las skills).
- **Motion** (curvas de Emil Kowalski): `--ease-out`, `--ease-fluid`, `--ease-drawer`. Scroll-reveal con IntersectionObserver que respeta `prefers-reduced-motion`. Botones con `scale(0.97)` al pulsar.
- Radios: un solo sistema (`--radius-card` 1.25rem, tiles 0.875rem, botones pill).

## Skills aplicadas

Instaladas vía `npx skills add emilkowalski/skill` y `Leonxlnx/taste-skill`, movidas de `.disabled` a activas en `~/.claude/skills/`:
- **design-taste-frontend** (anti-slop, pre-flight check), **high-end-visual-design** (look de agencia), **emil-design-eng** (motion/polish), **redesign-existing-projects**, **minimalist-ui**, **gpt-taste**.
- Pre-flight pasado: cero em-dashes, un solo acento, radios consistentes, ≤1 eyebrow por 3 secciones, sin clichés AI, una sola marquee.

## Estructura y rutas (slugs preservados del sitio viejo)

- `/` Home (8 secciones: hero asimétrico, marquee clientes, bento servicios, cifras, proceso, sectores, certificaciones, CTA)
- `/servicios/` + ruta dinámica `[slug].astro` → electricidad, cableado-estructurado, nuevas-tecnologias, mantenimientos
- `/empresa/quienes-somos/`, `/empresa/prevencion/`
- `/ingenieria/`, `/obras/`, `/clientes/` (55 clientes), `/certificados/`
- `/contacto/` (formulario), `/aviso-legal/` (redirect desde `/ley-de-proteccion-de-datos`), `404`
- **Datos centralizados** en `src/data/site.ts` (contacto, servicios, clientes, certificados). Componentes: `Layout`, `Header`, `Footer`, `CTASection`, `Breadcrumbs`.

## SEO

- Title + meta description únicos por página (el viejo tenía title triplicado + meta con 40 keywords amontonadas → penalizable).
- JSON-LD `LocalBusiness`/`ElectricalContractor` con dirección, teléfono, CIF, founded 1989.
- Open Graph + Twitter card (imagen `og-default.png` generada de marca 1200×630), canonical, sitemap, robots.txt, favicon de marca (tiles i·e·t).
- HTML semántico, `lang=es`, alt en imágenes, skip-link.

## Imágenes

- Stock de **Pexels** (URLs auto-hospedables) en `public/images/`, tratamiento **duotono** (grayscale + rojo multiply) para coherencia. Temas: electricidad, cableado, fibra, datacenter, oficinas, hospital, etc.
- **Pendiente**: sustituir por fotos reales de obras de IET (mismo nombre de archivo, no cambia el diseño).

## Formulario de contacto

- **Web3Forms** (gratis, sin backend, key pública). `src/pages/contacto.astro` lee `PUBLIC_WEB3FORMS_KEY` de `.env`.
- Estados de carga/éxito/error inline (sin `alert`). Honeypot anti-bot. Mapa de Madrid embebido (Google Maps iframe sin API key).
- **Pendiente**: el user crea la Access Key en web3forms.com con `administracion@iet.es` y la pone en `.env`. Ver `.env.example`.

## Despliegue

- `npm run build` → subir **todo `dist/`** a la raíz pública del Apache de iet.es (FTP/SFTP/panel). URLs con barra final → `index.html` por carpeta, sin config extra.
- **HTTPS roto** en su servidor: hay que instalar certificado (Let's Encrypt). Canonical/sitemap ya en `https://`.
- Túnel local NO funciona desde el Mac del user: puerto saliente 7844 (Cloudflare) y puertos de localtunnel bloqueados por la red. Para compartir → deploy estático (Netlify Drop / conectar repo).
- Dev: `npm run dev` (localhost:4321) · `npm run preview` sirve `dist/`.

## Pendientes

1. Commit + push a `mdelmontep/IET` (espera OK user).
2. Activar Web3Forms key.
3. Arreglar TLS/HTTPS en Apache.
4. Fotos reales de obra.
5. (Opcional) dark mode (tokens ya listos), enlace permanente conectando repo a Netlify/Cloudflare Pages.
