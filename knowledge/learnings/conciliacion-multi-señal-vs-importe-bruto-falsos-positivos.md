---
title: Conciliación bancaria — match multi-señal vs importe bruto (falsos positivos)
date: 2026-05-24
source: FacturaIA mig 155 + Sprint conciliación v3
tags: [facturaia, conciliacion, matching, scoring]
---

# Conciliación bancaria — match multi-señal vs importe bruto

Auto-matchear movimientos bancarios con facturas usando solo importe + ventana de fechas es una invitación a falsos positivos. Sobre todo en sandboxes/staging con seed data, pero también en producción con clientes que tienen importes redondos comunes (199€, 500€, 1.200€).

## Síntoma típico

Usuario crea factura nueva 1.270 €. La encuentra ya marcada como `cobrada` 5 segundos después, sin haber subido ningún extracto bancario. ¿Por qué? Existía un movimiento sandbox/seed del mismo importe en los últimos 30 días. Trigger lo enganchó.

Para el autónomo es un "magic trick" en su contra: el sistema "decide" cosas que él no entiende.

## Patrón correcto: score multi-señal con umbral alto para auto-confirmar

Cada par `(movimiento, factura candidata)` se puntúa por varias dimensiones independientes:

| Señal | Peso | Por qué |
|---|---:|---|
| Importe exacto (≤0,50€) | +40 | Sigue siendo la señal más fuerte |
| Importe cercano (≤tol) | +15 | Sub-señal, no auto |
| Fecha exacta (±3d) | +10 | Co-ocurrencia temporal |
| Fecha cercana (±15d) | +5 | Acepta retrasos típicos |
| Nº factura en descripción | +35 | Casi imposible coincidencia random |
| Nombre contraparte en desc | +25 | Token fuzzy match primer palabra |
| CIF/NIF en descripción | +30 | Identifica entidad sin ambigüedad |
| Regla aprendida (ver abajo) | +30 | Memoria de confirmaciones previas |

**Auto-confirmar solo con score ≥ 80**. Sub-80 → sugerencia para confirmar. Sub-30 → ignora.

El caso típico del falso positivo se desploma: importe 40 + fecha 5 = 45 → "posible" → sugerencia, no auto-confirma. Cierra el bug.

## Por qué importan TODAS las señales

Una sola señal fuerte no basta. El nº factura puede aparecer en el concepto bancario por casualidad (movimientos de devolución a otra factura con número parecido). El nombre puede coincidir parcialmente (gestoría que paga a 5 clientes distintos). La fecha exacta puede ser ruido si hay varios movimientos el mismo día. La combinación de 2-3 señales es lo que da certeza.

## Anti-pattern: tolerancia configurable como única defensa

El sistema viejo permitía configurar `tolerancia_euros` desde 1 hasta 100. Bajar la tolerancia reducía falsos positivos pero también perdía matches reales (retrasos en cobros, comisiones bancarias). Es un trade-off perdido: importe nunca debería ser señal única, da igual la tolerancia.

## Conexión

Va con [[reglas-aprendidas-de-confirmacion-manual-cierra-loop-aprendizaje]] — el sistema aprende qué patrones nuevos son válidos cuando el usuario confirma manualmente.
