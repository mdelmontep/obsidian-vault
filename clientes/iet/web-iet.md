---
title: web iet
date: 2026-05-30
source: rediseño iet.es
tags: [iet, web, astro, tailwind, seo, frontend]
---

# Web IET — Documentación técnica

Rediseño completo de `iet.es` desde cero. Web corporativa B2B (instalaciones eléctricas y telecomunicaciones). Estática, enfocada a SEO. Iteración 3 con tema dark inspirado en `iet-soluciones.lovable.app`. Hub: [[00-home/iet|IET]].

## Stack

- **Astro** estático + **Tailwind v4** (plugin Vite, CSS-first `@theme`).
- **Fuentes auto-hospedadas** (sin Google Fonts en runtime): `Space Grotesk` (titulares) + `Geist` (texto) vía `@fontsource-variable/*`.
- **Iconos**: `astro-icon` + Phosphor (`@iconify-json/ph`).
- **Sitemap**: `@astrojs/sitemap`. **Motion**: CSS puro (sin React/GSAP/Framer).
- Node 26, npm 11. Build → `dist/` (~4 MB). `site: https://www.iet.es`.

## Sistema de diseño (`src/styles/global.css`)

Tokens semánticos en CSS vars + `@theme` de Tailwind. Iteración 3 (2026-05-30):

- **Brand rojo**: `#E31C1C` (subido desde `#DA2C2B`, más saturado, igual al de la referencia). Hover `#B91313`. Tint `#FDE8E8`.
- **Dark navy**: `--color-dark` `#1A202E` (header, footer, bandas oscuras). `--color-dark-2` `#232A3A` para variantes.
- **Tinta navy**: `--ink` `#151C28` (antes negro cálido). `--ink-2` `#2A3142`. `--ink-3` `#5A6172`.
- **Superficies**: paper `#ECEAE6`, surface `#FFFFFF`, elevated `#F6F4F0`. Bordes `rgb(21 28 40 / 0.14)` y `/0.22` para strong.
- **Tipografía**: display Space Grotesk, body Geist. Open Sans del sitio viejo descartada (vetada por las skills de diseño).
- **Motion** (curvas de Emil Kowalski): `--ease-out`, `--ease-fluid`, `--ease-drawer`. Scroll-reveal con IntersectionObserver que respeta `prefers-reduced-motion`. Botones con `scale(0.97)` al pulsar; logos del marquee con `scale(1.10)` al hover.
- **Botones**: `.btn-primary` (rojo + sombra roja), `.btn-ghost` (border-line), `.btn-white` (blanco + sombra dark, **nuevo** para CTAs sobre fondo rojo). Radio único: cards `1.25rem`, tiles `0.875rem`, botones pill.

## Skills aplicadas

Instaladas vía `npx skills add emilkowalski/skill` y `Leonxlnx/taste-skill`, activas en `~/.claude/skills/`:
- **design-taste-frontend** (anti-slop, pre-flight), **high-end-visual-design**, **emil-design-eng** (motion), **redesign-existing-projects**, **minimalist-ui**, **gpt-taste**.
- Pre-flight pasado: cero em-dashes, un solo acento, radios consistentes, ≤1 eyebrow por 3 secciones, sin clichés AI, una sola marquee.

## Estructura y rutas (slugs preservados del sitio viejo)

- `/` Home (hero · marquee clientes · bento servicios · cifras · proceso · sectores · certificaciones · CTA banda roja)
- `/servicios/` + ruta dinámica `[slug].astro` → electricidad, cableado-estructurado, nuevas-tecnologias, mantenimientos
- `/empresa/quienes-somos/`, `/empresa/prevencion/`
- `/ingenieria/`, `/obras/`, `/clientes/` (55 entradas), `/certificados/`
- `/contacto/` (formulario), `/aviso-legal/` (con redirect desde `/ley-de-proteccion-de-datos`), `404`

Datos centralizados en `src/data/site.ts`. Componentes: `Layout`, `Header` (dark sticky), `Footer` (dark), `CTASection` (banda roja), `Breadcrumbs`.

## Cabeza/pie y CTA (iteración 3, tema dark)

- **Header sticky DARK** (`--color-dark`) con nav blanca translúcida, dropdowns sobre tray blanco, hamburguesa blanca, botón "Pedir presupuesto" rojo a la derecha. Background semi-translúcido con blur al hacer scroll.
- **Footer DARK** con texto blanco translúcido, bordes blancos al 10%, iconos sociales en blanco.
- **CTA final como banda roja full-width** (no tarjeta con halo). `<CTASection />` reutilizable: título + texto + botón blanco + botón fantasma con ring blanco para el teléfono.

