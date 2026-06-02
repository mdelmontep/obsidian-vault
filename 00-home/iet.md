---
title: iet
date: 2026-06-02
tags: [cliente, iet, hub]
---

# IET — Instalaciones Eléctricas y de Telecomunicación

Empresa de instalaciones eléctricas y telecomunicaciones, Madrid, fundada en 1989. Proyecto actual: **rediseño completo de su web** (la antigua era WordPress 4.9 con HTTPS roto). Web nueva en Astro estática, en preview en surge.sh.

## Estado

- **Web v3 EN PREVIEW** — `https://iet-preview.surge.sh` (surge.sh, build automático tras cada cambio desde Claude Code)
- **Repo GitHub**: github.com/mdelmontep/IET (privado, rama `main`, último commit `b43d35e`)
- **Formulario Web3Forms**: key `b81370cc` configurada, recipient `administracion@iet.es` añadido en el dashboard de Web3Forms. Funciona — OJO: si el email sigue llegando a Gmail, crear una key nueva en web3forms.com directamente con `administracion@iet.es`.
- **Deploy definitivo pendiente**: subir `dist/` al Apache de iet.es via FTP/SFTP + activar TLS (Let's Encrypt).

## Lo que está hecho en esta sesión (2026-06-02)

### Contenido
- Obras: filtros eliminados, h1 y descripción actualizados
- Nuevas tecnologías: "control de clima / calefacción" → **control de accesos / sistema KNX**
- Años en obras destacadas: Merz 2024, Nielsen 2020, WeWork 2019, Zeppelin 2018
- Clientes/referencias: clientsAll actualizado (Flulle, Korus, Lymet, Plasfoc, CBRE, Savills, STG Group, Sutega, Unen añadidos; Setel eliminado)

### Logos marquee (15, todos reales)
Tetris · Savills · CBRE · Indra · IFEMA · Prosegur · Ericsson · Jones Lang LaSalle · Lledó Iluminación · Plasfoc · Sutega · STG Group · Grupo Lymet · Unen · INSS

### SEO completo
- JSON-LD `LocalBusiness`+`ElectricalContractor`: añadidos `openingHours`, `geo` (coordenadas aprox. 28039), `hasMap`, `logo`
- Títulos de servicio con keywords: "Instalaciones Eléctricas para Empresas en Madrid y toda España · IET Instalaciones", etc.
- `Service` schema + `FAQPage` schema en cada `/servicios/[slug]/`
- Sitemap: `lastmod`, `changefreq`, `priority` por tipo de página
- `llms.txt` creado en `/public/llms.txt` para rastreadores de IA
- Audit técnico: score 81/100. Pendientes solo en producción (HTTP→HTTPS, security headers)

### Mobile / Header
- Menú móvil iOS: body-lock con `position: fixed + top: -scrollY` (fix definitivo para Safari)
- Overlay: `h-[100dvh]` para cobertura correcta al hacer scroll
- Formulario contacto primero en mobile
- Hero aspect-ratio mobile corregido

### Marquee
- Estructura refactorizada: div único `.marquee-inner` animado (antes dos `<ul>` independientes → salto visible)
- `w-max` en el inner div para cálculo correcto del `-50%`
- `loading="eager"` en todas las imágenes del marquee (antes `lazy` → logos desaparecían)
- Duración: 20s loop continuo y seamless

## Próximos hitos

1. **Deploy a iet.es** — `npm run build` → subir `dist/` al Apache por FTP/SFTP + TLS
2. **HTTP→HTTPS redirect + security headers** — configurar en Nginx/Apache/Cloudflare al desplegar
3. **Verificar coordenadas geo** — JSON-LD tiene aprox. 40.459, -3.703 (zona 28039). Verificar en Google Maps con dirección exacta C/ Armenteros 15.
4. **Fotos reales de obra** — sustituir stock de `public/images/` por fotos reales (mismo nombre de archivo, mismo duotono)
5. **Web3Forms**: si email sigue llegando a Gmail → crear key nueva con `administracion@iet.es`

## Links rápidos

- Preview: https://iet-preview.surge.sh
- Repo: github.com/mdelmontep/IET
- Local: `/Users/manueldelmonte/IET` · `npm run dev` (4321) · build: `npm run build && npx surge dist/ iet-preview.surge.sh`
- Web vieja: http://www.iet.es (WordPress 4.9, solo HTTP)
- Detalle técnico: [[clientes/iet/web-iet|Web IET — stack, diseño, despliegue]]
