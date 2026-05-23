---
title: 2 agentes Plan con perfil humano detectan jerga técnica en copy mejor que 1 agente "UX writing"
date: 2026-05-24
source: refactor copy cashflow v2.1 — bloque "Punto de riesgo / Ago mejora vs Jul"
tags: [agentes-paralelos, ux-writing, copy, contabilidad, autónomos]
---

## Contexto

El usuario abrió el módulo Cashflow IA y dijo literalmente *"¿punto de riesgo en el horizonte? ¿ago mejora? ¿mejora en cuanto a qué?"*. La interfaz mezclaba dos métricas (peor saldo acumulado + delta del neto mensual) en la misma tarjeta. Necesitaba una segunda opinión que **no fuera técnica**.

## Lo que hicimos

En vez de lanzar un agente genérico "UX writing critic", inventé **2 personajes humanos concretos** y los lancé en paralelo con perfiles muy distintos:

- **Lucía**: asesora contable de Valencia, 15 años hablando con autónomos en su despacho. Sabe traducir conceptos pero NO es ingeniera.
- **Marcos**: autónomo electricista de Albacete, 47 años, 22 años facturando, no sabe inglés, no usa Excel. Su mujer lleva los papeles a la asesoría.

A cada uno le di las **mismas preguntas estructuradas** ≤350 palabras. Sin coordinar entre sí.

## Resultado

**Sin haberse hablado, coincidieron en las MISMAS 5 cosas críticas**:

1. "Punto de riesgo en el horizonte" suena raro (Lucía: "parte meteorológico" / Marcos: pasa de la frase).
2. "Ago mejora 714€ vs Jul" es contradictorio cuando justo arriba pone que Ago es el peor mes.
3. Los bullets `DEMO-Nómina empleado (mensual, día 28) −1500€` son ruido — el día sí vale, lo demás sobra. Marcos: *"Día 28 sí, mensual ya lo sé yo, el menos quítalo, si pone gastos ya sé que es pa fuera."*
4. Falta acción concreta. Marcos: *"Que me diga el problema, de cuánto, y qué puedo hacer. Punto."*
5. Si el mes va bien, no mostrar el bloque rojo. Verde y a otra cosa.

**Diferencias menores** que ENRIQUECIERON la decisión:

- Lucía propuso mockup HTML completo con jerarquía visual.
- Marcos dio reacciones honestas en jerga rural (*"sigo sin cobrar"*, *"el chaval"*, *"pa el día a día me sobran"*) que descubrieron qué KPIs eliminar y cómo nombrar las cosas.

## Por qué funcionó mejor que 1 agente

Un agente "UX writing expert" tiende a:
- Recitar best-practices abstractas.
- Proponer copy elegante pero no necesariamente claro.
- Quedarse en lo teórico ("el usuario debería entender X").

Los 2 personajes humanos:
- **Convergencia honesta**: cuando 2 perfiles muy distintos coinciden sin coordinar, el hallazgo es real. Si SOLO Lucía hubiera dicho "Punto de riesgo confunde" podría ser sesgo experto. Si SOLO Marcos lo hubiera dicho podría ser "este no entiende nada". Los dos a la vez = problema real.
- **Voz aterrizada**: Marcos escribió tal cual cómo lo diría él. Ese copy es el que entra en producción ("Cuidado con agosto", "Mes más justo").
- **Cubren ángulos opuestos**: Lucía cubre "qué se entiende profesionalmente correcto", Marcos cubre "qué se entiende de verdad". Sin uno, el copy queda demasiado técnico. Sin el otro, demasiado pop.

## Patrón reusable

Cuando tengas que decidir copy para usuarios no técnicos:
1. Inventa 2 personajes humanos **concretos** (nombre, edad, profesión, contexto). No "un usuario" abstracto.
2. Hazlos opuestos en algún eje (técnico vs no técnico, urbano vs rural, joven vs mayor).
3. Dales **las mismas preguntas estructuradas** en paralelo.
4. Lo que coincide = problema real. Lo que difiere = oportunidad de balance.
5. Implementa la versión de Marcos (la del usuario real), refinada con la jerarquía de Lucía.

## Caso aplicado al cashflow

Texto antes:
```
Punto de riesgo en el horizonte
Ago: -2435 € saldo negativo previsto
⭐ IA  Ago mejora 714 € vs Jul porque:
   • DEMO-Nómina empleado (mensual, día 28) −1500€
```

Texto después:
```
⚠ Cuidado con agosto
En agosto te faltarían 2.435 € para cubrir tus gastos.
Los ingresos previstos (1.200€) no llegan para los gastos previstos (3.635€).

[Ver qué pasa en agosto ▾]
   Nómina empleado    el día 28    1.500 €
   Alquiler oficina   el día 1       650 €
   Luz (Endesa)       el día 15       85 €

QUÉ PUEDES HACER
• Adelantar el cobro de Cliente X (2.420€).
• Mover el pago de "Nómina empleado" a otro día si tu proveedor lo permite.
• Tener 2.435€ de colchón antes de agosto.
```

## Cross-ref

- `src/lib/cashflow/narrative.ts:narrativeHeadline` + `seccionHeadline` + `buildNarrativeActions` (commit `da34f6c`).
- `src/components/cashflow/cashflow-view.tsx:mes-foco-card` (mismo commit).
- [[narrative-headline-no-mezclar-saldo-acumulado-con-delta-mensual]] — la causa raíz técnica que los agentes diagnosticaron sin ver código.
