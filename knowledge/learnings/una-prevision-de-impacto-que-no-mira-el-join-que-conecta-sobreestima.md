---
title: una previsión de impacto que cuenta filas sin mirar el JOIN que las conecta sobreestima
date: 2026-08-03
source: claude-code-session
tags: [migraciones, datos, adr, facturaia, metodo]
---

El ADR-obras-008 anunciaba, en negrita y como consecuencia asumida, que los
**11.595** materiales sin marca de una sandbox subirían de precio al dejar de
heredar el descuento genérico. Al aplicar, las aserciones de la migración
dijeron **0**.

El cero era correcto. Esa organización tiene 7.174 filas de descuento y **cero
enlaces material-proveedor**, y un material solo cobra el descuento *a través*
de su enlace. Nunca lo estuvieron heredando: ya estaban marcados «sin preparar».
La previsión contó las dos puntas (materiales sin marca, filas de descuento) sin
comprobar la tabla intermedia que las une.

**Método, que es lo que vale:** un resultado que sale mejor de lo previsto se
investiga igual que uno peor. «Salió bien» tapa un bug tan bien como «salió
mal» — aquí podría haber significado que la resolución nueva no se estaba
aplicando en absoluto, y el síntoma habría sido idéntico.

Al estimar impacto sobre datos, contar **por el camino real de lectura** (con el
JOIN), no por las tablas de los extremos. Y corregir el ADR con lo medido: una
predicción falsa que se queda escrita se cita después como si fuera un hecho.
