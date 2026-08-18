---
title: un experimento que mide algo contra sí mismo da el 100 % — y el 100 % es la señal, no el resultado
date: 2026-08-18
source: obsidian-vault
tags: [metodo, verificacion, evals, metricas]
---

**Caso.** Backtest para saber cuántas notas nuevas tenían ya un duplicado en el vault. Salió **100 %**. Era falso: cada nota seguía en el índice, así que se encontraba **a sí misma**. Al excluirla y mirar solo notas anteriores a su fecha, el número real era **14 %**.

**La regla.** Un resultado perfecto o redondo en un experimento propio es motivo de sospecha, no de celebración. Dos preguntas antes de creerlo:
1. ¿El sujeto medido está dentro del conjunto contra el que se mide? → excluirlo.
2. ¿Se está comparando contra información posterior al momento que se simula? → acotar por fecha.

**Segunda capa, más silenciosa.** Aunque el experimento sea correcto, si las consultas de prueba **salen del propio documento** heredan su vocabulario y el resultado sale inflado. La literatura de recuperación lo tiene medido: las colecciones sintéticas son sistemáticamente más fáciles que las reales (arXiv 2405.07767). Sirve para **comparar dos sistemas** con el mismo protocolo; no para afirmar una cifra absoluta.

**Fix.** Antes de interpretar, un control negativo: si con la pieza clave desactivada el experimento da lo mismo, no estaba midiendo eso.

Ver [[un-control-negativo-que-no-discrimina-invalida-el-test-entero]] · [[el-instrumento-devuelve-cero-sin-decir-que-no-ha-medido]]
