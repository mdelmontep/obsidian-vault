---
title: WAPI — Constantes del Programa y su equivalente en TuFacturaIA
date: 2026-07-29
source: WAPI. Documentación general de Usuario (manual oficial, dic-2015) + pantalla real de IET (29-jul-2026)
tags: [facturaia, obras, wapi, iet, precios]
---

# WAPI · Constantes del Programa (tarea `GCONS`)

Complementa a `docs/architecture/obras/modelo-wapi-y-precios.md` del repo, que sigue siendo el
**autoritativo** para la fórmula. Esto es lo que añade el manual: qué hace cada constante global y
dónde vive lo mismo en TuFacturaIA.

**Copia durable del manual**: `knowledge/projects/agentesia/wapi-manual/` de este vault
(PDF escaneado, 113 pág., sin capa de texto → leer con `pdftoppm`, ver
[[pdf-escaneado-sin-capa-de-texto-renderizar-paginas-con-pdftoppm]]). Recortes de las 3 páginas
clave en `wapi-manual/paginas/`. Secciones útiles: **29-31** (materiales, fórmula de precio),
**45** (alta de presupuesto), **51** (aceptar), **54** (cierre de obra), **56-59** (facturas),
**75-78** (precio hora instalador, estadísticas), **101-102** (constantes).

## Las 12 constantes → TuFacturaIA

Los 6 primeros son los únicos que documenta el manual. Los 6 marcados **(nuevo)** se añadieron
después de 2015 y **no están documentados**: la lectura es del nombre del campo.

| Constante (valor en IET) | Qué hace | Equivalente TuFacturaIA |
|---|---|---|
| Margen Obra `36` | % de beneficio sobre la M.O. de todos los materiales. **Se congela en cada obra** al crearla (Estado de Obras muestra «el % con la que se creó») | Sin multiplicador equivalente. `obras_settings.margen_min_pct` (15) es solo **umbral de aviso** del copiloto |
| Precio Mat. `34 %` | % sobre el precio NETO de compra | `obras_settings.incremento_precio_material_pct` (**33**) |
| Precio M.O. `34 €/h` | Precio de **venta** de la hora. Multiplica `Tiempo Mano de Obra` del material (horas decimales) | `obras_settings.precio_hora_mo` (33) |
| Día Cálculo Estadísticas `15` | Día en que se LANZA el cálculo. La foto es siempre a último día del mes anterior → cambiarlo no mueve cifras | No aplica (informes en vivo) |
| Días aviso Cierre obras `35` | Obras facturadas al 100 % aún abiertas. Corre los **domingos**, avisa al gestor | `obras_settings.dias_aviso_cierre` (vacío = apagado) |
| Días aviso Inactividad `30` | Obra abierta sin apunte/pedido/factura-proveedor/factura emitida. También domingos | `obras_settings.dias_aviso_inactividad` (30) |
| Precio materiales `Mínimo` **(nuevo)** | Criterio con varios proveedores. **El manual de 2015 dice el MÁS CARO**; la pantalla real está en Mínimo, que es lo que confirmó Natalia el 17-jul | Regla FIJA `MIN(PFVC)`, no configurable |
| % IVA Defecto `21` **(nuevo)** | Valor propuesto en «IVA a aplicar» del alta de presupuesto | `organizations.default_iva_pct` |
| % Retención Facturas `0` **(nuevo)** | Retención por defecto. **No se sabe si aplica al total o a una parte** | `organizations.irpf_pct_default` |
| Pedir Id. Pedido `NO` **(nuevo)** | Obligar el nº de pedido del cliente antes de aceptar (aceptar es irreversible) | Sin bloqueo |
| Días caducidad Contraseña `30` **(nuevo)** | Caducidad de la contraseña de entrada | Sin caducidad (2FA) |
| Nº contraseñas sin repetir `2` **(nuevo)** | Historial de contraseñas vetadas | ídem |

Sin equivalente en WAPI: dieta por defecto, momento de consumo de stock, plazo y forma de pago,
nota de la Ley 15/2010.

## Preguntas abiertas para IET

1. **Precio Mat. 34 % (WAPI) vs 33 % (TuFacturaIA)** — el 33 es el validado con el catálogo real
   el 17-jul. Decidir cuál manda y alinear.
2. **Precio M.O. = 34** coincide con Precio Mat. = 34, y son magnitudes distintas (€/h vs %).
   Confirmar que 34 €/h es el precio de venta real de la hora y no un campo mal rellenado.
3. **% Retención Facturas**: alcance sin documentar. Preguntar al proveedor de WAPI antes de tocar.
4. Las **3 fechas de última modificación son 23/07/2026**: los tres multiplicadores se cambiaron el
   mismo día. Fecha de corte si algo sale raro en presupuestos recientes.

## Diferencias de comportamiento que importan

- **Recálculo**: en WAPI el precio del material se regraba al añadirle un proveedor, y un material
  ya metido en un presupuesto exige pulsar «Actualizar». En TuFacturaIA, guardar
  `obras_settings` dispara `obras_trg_recalcular_por_settings` (mig 478) y recalcula el catálogo
  entero. En los dos casos **el presupuesto ya hecho no se repone solo**.
- **Coste vs venta de la hora**: WAPI separa `Precio M.O.` (venta, constante global) de
  `Gestión Precio Hora/Instalador` (coste por categoría y tipo de hora, manual pág. 76). Es el
  mismo reparto que `obras_settings.precio_hora_mo` vs Obras → Ajustes → Tarifas de hora.

Entregable explicativo para Natalia (artifact, 29-jul):
https://claude.ai/code/artifact/75f8cad9-c3bd-4c9f-8236-c465e8727584

Ver [[facturaia]] · [[iet]] · [[la-copia-durable-de-una-fuente-efimera-se-hace-el-mismo-dia-o-no-se-hace]]
