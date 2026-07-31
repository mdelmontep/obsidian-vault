---
title: una prohibición escrita en un comentario merece medirse antes de aceptarla
date: 2026-07-31
source: claude-code-session facturaia
tags: [metodo, deuda-tecnica, verificacion, producto]
---
El gemelo del comentario que afirma una invariante: el que declara que algo **no se puede
arreglar**. Se lee como una decisión ya tomada por alguien con más contexto, y congela el
bug indefinidamente sin que nadie vuelva a mirarlo.

Caso FacturaIA (e5dc74e7). `textos-tipo-block.tsx` decía: *«Aquí no se arregla el de notas:
eso cambiaría documentos que ya se están emitiendo»*. Razonamiento correcto — y falso en los
datos: en prod, de 1.415 facturas con notas, **0 tenían un salto de línea**, y de esas 1.415
solo 76 eran propias (las otras 1.339 son `registro_externo`, PDFs de terceros que ni pasan
por esas plantillas). Alcance real del cambio «peligroso»: **cero documentos**. Una consulta
de 30 segundos desbloqueó un bug de cara al cliente que llevaba meses documentado como
intocable.

Regla: ante «no se toca porque afectaría a X», **contar cuántos X hay** antes de aceptarlo.
Y al arreglarlo, reescribir el comentario: si no, el siguiente vuelve a creérselo. Cuidado
además con el numerador: cuenta solo las filas que **ese** código renderiza, no todas las de
la tabla. Ver [[un-comentario-que-afirma-una-invariante-es-una-deuda-de-test]] ·
[[comentario-que-declara-una-formula-deliberada-solo-cubre-su-mitad]]
