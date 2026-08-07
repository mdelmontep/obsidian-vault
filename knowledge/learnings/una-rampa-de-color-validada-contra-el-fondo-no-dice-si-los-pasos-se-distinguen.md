---
title: una rampa de color validada contra el fondo no dice si los pasos se distinguen entre sí
date: 2026-08-07
source: claude-code-session
tags: [diseno, color, accesibilidad, dataviz]
---

Rampa ordinal de 6 etapas: validé cada paso contra el fondo (≥3:1, todos pasaban de sobra) y
di la paleta por buena. Manuel miró la pantalla y dijo que no se distinguían. **ΔE 6,3 entre
contiguos, sobre un suelo de 15** — validé la propiedad equivocada. Contra-el-fondo dice si
SE VE; paso-contra-paso dice si se DISTINGUE. Son dos comprobaciones y hacen falta las dos.

Causa: la rampa variaba sólo luminancia dentro de un tono. Fix: **rotar el tono a lo largo de
la rampa** (la luminancia lleva el orden, el tono lleva la separación — es lo que hacen viridis
y familia). 6,3 → 11,3.

**Y el techo se mide, no se supone**: con 6 pasos obligados todos a 3:1 contra el fondo, tono
monótono y croma sin saltos, el máximo es ΔE ~11. Escribirlo evita que alguien pierda una tarde
persiguiendo el 15.

**Trampa del optimizador**: al maximizar ΔE numéricamente salió azul→naranja→azul→rojo (ΔE 39)
y luego, al fijar el tono, un croma en zigzag (ΔE 18). Cumplía lo que escribí y destruía lo que
el número medía. **La restricción que no escribes es la que explota.** Aquí faltaban «tono
monótono» y «croma sin saltos» — o sea, «que siga pareciendo una rampa».

Medir siempre sobre el fondo REAL de la página (`#f8f8fa`), no sobre blanco puro: dos valores
míos calculados contra blanco caían por debajo del mínimo al pintarse. Ver
[[verificar-aa-sobre-glass-componer-capas-alpha]].
