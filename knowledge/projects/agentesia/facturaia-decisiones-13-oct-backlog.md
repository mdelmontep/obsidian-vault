---
title: facturaia-decisiones-13-oct-backlog
date: 2026-10-13
source: AgentesIA-MAdrid/facturaia (triage de 179 issues abiertos, 13-oct)
tags: [facturaia, decisiones, backlog]
---

# Decisiones de Manuel sobre el backlog (13-oct-2026)

Tomadas sobre la página de decisiones del triage (opciones sacadas de cada issue). Hub: [[facturaia]].
Pendiente de reflejar en cada issue (comentario) y de ejecutar.

- **#3431** Cambiar el NIF-IVA deja la validación VIES vieja → **A**: Trigger en clientes y proveedores que invalida VIES al cambiar nif_iva
- **#2589 #2967** La deuda pendiente: importe bruto o lo realmente cobrable → **A**: Medir la deuda en cobrable, con una sola función compartida
- **#3044** Fecha del extracto bancario: contable o valor → **A**: Fecha contable u operación siempre antes que valor
- **#2819** Un worktree nace sin .env.test y el push se aborta → **A**: Script generador, como el de .env.local, con CLI de Supabase y 1Password
- **#1815** Códigos de campaña valen para cualquier producto → **A**: El panel pide los productos al crear y se envían a Stripe en applies_to
- **#3340** Aviso de factura normal que repite un albarán pendiente → **A**: Comparar también la cantidad, no solo cliente y producto
- **#3398** Documento encolado antes de suspender queda en error → **A**: Liberar la fila como «sin cupo» mientras la org esté suspendida
- **#2843** Exención obligatoria a un 0 % no sujeto o exportación → **A**: Que pregunte al clasificador (como la importación) y a VeriFactu vaya N1/N2
- **#2317** Reprocesar una lectura mal hecha solo lo hace el superadmin → **A**: Abrirlo a todos con límite y conservando las correcciones humanas
- **#2084** «Recalcular» en declaraciones ya presentadas → **A**: Deshabilitar el botón fuera de borrador y cuadrado, y guard en el endpoint
- **#1778** Facturas de suscripción: panel de Stripe y cutover → **A**: Hacer PR 0 y cutover ya, con las preguntas de gestoría después
- **#3420** Código de proveedor del cliente en la factura → **A**: Copia fija en la factura cuando sale de albaranes de venta
- **#3448** Errores 422 en inglés en textos tipo y 114 rutas → **D**: A ahora y B aparte
- **#3423** NumberField muestra «7.5» hasta el primer toque → **A**: Prop opt-in formatearAlMontar, activada en el albarán de venta
- **#3446 #3428** Etiquetas cortadas con elipsis en el Select a 375 px → **A**: Arreglo local: etiquetas más cortas / fecha delante del nombre
- **#3419** Tablas en móvil cortadas sin pista de más columnas → **A**: scroll-fade-x y useScrollFade en esta tabla
- **#3421** El toast de error tapa Guardar en móvil → **A**: Anclar el toast arriba en móvil, con safe-area, para toda la app
- **#3422** El borrador no enseña horario ni cita de la sede → **B**: El GET devuelve en borrador horario, cita y teléfono vivos
- **#3444** Ficha inexistente responde 200 con pantalla de 404 → **A**: Aceptarlo (zona con login, sin SEO)
- **#3131** Dos sitios escriben en las sedes de cliente → **A**: Único módulo escritor en sedes/db.ts que Obras consume
- **#2877** OCR con coordenadas de cada campo para la app iOS → **A**: Añadir _boxes opcional (0-1 y página) para los campos principales
- **#2498** Los dos interruptores de la IA de conciliación están separados → **A**: Los dos controles juntos, con una frase de qué apaga cada uno
- **#2259** Aviso de deriva en el hub contradice el ADR-019 → **B**: Manda el código: enmendar ADR-019 §4 con fecha y motivo
- **#2162** Marcar importaciones con DUA e ISP nacional → **A**: Esperar al primer caso real
- **#2045** Qué campos de una pieza se escriben al crearla → **A**: Escribir la regla en manual-admin §50 o CONTEXT.md y revisar los campos
- **#3333** Dos abonos parciales dictados de la misma línea → **B**: La clave dictada pasa a cliente, línea, cantidad y devuelve
- **#3329** Línea de factura que mezcla entregas con y sin stock → **A**: Impedir en facturar que se agrupen entregas con y sin movimiento de stock
- **#3393 #3394** Fila de facturación rota: degradar o fallar entera → **A**: Degradar en ficha y lista: clientes sanos más aviso con el nº de albarán
- **#3391** Sobreservicio ya aceptado reaparece cada mes → **A**: Señal solo de lo nuevo del mes
- **#3461** Separador de miles en las cantidades → **A**: Agrupar siempre en pantallas y PDF
- **#3415** El smoke de módulos exige fiscal encendido en staging → **A**: Encender fiscal en la org de lectura y dejarlo en el seed
- **#3231** Contraste insuficiente en botones y textos de estado → **A**: --fg-on-accent distinto por tema
- **#3279** Facturar un albarán con la función apagada → **A**: Permitir facturar lo emitido con la función apagada también en la ficha
- **#3250** /cashflow ignora ?org_id= de superadmin → **A**: Respetar ?org_id= con effectiveOrgId, como las APIs
- **#3050** Importación wapi: presupuesto aceptado con total negativo → **A**: Enganchar el ajuste a su presupuesto base
- **#2972** Coste de partida sin portes, IVA no deducible ni rappels → **A**: Los cuatro, cada uno con su ADR y PR
- **#2810 #2808** Casos del art. 89.Cinco que el producto no cubre → **A**: Documentar ambos como casos que resuelve el asesor
- **#2804** Conciliar una salida del banco con un abono por devolver → **A**: Asignación de tipo devolución, candidatas con abonos y automarcado alineado
- **#2227** 91 módulos que escriben solos sin ningún test → **B**: Cubrir los 91 uno a uno
- **#1959** Revideo no compone: motor por defecto es ffmpeg → **A**: Cablear Revideo: instalar renderer y Chromium, una composición por plantilla
- **#1656 #1643** Extraer el equipo de contenido a un paquete propio → **A**: Extraerlo ahora (contenido-13)
