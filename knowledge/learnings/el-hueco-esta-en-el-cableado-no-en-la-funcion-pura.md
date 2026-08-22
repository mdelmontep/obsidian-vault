---
title: el hueco de test suele estar en el cableado, no en la función pura que el issue nombraba
date: 2026-08-12
source: claude-code-session agh-iberica
tags: [testing, mutacion, diseno, metodo]
---
Tres veces en una sola tanda (AGH, familia `mutate:diff`): el issue pedía arreglar una **lógica**, la
lógica quedó cubierta, y la mutación destapó que el hueco real estaba en el **punto de unión**, dentro
de un `main()` que ningún test invoca.

El caso tipo: `anotarEnDiario(…, mutante)` y `writeFileSync(ruta, mutante)` como dos llamadas sueltas.
Pasar ahí el argumento equivocado **sobrevive a la suite entera** — y el efecto no era cosmético (el
diario dejaba de restituir *nunca*). El diff se lee perfecto: cada llamada es correcta por separado;
lo que está mal es que **la pareja se puede desparejar**. Eso no se ve leyendo, solo mutando el punto
de unión — no la lógica que el issue nombraba.

**El arreglo bueno no es otro test: es colapsar la pareja en un valor** que fluye (una función que
hace las dos cosas; o devolver `{a, b}` y que el consumidor lo tome entero en vez de dos parámetros).
Así el defecto es **inexpresable**. Mismo principio que derivar una whitelist de un `Record<Union,
true>` en vez de escribirla a mano.

Si el cableado no se puede cubrir porque el `main()` no es invocable: **declara en el código qué
mutación sobrevive**, con qué se cubre en su lugar (una corrida real **con contrafáctico**), y abre
issue — dejarlo en la PR no lo pone en ninguna cola.

**Desenlace (13-ago, AGH #1123): esas declaraciones se cobraron, y hacerlo invocable destapó MÁS de lo
que decían.** Se parte `main()` en «lectura de entorno» + `barrer(deps)` con los **bordes de proceso**
inyectados (el fs NO: raíz temporal real, y así lo que se escribe se mira en disco). La clave: **`barrer`
DEVUELVE el código de salida en vez de llamar a `process.exit()`** — y con eso el hook de limpieza
(`process.on("exit", …)`) **sobra**, porque existía justo para lo que un `exit()` se salta un `finally`.
El refactor que hace testeable el cableado **quita** una pieza; no es el trade de «testeable a cambio de
andamio». Baja también el `catch` del error propio al nivel invocable, o ese candado se queda fuera.

🔑 Y lo reutilizable: de los **4 supervivientes** que aparecieron, **dos eran códigos de salida** —justo
las líneas que el refactor acababa de poner al alcance de un test—. Un efecto de proceso en medio de la
lógica no sólo impide testear: **oculta cuánto hay sin testear**, porque lo que se lleva no aparece en
ninguna cuenta de cobertura. Lo que asoma al sacarlo al borde no son «unas líneas» sino decisiones
enteras (un barrido donde ningún mutante llegó a ejecutarse y aun así se podía citar como cobertura).

Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] ·
[[una-herramienta-que-se-aplica-a-su-propio-fuente-necesita-el-rescate-fuera]].

**Cuarta vez (14-ago, AGH #1158), y ahora con el porqué:** se escribieron **12 mutaciones a mano y
todas cayeron sobre las funciones puras**. El barrido automático encontró a la primera un `SIN
VÍCTIMA` en el cableado — un reparto de estados como `if/else` **dentro del bucle del driver**, cuyo
predicado se podía negar sin poner en rojo ni un test (solo lo cazaba abrir un navegador). 👉 **Una
tanda de mutaciones a mano hereda tu hipótesis; el barrido derivado del diff, no**: al elegirlas
eliges dónde crees que está el fallo, y el cableado es justo lo que no se te ocurre mutar porque
«solo pasa argumentos».

Regla práctica: **corre el barrido ANTES de escribir mutaciones a mano** y deja las manuales para lo
que él declare «sin medir» (hunks que no compilan al revertirse). Si la carpeta no está cubierta,
asume el sesgo y muta explícitamente **el paso de argumentos**: invertir dos, fijar uno, dejar caer
otro. Ese mismo día el arnés se lo hizo a sí mismo: `correr: (cmd, cwd) => correr(cmd, cwd)` se podía
revertir a la forma de **un solo parámetro** con la suite verde **y el typecheck limpio** — TS acepta
aridad menor donde se espera mayor.


**Quinta vez (15-ago noche, AGH #1055) y con un matiz nuevo: un candado ESTRUCTURAL no cubre el
cableado.** Mutando el punto de unión (`if (false)` delante de la grabación del turno) el candado de
esa misma familia salió **verde**: es un test que **lee el fuente y cuenta marcadores**, así que un
`if (false)` no mueve nada — el marcador sigue ahí. La conducta la cubrían otros tests, y con ellos
la mutación murió (`4 failed | 50 passed`).

👉 Dos lecturas, las dos útiles: *(a)* un `SIN VÍCTIMA` puede ser **selección de tests demasiado
estrecha**, no un hueco — antes de acusar, amplía a los de conducta; *(b)* un candado que asevera la
**forma** del fuente y otro que asevera la **conducta** cubren cosas distintas, y el estructural
**solo** dejaría el cableado sin vigilar el día que alguien borre los de conducta.

**Sexta vez (22-ago, FacturaIA #2115) y ya no en un arnés, sino en una feature de producto.** Un
cuadre nuevo tenía tests con dientes para la función pura y para el loader que la alimenta. El
cableado era **un `push` a la lista de salida**: `...(cuadre ? [cuadre] : [])`. Borrándolo se apaga
el aviso para el usuario — la feature entera — y pasaron las **14.872** pruebas del repo. No fue una
selección estrecha: se comprobó con la suite completa, precisamente porque filtrar por carpeta habría
dado el mismo verde por el motivo equivocado. 👉 En una feature, el cableado no es un `main()`: es
**el punto donde el resultado entra en la estructura que alguien lee**. Y el test que lo cubre tiene
que mirar la **fila persistida**, no el retorno del calculador: el bug perseguido era justo que el
valor no llegara a guardarse.
