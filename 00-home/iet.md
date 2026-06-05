---
title: iet
date: 2026-06-05
tags: [cliente, iet, hub]
---

# IET — Instalaciones Eléctricas y de Telecomunicación

Empresa de instalaciones eléctricas y telecomunicaciones, Madrid, fundada en 1989. Proyecto actual: **rediseño completo de su web** (la antigua era WordPress 4.9). Web nueva en Astro estática, **en producción en iet.es** con HTTPS activo.

## Estado actual

- **PRODUCCIÓN ACTIVA** — `https://iet.es` (SFTP sobre servidor IONOS/1&1, SSL Let's Encrypt activo)
- **Preview**: `https://iet-preview.surge.sh`
- **Repo GitHub**: github.com/mdelmontep/IET (privado, rama `main`, último commit `7e9e4ad`)
- **WordPress original**: renombrado a `_index.php.bak` en el servidor — intacto pero no sirve
- **SFTP**: `home311542229.1and1-data.host` · puerto 22 · usuario `acc1570798660` (cred en 1Password)

## Flujo de deploy

1. Cambios en `/Users/manueldelmonte/IET/src/`
2. `npm run build` → genera `dist/`
3. Subir archivos afectados vía sftp + nuevo CSS hash + `chmod 644` archivos + `chmod 755` directorios
4. `git push origin main`

OJO: cada build puede cambiar el hash del CSS (`_astro/Layout.XXXX.css`). Subir siempre el nuevo CSS o la página se ve sin estilos.

## Hecho en sesión 2026-06-02 / 2026-06-05

### Contenido
- Obras: filtros eliminados, h1 y descripción actualizados; "Tetris · Amadeus" → "Amadeus"
- Nuevas tecnologías: tagline "Automatización de Edificios y Optimización Energética"; texto intro revisado por cliente (Natalia)
- Quiénes somos: "radioenlaces" → "soluciones de movilidad eléctrica, instalaciones fotovoltaicas y gestión inteligente de edificios"
- Certificados: card de fabricantes eliminada; grid 2-col → 1-col; foto técnico IET añadida a la derecha con duotono + hover color
- Servicios: "subcontratar" eliminado de descripción; `seoTitle` por servicio
- Aviso legal: emails → `lopd@iet.es` (antes `administracion@iet.es`)
- Imágenes: hospital y datacenter reemplazadas por versiones de mayor calidad

### UX / Mobile
- Header: `.btn` movido a `@layer components` (fix overflow horizontal en iOS)
- Header: CTA solo en `lg:` (desktop), móvil solo logo + hamburger
- Hero image: `aspect-[3/2]` → `aspect-square` en móvil; h1 `clamp(1.75rem,7.5vw,2.25rem)` fluido
- Marquee: `-webkit-mask-image` añadido (logos invisibles en iOS Safari sin prefijo)
- IntersectionObserver: threshold `0.15` → `0.05`, rootMargin `0px` (reveals en móvil)
- Hover duotono: todas las imágenes con overlay rojizo revelan color en 500ms al hacer hover

### SEO / Legal
- JSON-LD expandido, sitemap con lastmod, llms.txt, Service+FAQ schema por servicio
- Banner cookies RGPD: tarjeta flotante `.tray` con Aceptar/Rechazar + localStorage

### Deploy
- Subida completa a producción vía lftp + sftp
- Permisos corregidos: `chmod 755` directorios, `chmod 644` archivos (IONOS crea dirs con 700)
- HTTPS activo: SSL activado desde panel IONOS; redirección HTTP→HTTPS en `.htaccess`

## Pendientes

1. **Verificar coordenadas geo** — JSON-LD tiene aprox. 40.459, -3.703 (C/ Armenteros 15, 28039)
2. **Web3Forms**: si email de contacto sigue llegando a Gmail → crear key nueva con `administracion@iet.es`
3. **Security headers** — Content-Security-Policy, HSTS, X-Frame-Options (requiere acceso a config Apache en IONOS)
4. **Fotos reales de obra** — sustituir stock de `public/images/` por fotos reales del cliente

## Links rápidos

- Producción: https://iet.es
- Preview: https://iet-preview.surge.sh
- Repo: github.com/mdelmontep/IET
- Local: `/Users/manueldelmonte/IET` · `npm run dev` (4321) · build: `npm run build`
- Formulario Web3Forms: key `b81370cc`, recipient `administracion@iet.es`
