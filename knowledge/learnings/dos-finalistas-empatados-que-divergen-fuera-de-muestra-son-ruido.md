---
title: dos finalistas empatados en búsqueda que divergen fuera de muestra son la firma del ruido
date: 2026-08-02
source: claude-code-session
tags: [metodo, estadistica, validacion, tuning]
---

Test de diagnóstico barato, y no hace falta que ninguno "pase": mira los **dos mejores**
candidatos de la búsqueda.

- Si en búsqueda están **empatados** (indistinguibles) y fuera de muestra se van a lados
  **opuestos**, tu capa de búsqueda está dominada por ruido. El ganador no ganó: le tocó.
- Y entonces el que sí sobrevive tampoco vale, porque salió del mismo sorteo.

Caso real (cryptobruj): 79 combinaciones; top-2 con +0,0535 y +0,0531 en búsqueda; en
reserva, +0,0826 y −0,0645. La misma moneda cayendo de dos lados.

Por qué importa: mirar solo al ganador invita a racionalizarlo ("el RSI alto tiene sentido,
la tendencia tiene inercia"). El segundo clasificado es el control que desmonta el cuento
sin necesidad de discutirlo. Guarda siempre el ranking completo, no solo el máximo.

Ver [[el-argmax-de-una-mitad-medido-en-la-otra-dice-si-la-superficie-existe]] ·
[[celdas-libres-del-diseno-2x2-son-dos-reservas-mas-sin-gastar]]
