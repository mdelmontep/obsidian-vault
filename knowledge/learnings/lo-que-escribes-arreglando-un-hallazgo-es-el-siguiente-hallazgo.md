---
title: lo que escribes arreglando un hallazgo es, seis veces de cada diez, el hallazgo siguiente
date: 2026-09-06
source: claude-code-session facturaia
tags: [auditoria, gate, documentacion, verificacion, metodo]
---
24 pasadas del gate de cierre sobre un PR **solo de texto** (prompts de continuación del ticket
171). **Seis bloqueantes consecutivos los introduje yo al arreglar el anterior**, y cada uno lo
cazó la pasada siguiente, no la mía:

- una lista de 4 sitios enumerada en la sección que predica «no se enumera, se remide» (el comando
  daba 12);
- conteos escritos a mano *dentro* de esa misma sección;
- «misma coda que la 4.3», apuntando a una coda que no existía;
- «la única de las tres que crea algo», refutada en su propio paréntesis;
- «crea y **aprueba** una recibida», donde la fuente decía «no aprobar»;
- **un producto inventado** (`Ostra fina n1`) para que dos frases contradictorias pareciesen
  compatibles. Era el mismo producto y la misma org: no había dos eventos.

Dos reglas, y la segunda es la cara fea de la primera:

1. **Un categórico afirmativo escrito mientras arreglas es sospechoso por construcción** — «la
   única», «los cuatro sitios», «misma X que», «siempre», «todos». Al arreglar escribes con la
   confianza del que acaba de mirar *una* cosa, y el categórico habla de *todas*. Si el documento
   ya manda un comando que reproduce la lista, el número no se escribe: se remite al comando.
2. **Un dato inventado para cuadrar una contradicción es peor que la contradicción.** La
   contradicción avisa; el dato la silencia y sobrevive a todas las pasadas siguientes porque ya
   «cuadra». Cuando dos frases propias se contradigan, la salida es reconciliar por ALCANCE
   («esta habla de lo mío, aquella de la org») o declarar una caducada — nunca inventar el hecho
   que las haría compatibles.

El coste real no fue el gate: fue que **el bucle converge igual** (`no-listo` ×3 → `con-reservas`
×2 → `no-listo` ×3 → `listo`) y eso disfraza de progreso lo que es un maker que se ensucia a sí
mismo. La señal de que estás en esto: el hallazgo de la pasada N+1 cita una frase que no existía
en la pasada N.

Emparenta con [[el-gate-escrito-justo-despues-del-arreglo-mide-cero-casos]] (el arnés escrito en
caliente) y con [[una-lista-de-hallazgos-caduca]].
