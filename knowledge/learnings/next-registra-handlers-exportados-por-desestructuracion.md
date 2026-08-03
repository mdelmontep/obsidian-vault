---
title: next registra handlers de ruta exportados por desestructuración y deriva HEAD de GET
date: 2026-08-03
source: claude-code-session
tags: [nextjs, app-router, api]
---

Comprobado contra un servidor construido con Next 16.2 (no deducido, no está claro en
la documentación):

- `export const { GET, POST, PUT } = algo()` **se registra y se sirve** igual que los
  exports uno a uno. Sirve para que un solo envoltorio devuelva varios verbos en una
  línea.
- **`HEAD` lo deriva Next de `GET`** si nadie exporta `HEAD`, y responde con las
  cabeceras de tu `GET`. Exportar un `HEAD` que devuelva 405 sobre una ruta que sirve
  `GET` es romper HTTP para cumplir un gate.
- Un verbo que la ruta no exporta lo contesta **Next** con `405` y **cuerpo vacío**: sin
  tus cabeceras, sin tu forma de error y sin dejar rastro en tu registro. Igual el `404`
  de un camino que no existe. Si el contrato de la API dice "toda respuesta lleva
  `X-Request-Id`", hay que exportar los siete verbos y añadir un comodín `[...ruta]`.
- Una carpeta con prefijo `_` (`app/api/v1/__probe`) **no se enruta**: son carpetas
  privadas. Al hacer una sonda, no le pongas guion bajo o creerás que la forma no
  funciona.
