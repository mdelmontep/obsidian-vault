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

**Y el suelo contaminado no solo estorba: falsea los umbrales que derives de él**
(7-sep, tarde). Con `fseventsd` a 98-102 % de CPU y 1,73 GB durante 25 días, la
carga en reposo era **7,43 sin un solo gate corriendo**. De una tabla medida así se
dedujo un umbral —«verde con load 5-6»— y se propagó a tres sesiones como si fuera
una propiedad del test. No lo es: **es dónde queda la carga cuando el demonio ya se
ha servido.** La escala de la tabla seguía siendo buena (sus filas se separan por
contención real); lo falso era el cero, y como el cero es el que fija el margen, el
error se propagó justo a la conclusión que importaba: cuánto aire tiene el caso.
Un umbral calibrado sobre un cero contaminado **no viaja**, y deja de valer sin que
nadie se entere. Antes de derivar un número de una tabla, medir el reposo.

**Corolario (11-sep): medir el suelo no basta, hay que separar admisión de duración.**
Con el suelo ya medido, tres sesiones atribuyeron un pre-push de 70 min a la contención
(load 17 real) y al semáforo. El log decía que la espera de admisión máxima fue **1 s**:
la cola no era el problema y el load, siendo cierto, no era la causa. Un load alto es
compatible con cero espera. Ver [[el-suelo-de-un-semaforo-explica-quien-entra-no-cuanto-tarda]].
