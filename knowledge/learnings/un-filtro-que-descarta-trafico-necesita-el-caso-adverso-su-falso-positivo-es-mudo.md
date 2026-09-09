---
title: un filtro que descarta tráfico necesita el caso adverso — su falso positivo es mudo
date: 2026-09-09
source: centro-elphis
tags: [testing, clasificadores, llm, cobertura]
---
El bot de voz clasifica `no_paciente` (comercial, proveedor, prensa, equivocado) y esa etiqueta
**ni crea deal ni avisa a nadie** — es justo lo que se buscaba: que un comercial no ensucie el
embudo. La suite medía ese lado: "Saúl el comercial NO entra". Nadie medía el otro.

Los dos errores del clasificador no cuestan lo mismo ni se ven igual:
- **falso negativo** (comercial entra) → un deal que alguien cierra a mano. Visible.
- **falso positivo** (un familiar acaba en `no_paciente`) → la llamada se pierde y **no queda
  rastro en ningún sitio**, precisamente porque esa rama se diseñó para no avisar. Mudo.

**Toda rama que suprime efectos necesita un caso que demuestre que no se traga lo que no debe.**
El caso adverso es el que más se parece al descartado sin serlo: aquí, una señora que empieza
hablando de la mutua y del seguro de la empresa de su marido y solo al tercer turno dice que
bebe. Verificado: sale `handoff`, no `no_paciente`.

Y al escribirlo, cuidado con el criterio: el primero que redacté prohibía decir "eso aquí no lo
llevamos" y marcaba como fallo el comportamiento correcto (aclarar el equívoco y **seguir**
atendiendo). Un caso adverso mal redactado mide tu redacción, no el sistema.
