---
title: iet
date: 2026-05-30
tags: [cliente, iet, hub]
---

# IET — Instalaciones Eléctricas y de Telecomunicación

Empresa de instalaciones eléctricas y telecomunicaciones, Madrid, fundada en 1989. Proyecto actual: **rediseño completo de su web** (la antigua era WordPress 4.9 con HTTPS roto). Web nueva en Astro, estática, en preview en Netlify. Punto de entrada al proyecto.

## Estado

- **Web v3 ENVIADA Y EN PREVIEW** (2026-05-30) — Astro + Tailwind v4, 15 páginas, build limpio. En Netlify: **https://illustrious-kulfi-1661d9.netlify.app** (Drop manual, lo refresca el user arrastrando `dist/` cada iteración).
- **Repo GitHub**: github.com/mdelmontep/IET (privado, rama `main`, 5 commits, todo pusheado).
- **Identidad visual** (iteración 3, inspirada en `iet-soluciones.lovable.app`): rojo brand `#E31C1C` · ink navy `#151C28` · dark navy `#1A202E` para header/footer/bandas. Logo nuevo **compacto** i·e·t (200×58). Marquee de clientes con **20 logos reales** (Wikipedia SVG + 3 wordmarks).
- **Cambios fundamentales respecto a v1**: header y footer DARK, CTA final como **banda roja full-width** (estilo referencia), bento de servicios reorganizado (Electricidad banda horizontal sin huecos), página de Obras con 36 entradas reales filtrables por tipo / provincia / año (sin imágenes por obra), contraste global subido.
- **Sitio antiguo**: `http://www.iet.es` (WordPress 4.9.29). Slugs preservados, redirect del slug de privacidad. Detalle técnico: [[clientes/iet/web-iet|Web IET]].

## Próximos hitos

1. **Activar formulario Web3Forms** (NEXT) — crear Access Key gratis en web3forms.com con `administracion@iet.es` → poner en `.env` como `PUBLIC_WEB3FORMS_KEY`. Hasta entonces el form muestra aviso y no envía.
2. **Arreglar HTTPS en Apache** (NEXT) — instalar/renovar certificado (Let's Encrypt) en su servidor. Canonical y sitemap ya apuntan a `https://www.iet.es`.
3. **Fotos reales de obra** (LATER) — sustituir las fotos de stock de Pexels (en `public/images/`, en duotono rojo) por fotos reales que pase la propiedad.
4. **Decidir despliegue definitivo** — el user eligió "su hosting actual" (Apache): `npm run build` → subir `dist/`. Alternativa permanente: conectar repo a Netlify/Cloudflare Pages para auto-deploy en cada push (lo hace en 2 clics).

## Histórico (iteraciones)

- **2026-05-30** copy: titular de sectores → "Trabajamos para realizar y cubrir todas las necesidades de nuestros clientes". Certificaciones: fuera Siemon, Brand-Rex, R&M, Krone; dentro KNX, Leviton, DALI. *(commit `98c30ca`)*
- **2026-05-30** v3 tema dark inspirado en `iet-soluciones.lovable.app`: rojo a `#E31C1C`, ink a navy `#151C28`, header/footer dark navy, CTA final reconvertida a **banda roja full-width**, nuevo `.btn-white` para CTAs sobre rojo. *(commit `5a9d1d2`)*
- **2026-05-29** logos reales de clientes (en lugar de fotos de Wikipedia): refiltrado por archivos con "logo" en el nombre y priorizando SVG. Marquee a color con `scale(1.10)` al hover. *(commit `c0691c3`)*
- **2026-05-29** v2: logo compacto i·e·t (200×58), contraste global subido, bento sin huecos (Electricidad horizontal), obras sin imágenes, marquee con 20 logos. *(commit `953186b`)*
- **2026-05-27** primer push real del proyecto al repo `mdelmontep/IET`. *(commit `1467a42`)*
- **2026-05-27** rediseño inicial: 15 páginas, sistema de diseño, SEO, formulario Web3Forms, imágenes duotono. *(commit base)*

## Links rápidos

- Repo: github.com/mdelmontep/IET
- Local: `/Users/manueldelmonte/IET` · `npm run dev` (4321) · `npm run build` → `dist/`
- **Preview deploy**: https://illustrious-kulfi-1661d9.netlify.app (Drop manual; refrescar arrastrando `dist/` al panel Deploys del mismo sitio)
- Web vieja: http://www.iet.es (solo HTTP)
- Detalle técnico: [[clientes/iet/web-iet|Web IET — stack, diseño, despliegue]]
- Contexto cliente: [[clientes/iet/index|IET — contexto y servicios]]
