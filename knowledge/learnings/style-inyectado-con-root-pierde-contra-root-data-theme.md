---
title: Un <style> con :root pierde contra :root[data-theme] y escribe CSS inerte
date: 2026-08-03
source: FacturaIA — color de marca sembrado en SSR
tags: [css, cascada, especificidad, ssr, verificacion]
---

Mover la aplicación de un token de **estilo inline** a una **hoja de estilos** cambia quién gana
la cascada, y ahí se pierde silenciosamente. `element.style.setProperty()` gana a cualquier
selector; una regla `:root{--x:…}` puntúa (0,1,0) y **pierde** contra el
`:root[data-theme="light"]{--x:…}` (0,2,0) donde suelen vivir los tokens de tema. Resultado: el
valor llega al DOM, se ve en el inspector y **no tiene ningún efecto**.

Arreglo sin `!important` ni depender del orden de las hojas: repetir el selector —
`:root:root:root` (0,3,0). Solo hace falta en los tokens que el tema **también** declara; las
variables de entrada nuevas, que nadie más define, van bien con `:root`.

Lo caza únicamente leer el **valor computado** en un navegador
(`getComputedStyle(document.documentElement).getPropertyValue('--x')`). Los unitarios validaban la
cadena generada y seguían verdes con el bug delante: medían la salida de la función, no el efecto.

Del mismo episodio, un falso negativo: `expect(locator).toContainText()` sobre un `<style>`
devuelve `''` porque mide texto RENDERIZADO y una hoja de estilos no renderiza. Para su contenido,
`await locator.textContent()`.

Ver [[token-de-relleno-no-sirve-como-token-de-texto]] · [[camino-critico-sin-smoke-se-pudre-meses]]
