---
title: IET — preguntas sobre los tiempos de mano de obra
date: 2026-08-07
source: sesión TuFacturaIA 07-ago-2026, auditoría de 6 agentes
tags: [facturaia, iet, obras, cliente, pendiente-respuesta]
---

# Preguntas a Natalia (IET) sobre los tiempos de mano de obra

**Estado: redactado el 07-ago-2026, pendiente de enviar y de respuesta.**

Salen de la auditoría que retiró la normalización de la unidad y la copia del
catálogo. Contexto técnico en [[facturaia]] y en `docs/architecture/gotchas.md`
§Obras. Las decisiones que ella ya tomó están en
`docs/architecture/obras/decisiones-migracion-iet.md`.

## Por qué se pregunta cada cosa

| Pregunta | Qué desbloquea | Si no responde |
|---|---|---|
| 1. Las dos escalas de tiempo | Normalizar el tiempo a horas reales | No se puede normalizar. El campo sigue mintiendo en la UI, pero los precios siguen bien |
| 2. ¿Sigue usando WAPI? | Saber si el volcado del 21-jul está vigente | Lo que se cargue puede nacer con meses de retraso |
| 3. 16,35 €/h: coste-empresa o bruto | Poner `obras_settings.coste_hora_mo` | El coste previsto de la mano de obra sigue a 0 y marcado como no fiable (mig 652) |
| 4. Aviso del salto de precio | Aplicar el §5 ya aprobado (415 materiales) | No se toca su catálogo |

La 1 es la que manda: sin ella no se normaliza, y sin normalizar el número de la
3 tampoco se puede escribir (habría que dividirlo por un factor que no se sabe).

## El mensaje, tal como se le manda

> Asunto: Cuatro dudas sobre los tiempos de instalación
>
> Hola Natalia,
>
> Estamos preparando la carga de los tiempos de mano de obra y nos han salido
> cuatro dudas. La primera es la importante, las otras tres son rápidas.
>
> Antes de nada, para que estés tranquila: los precios que estás usando ahora son
> correctos. Nada de esto afecta a lo que has facturado ni a los presupuestos que
> ya tienes hechos.
>
> **1. Los tiempos de instalación llevan dos escalas distintas**
>
> En vuestro programa antiguo hay una lista de tiempos de instalación, y muchos se
> llaman por el tiempo que representan. Al abrirlos vimos que el número que tienen
> guardado dentro no coincide con su nombre:
>
> - El que se llama "TIEMPO 1 HORA" tiene guardado 1,49
> - El que se llama "TIEMPO 0,5 HORAS" tiene guardado 0,71
> - El que se llama "TIEMPO 10 HORAS" tiene guardado 14,21
> - El que se llama "TIEMPO 100 HORAS" tiene guardado 142,15
>
> Si todos estuvieran multiplicados por el mismo número, sería fácil de corregir.
> El problema es que no lo están. Los que están escritos en plural van
> multiplicados por 1,42, y los que están en singular por 1,49. Son dos criterios
> distintos conviviendo en la misma lista.
>
> ¿Te suena a qué puede deberse? Se nos ocurren tres posibilidades:
>
> - Un cambio de convenio o de tarifa en alguna época
> - Dos formas de contar que se usaron en momentos distintos
> - Que se metieran mal en su día y nadie lo viera, porque los precios salían bien
>   igualmente
>
> Lo preguntamos porque queremos dejar esos tiempos en horas de verdad, para que
> veas "media hora" donde ponga media hora. Sin saber a qué corresponde cada
> escala, corregir una nos dejaría mal la otra.
>
> **2. ¿Sigues dando de alta cosas en el programa antiguo?**
>
> La copia que tenemos es del 20 de julio. Si has seguido metiendo materiales o
> unidades de obra allí desde entonces, lo pasaríamos con ese retraso, y
> preferimos evitarlo.
>
> **3. Lo que os cuesta una hora de instalador**
>
> De vuestra copia de seguridad sale una media de 16,35 euros por hora en 2022 y
> 2023. No es una tarifa: sale de los partes de trabajo reales de vuestros
> instaladores, cruzando las horas que imputaron con lo que se le pagaba a cada
> uno. Son 455 partes y unas 25.680 horas.
>
> Lo que no sabemos es si esa cifra es lo que os cuesta a vosotros el instalador,
> con la Seguridad Social incluida, o si es el bruto que cobra él. Lo buscamos por
> todo el programa y no lo dice en ningún sitio. Si fuera el bruto, el coste real
> para vosotros rondaría los 21,6 euros la hora.
>
> Es un dato importante porque es el que usa la aplicación para deciros el margen
> que os deja cada partida.
>
> **4. Un aviso antes de tocar nada**
>
> Tenéis 415 materiales que están a la vez en vuestra tarifa de Telematel y en el
> programa antiguo. Como acordamos, mantendríamos el precio de la tarifa y les
> añadiríamos solo el tiempo de instalación, que es lo que les falta.
>
> El efecto es que 284 de ellos van a subir de precio: un 18 % de media, y alguno
> hasta tres veces. No es un error. Es que ahora mismo esos materiales se están
> presupuestando como si instalarlos no costara nada.
>
> Si prefieres verlo antes, te pasamos la lista con el precio de ahora y el que
> quedaría.
>
> Un saludo

## Datos de respaldo, por si pregunta

- **Las dos familias**: 44 tipos con factor 1,4204 (2.568 materiales) y 7 con
  1,4917 (346). Más `TIEMPO 1250 HORAS` = 1000, que es la partida «VARIOS PARA
  OFERTAS DE 10000 EUROS» y ahí el número son euros.
- **El backup**: hecho el 20-jul-2026 a las 23:50 en `IETPDC\SERVERERP`, leído de
  la cabecera del propio fichero. El volcado a la aplicación fue el 21-jul, así
  que la copia contiene todo lo del backup.
- **El 16,35 €/h**: `dbo.TIPO_PERSONAL` × `dbo.TRABAJO`, ponderado por horas,
  2022-2023. Serie anual: 13,1 (2015) → 14,6 (2019) → 16,5 (2022) → 16,2 (2023).
  Se excluyó el 74 % del volumen bruto porque eran euros de subcontrata metidos
  en la columna de horas a 1,00 €/unidad.
- **El salto de precio de los 415**: 284 con tiempo en el origen, +2.108,95 € en
  total sobre el precio unitario, factor medio 1,182 y máximo 3,46.
