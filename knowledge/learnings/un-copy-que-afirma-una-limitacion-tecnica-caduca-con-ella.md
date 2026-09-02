---
title: un copy que afirma una limitación técnica caduca con ella, y nadie lo actualiza
date: 2026-09-02
source: facturaia
tags: [copy, docs, candado, albaranes, deuda]
---
Un texto de usuario que dice «esto solo se puede hacer después de X» describe el código de ese día. Cuando otro PR levanta la limitación, el texto sigue vivo: nadie grepa el copy al cambiar la lógica.

Caso (facturaia, 28-ago → 2-sep): el 409 `albaranes_sin_cruzar` decía «cruza los albaranes una vez aprobada la factura». El #2281 (mig 768, cruce previo desde la bandeja) lo invirtió: ahora se cruza ANTES, y tras aprobar sin cruzar AL014 ya no deja corregirlo. El diálogo llevaba cinco días mandando al cliente por el camino que ya no existía; ADR-030 y dos hallazgos de QA afirmaban lo mismo.

Patrón (#2396):
- el copy que nombra una condición técnica sale de una función con la condición como parámetro (`mensajeAlbaranesSinCruzar(albaranes, desde)`), y las superficies que la citan (título del panel) comparten constante.
- un test lee la FUENTE de los emisores (grep de la constante en los ficheros que devuelven el 409) para que un copy hardcodeado vuelva a fallar.
- al invertir un comportamiento, grep del texto viejo en `src/`, manuales y ADR: la doc que afirma lo contrario es peor que ninguna.
