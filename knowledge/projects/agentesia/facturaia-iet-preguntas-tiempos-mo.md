---
title: IET — preguntas sobre los tiempos de mano de obra
date: 2026-08-07
updated: 2026-08-07
source: sesión TuFacturaIA 07-ago-2026, auditoría de 6 agentes + repaso de cifras
tags: [facturaia, iet, obras, cliente, pendiente-respuesta]
---

# IET — tiempos de mano de obra y coste/hora

**Estado 07-ago: 3 de las 4 preguntas resueltas. Queda que ella dé el coste real
por hora y el OK al salto de precio.** Contexto técnico en [[facturaia]] y en
`docs/architecture/gotchas.md` §Obras. Sus decisiones del 2-ago están en
`docs/architecture/obras/decisiones-migracion-iet.md`.

## Dónde quedó cada pregunta

| # | Pregunta | Estado |
|---|---|---|
| 1 | Las dos escalas de tiempo | **Resuelta por nuestra cuenta.** No son dos criterios: son 7 tipos con un +5 % exacto. Solo falta que confirme si le suena esa subida |
| 2 | ¿Sigue usando WAPI? | **Contestada.** Sigue trabajando allí pero **no ha subido materiales ni tarifas** desde el backup → el volcado del 21-jul sigue vigente |
| 3 | 16,36 €/h: ¿coste-empresa o bruto? | **Resuelta contra el ERP: es BRUTO de convenio.** Ver abajo. El coste-empresa **no existe en WAPI**, se lo tiene que dar ella |
| 4 | Aviso del salto de precio | **Listado entregado** (294 materiales). Pendiente su OK |

## El coste/hora: de dónde sale y por qué es bruto

**Fuente**: `dbo.TRABAJO`, los partes de trabajo. Una fila por instalador y día,
con 12 columnas de horas y sus 12 precios/hora **congelados en el parte** (`p_*`).
Se usan esos, no la tarifa de hoy: son el dato histórico real.

**Limpieza obligatoria**: hay líneas donde las «horas» son euros de subcontrata
con precio 1,00. En 2022-23 son 38 líneas con 53.111 «horas» falsas frente a 451
líneas con 25.361 horas reales. Excluir `precio = 1`.
→ [[precio-unitario-1-00-marca-una-cantidad-que-son-euros]]

**Serie limpia** (`labo_norm_mad`, laborable normal en Madrid, el 90 % del volumen):
2018 15,68 · 2019 14,64 · 2020 14,70 · 2021 15,32 · **2022 16,52** · **2023 16,23**.
Media ponderada 2022-23 = **16,36 €/h**. De ahí salían los «16,35».

**Solo lo componen 7 tarifas**, y la que domina es TECNICO INSTALADOR a 15,31 €/h
(11.781 h, el 46 %); el resto son oficiales de 1ª entre 16,15 y 19,74, un OFICIAL
3ª a 12,70 y TECNICO DE GESTION a 19,35.

**Que es bruto de convenio, no coste-empresa**, con dos pruebas en el propio ERP:
- `TIPO_PERSONAL` tiene `PEON 1º AÑO` a **5,50 €/h**: como coste-empresa es
  imposible, no llega al SMI. Como salario de convenio antiguo, encaja.
- En **33 de los 63 tipos con precio**, la hora extra es exactamente la normal
  **×1,5** — el recargo del convenio. Un coste-empresa no se estructura así.

**Y el coste-empresa no está en WAPI en ninguna parte**: barrido de `sys.columns`
sobre las 1.100 tablas por `segur`, `cotiz`, `nomina`, `salario`, `bruto`, `ss` →
cero campos reales. → [[barrer-el-catalogo-de-columnas-convierte-no-lo-encuentro-en-no-existe]]

Los **21,6 €/h** que circularon son **estimación nuestra** (16,36 × 1,32 de
cotización empresarial), no un dato suyo. Etiquetarlo siempre como tal.

**Retirado**: lo de que sus tarifas están congeladas desde 2021 no se sostiene —
la serie sigue moviéndose y las tarifas se han ido tocando por tipo.

## Los dos listados que se le pasaron

**`IET-materiales-que-suben-de-precio.csv` — 294 filas.** Los que están a la vez
en su tarifa de Telematel y en WAPI, y suben al añadirles el tiempo de instalación
que ya tienen allí. **Son 294, no 295**: uno (`0121000096`) ya tenía exactamente
el mismo tiempo. Total **2.152,34 €**, media 7,32 €. **Media 26,5 %, mediana
17,7 %**, máximo 245,8 %, uno desde precio cero. El «18 %» que circuló era la
mediana llamada media. Antigüedad: 176 usados de 2023 en adelante, 53 desde antes
de 2020.

**`IET-materiales-duplicados.csv` — 464 fichas en 222 grupos** (317 metidas a mano,
147 de Telematel), ordenado por grupo para que las gemelas salgan juntas, que es
como ella lo pidió. **152 llevan desde antes de 2020 sin usarse** → borrado en
bloque casi sin mirar. 199 se han usado de 2023 en adelante y esas las repasa ella.
2 sin fechar (grupos 98 y 122, referencia `LIBRE`): no tocar.

Se descartó un criterio de agrupación más laxo que daba 1.475 grupos: al ignorar
los dígitos mete cables de secciones distintas en el mismo saco.

**Las fechas de último uso** salen de 8 vías (presupuestos, unidades de obra,
pedidos, albaranes y obras), no solo de presupuestos. Cobertura 100 % en el primer
listado y 99,6 % en el segundo.

## El factor de los tiempos, verificado por regresión

Método independiente de cómo se dedujo: sobre los 44 tipos del grupo dominante,
pendiente **1,42115** con **R² = 1,000000**. Los 7 desviados están en 1,49232,
exactamente un **+5,008 %**. Ninguno de esos 7 lo usa material alguno de su org real.

## El mensaje que se le manda

Está redactado en texto plano (nada de tablas markdown: se rompen al pegar) en el
cierre de la sesión del 07-ago. Responde a los 16 €, entrega los dos listados y
pide el coste-empresa real. Lo único que se le pregunta de nuevo es si le suena
una subida del 5 % en aquellos 7 tipos.
