---
title: el canónico apuntaba al único host sin certificado, y todas las señales le siguieron
date: 2026-09-17
source: ecobox
tags: [seo, nginx, traefik, dokploy, despliegue]
---
La web la servía el apex; `site`/`SITE.url` declaraban el `www`, que **nunca se dio de alta en
Dokploy** → Traefik no le pidió certificado y no conectaba. Un dato mal puesto desalineó todo
lo derivado: canonical, `og:url`, JSON-LD, las 23 URLs del sitemap y la URL del verificador.

El agujero no era el `www`, era el `map $host` del `X-Robots-Tag`: eximía del `noindex` a ese
host muerto, así que el único que servía la web caía en el `default` y **pidió `noindex` desde
el primer deploy sin que nadie lo viera en meses**.

Por qué no saltó: el verificador moría en `self-signed certificate` **antes** de comprobar nada
(falso rojo crónico que se lee como «el dominio aún no apunta»), y su check daba
`ok noindex, follow` porque esperaba encontrarlo — medía el host equivocado.

Patrón: **exime por el host que un visitante puede abrir**, no por el canónico sobre el papel, y
que la URL del verificador salga del MISMO dato que el canonical para que un host muerto ponga
algo rojo. Cambiar el canónico con la web en `noindex` cuesta cero; después es migración de
dominio. Ver [[dos-locales-del-mismo-negocio-van-en-un-graph-con-branchof]].
