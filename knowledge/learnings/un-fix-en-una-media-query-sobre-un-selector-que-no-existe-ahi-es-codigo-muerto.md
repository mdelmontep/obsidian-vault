---
title: un fix en una media query sobre un selector que no existe ahí es código muerto
date: 2026-08-28
source: facturaia
tags: [css, diseno, medicion, falso-verde]
---

Cerré un hallazgo de auditoría (exceso de capas de cristal en móvil) con una regla dentro de `@media (max-width: 768px)` sobre `.table-wrap`. Compiló, pasó lint y build, tenía pinta de arreglo — y no cambiaba **nada**: por debajo de 768px la tabla se convierte en tarjetas y `.table-wrap` no se renderiza. Cero coincidencias medidas a 390px y a 700px.

**Un selector válido no es un selector presente.** El CSS no avisa de reglas que no casan con nada, así que un fix de breakpoint puede quedar como código muerto con aspecto de solución, y el hallazgo se da por cerrado sin que nadie haya medido.

**Antes de escribir un fix dentro de una media query**, sondear el DOM **a ese ancho**: abrir el viewport en 390 / 700 / 1440 y contar `document.querySelectorAll('<selector>').length`. Si sale 0 en el rango de la query, el arreglo va en otro sitio (aquí, el componente de tarjeta) o el hallazgo estaba mal localizado.

Vale igual para `:hover` en táctil, `@media print` y cualquier rama que la QA normal no visita: la rama que nadie pisa acepta cualquier cosa.

Ver [[una-piel-de-tokens-solo-alcanza-lo-que-no-esta-escrito-a-mano]] · [[nombre-de-clase-css-modules-como-string-global-es-selector-muerto-sin-error]] · [[la-maqueta-se-mide-con-el-motor-no-se-modela-sumando-anchos]]
