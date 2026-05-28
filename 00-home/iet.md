---
title: iet
date: 2026-05-27
tags: [cliente, iet, hub]
---

# IET — Instalaciones Eléctricas y de Telecomunicación

Empresa de instalaciones eléctricas y telecomunicaciones, Madrid, fundada en 1989. Proyecto actual: **rediseño completo de su web** (la antigua era WordPress 4.9 con HTTPS roto). Web nueva en Astro, estática, lista para su hosting. Punto de entrada al proyecto.

## Estado

- **Web nueva CONSTRUIDA** (2026-05-27) — Astro + Tailwind v4, estática, 15 páginas. Compila limpio. Detalle técnico: [[clientes/iet/web-iet|Web IET]]
- **Repo GitHub**: `mdelmontep/IET` (privado). Local en `/Users/manueldelmonte/IET`. **Sin commitear aún** (a la espera de OK del user).
- **Sitio antiguo**: `http://www.iet.es` (WordPress 4.9.29, tema Versatile). HTTPS roto en su servidor (error TLS). Slugs preservados en la web nueva para no perder SEO.
- **Marca**: rojo `#DA2C2B` + grises, logo de tres tiles i·e·t (en `public/logo-iet.png`).

## Próximos hitos

1. **Commit + push al repo** (NEXT) — pendiente OK del user.
2. **Activar formulario** (NEXT) — crear Access Key gratis en web3forms.com con `administracion@iet.es` → `.env` `PUBLIC_WEB3FORMS_KEY`. Hasta entonces el form avisa y no envía.
3. **Arreglar HTTPS** (NEXT) — instalar/renovar certificado (Let's Encrypt) en su Apache. Canonical y sitemap ya apuntan a `https://`.
4. **Fotos reales** (LATER) — sustituir stock de Pexels (duotono) por fotos reales de obras de IET, mismo nombre de archivo.
5. **Decidir despliegue** — el user eligió "su hosting actual" (Apache): `npm run build` → subir `dist/`. Alternativa permanente: conectar repo a Netlify/Cloudflare Pages.

## Bloqueos / esperando a terceros

- Web3Forms key, certificado TLS y fotos reales dependen del cliente/user.

## Links rápidos

- Local: `/Users/manueldelmonte/IET` · build `npm run build` → `dist/`
- Repo: github.com/mdelmontep/IET (privado)
- Web vieja: http://www.iet.es (solo HTTP)
- Detalle técnico web: [[clientes/iet/web-iet|Web IET — stack, diseño, despliegue]]
- Contexto cliente: [[clientes/iet/index|IET — contexto]]