## Bento de servicios (iteración 2)

Reorganizado para evitar tarjetas huérfanas:
- **Electricidad** en banda horizontal full-width: icono+título+intro+CTA a la izquierda, lista de puntos con hairline divisora a la derecha.
- Cableado · Nuevas tecnologías · Mantenimientos en una fila de 3.
- Ingeniería como banda dark con halo rojo, full-width.

## Página de Obras (iteración 2)

- **36 obras reales** (con splits por año para clientes recurrentes): cliente, tipo, provincia, características, año. `Obra`/`ObraTipo`/`obras`/`obrasTipos` en `site.ts`.
- 6 tipos con icono Phosphor: Oficinas, Hotel, Retail, Industrial, Logística, Grupo electrógeno.
- **3 destacadas** arriba como tarjetas tipográficas con halo brand (sin foto).
- **Listado filtrable**: pills por tipo + select provincia + select año + buscador con debounce. Animación al filtrar vía View Transitions API (~280 ms), respeta `prefers-reduced-motion`.
- **Sin imágenes** en ninguna tarjeta (decisión del user).

## Logos de clientes (iteración 2)

20 logos en `public/clients/`, cableados a `clients` en `site.ts`:
- 17 SVG/PNG/JPG bajados de Wikipedia vía API (`prop=images` filtrando por "logo" en el nombre, prioridad SVG). Re-filtrado tras detectar que la primera ronda traía fotos de sedes/aeropuertos.
- 3 wordmarks SVG generados (Asisa, Lledó, Revenga — sin entrada de logo en Commons).
- Cepsa enlaza al logo Moeve (rebranding oficial 2024).
- Marquee: muestra los 20 a color por defecto, `scale(1.10)` al hover, marquee animation con mask de fade lateral.

## SEO

- Title + meta description únicos por página (el viejo tenía title triplicado + meta con 40 keywords).
- JSON-LD `LocalBusiness`/`ElectricalContractor` con dirección, teléfono, CIF, founded 1989.
- Open Graph + Twitter card (imagen `og-default.png` 1200×630), canonical, sitemap, robots.txt, favicon de marca (tiles i·e·t).
- HTML semántico, `lang=es`, alt en imágenes, skip-link.

## Imágenes

- **Sectores** (home y obras hero): stock de Pexels en `public/images/`, tratamiento duotono (grayscale + brand multiply).
- **Obras**: sin imágenes por entrada.
- **Pendiente**: sustituir las de stock por fotos reales de obras (mismo nombre de archivo).

## Formulario de contacto

- **Web3Forms** (gratis, sin backend, key pública). `src/pages/contacto.astro` lee `PUBLIC_WEB3FORMS_KEY` de `.env`.
- Estados de carga/éxito/error inline (sin `alert`). Honeypot anti-bot. Mapa de Madrid embebido (Google Maps iframe sin API key).
- **Pendiente**: crear la Access Key en web3forms.com con `administracion@iet.es` y ponerla en `.env`. Ver `.env.example`.

## Despliegue

- **Local**: `npm run dev` (localhost:4321) · `npm run build` → `dist/` · `npm run preview` sirve estático.
- **Producción** (objetivo): subir `dist/` a la raíz del Apache de iet.es (FTP/SFTP/panel). URLs con barra final → `index.html` por carpeta. Hace falta instalar certificado TLS (Let's Encrypt) en su servidor.
- **Preview actual**: https://illustrious-kulfi-1661d9.netlify.app (Netlify Drop manual, refrescable arrastrando `dist/` al panel *Deploys* del mismo sitio).
- **Túneles desde este Mac están bloqueados** (cloudflared 7844 y localtunnel verificados). Para compartir → siempre deploy estático.

## Repo

- github.com/mdelmontep/IET (privado, rama `main`). 5 commits actuales:
  - `98c30ca` copy: titular sectores + certificaciones (KNX/Leviton/DALI)
  - `5a9d1d2` tema dark + CTA roja + brand `#E31C1C`
  - `c0691c3` logos reales (re-filtrado)
  - `953186b` v2: logo compacto, contraste, bento, obras
  - `1467a42` rediseño completo inicial

## Pendientes

1. **Web3Forms key** — depende del cliente/user.
2. **TLS/HTTPS en Apache** — depende del cliente/user.
3. **Fotos reales de obra** — depende del cliente/user.
4. **(Opcional) Auto-deploy permanente** — conectar el repo de GitHub a Netlify/Cloudflare Pages en dos clics para que cada push despliegue solo.
