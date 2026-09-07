---
title: el suelo de carga de una máquina compartida no lo ponen las sesiones
date: 2026-09-07
source: facturaia
tags: [rendimiento, agentes, medicion, atribucion]
---
Tres sesiones cediéndose turnos de máquina para una suite que fallaba por timeout
(8.219, 8.126, 8.123 ms contra un tope de 8.000). La atribución era «nos pisamos»,
y la corrida verde se leyó como «alguien se apartó».

Medido con **cero gates corriendo**: load de fondo **7,97**, swap al **85-91 %**
(8.400-8.700 MB de ~9-10 GB), ~134 MB libres. Los dos mayores bloques eran
`fseventsd` (2,4-4,1 GB, 25 días vivo) y la VM de Colima (1,26 GB) — y la Postgres
compartida vive **dentro** de esa VM, así que la contención de la BD y la del host
son el mismo problema visto desde dos sitios. La única corrida verde no coincidió
con que una sesión soltara, sino con el único momento en que el host bajó a 5,88.

Regla: antes de negociar turnos, **medir el suelo con nadie corriendo**. Si el load
en vacío ya es alto, el turno reparte solo la parte que ponéis vosotros y la
ventana que esperáis no existe. Y `ps` no basta: dice **quién compila**, no por qué
la máquina va lenta — con el host paginando hay que mirar `sysctl vm.swapusage` y
`vm_stat`. Dos sesiones midiéndolo por separado convencen; una parece una excusa.
Ver [[contencion-cpu-entre-sesiones-parece-bug-ui]].
