# -*- coding: utf-8 -*-
"""Parches de la v30 sobre un conversation flow de Centro Elphis.
Cada parche lleva su ancla y su assert: si el ancla no aparece EXACTAMENTE una vez,
aborta. Sin eso, un parche que no aplica pasa por aplicado y se publica el flow viejo."""
import json

def _sust(nodo, campo, viejo, nuevo, etiqueta):
    txt = nodo[campo]["text"] if campo == "instruction" else nodo[campo]
    n = txt.count(viejo)
    assert n == 1, f"[{etiqueta}] ancla aparece {n} veces, se esperaba 1"
    txt = txt.replace(viejo, nuevo)
    if campo == "instruction": nodo["instruction"]["text"] = txt
    else: nodo[campo] = txt

def aplicar(f, saltar=()):
    nodo = lambda i: next(n for n in f["nodes"] if n.get("id") == i)
    hechos = []

    # ── P1 · El referente de dv_nombre ────────────────────────────────────────────
    # Medido: 2/2 llamadas con relacion=familiar devolvieron "Sin nombre" (una con
    # "Diego", nombre espanol impecable, ya en v16), 1/1 con relacion=paciente devolvio
    # el nombre completo. No era un filtro de plausibilidad: la descripcion pedia el
    # nombre DEL PACIENTE, y en las llamadas de familiares ese nombre no se dice nunca.
    # El contacto de Clientify se crea con el TELEFONO de quien llama (registrar-lead ->
    # Upsert contacto -> first_name/last_name), asi que el nombre que corresponde a esa
    # ficha es el suyo. No se admite el del paciente como sustituto: seria una ficha con
    # el telefono de uno y el nombre de otro, y recepcion llamaria a Mariana por el
    # nombre de su consuegra.
    VIEJA_NOMBRE = ("Nombre y apellidos de la persona que va a ser atendida, tal como se han dicho. "
        "Si solo consta el nombre de pila, usa el nombre de pila. Si lo transcrito NO parece un nombre "
        "de persona real (una frase suelta, palabras sin sentido, algo que no encaja como nombre) o no "
        "se dio ninguno, devuelve exactamente: Sin nombre. Nunca inventes un nombre ni uses una frase "
        "de la conversacion como si lo fuera.")
    NUEVA_NOMBRE = ("Nombre y apellidos de QUIEN ESTA AL TELEFONO, tal como los ha dicho. No es el nombre "
        "del familiar del que habla: si llama por otra persona, aqui va el de quien llama, y el del "
        "paciente NO sirve como sustituto. Si solo consta el nombre de pila, usa el nombre de pila; si "
        "lo deletreo, junta las letras. Senal fiable de que es un nombre: se dijo respondiendo a la "
        "pregunta por el nombre, o precedido de me llamo, soy, mi nombre es. Acepta cualquier nombre o "
        "apellido aunque no te suene, no sea espanol o sea dificil de escribir: buena parte de quien "
        "llama es extranjera y no reconocer un nombre NO es motivo para descartarlo. Devuelve exactamente "
        "Sin nombre SOLO en dos casos: nadie dijo ningun nombre, o lo transcrito no es un nombre sino "
        "otra cosa (una frase con verbo, una peticion, una sustancia, un parentesco, un cargo u oficio, "
        "silabas sueltas o ruido de transcripcion, o un trozo de lo que acaba de decir la asistente). "
        "Ante la duda entre un nombre que no reconoces y una frase suelta, quedate con el nombre. Nunca "
        "inventes un nombre ni uses una frase de la conversacion como si lo fuera.")
    tocados = 0
    for nid in ("extract_reserva", "extract_lead"):
        for v in nodo(nid).get("variables", []):
            if v.get("name") == "dv_nombre":
                assert v["description"] == VIEJA_NOMBRE, f"[P1/{nid}] descripcion inesperada"
                v["description"] = NUEVA_NOMBRE; tocados += 1
    assert tocados == 2, f"[P1] se esperaban 2 variables dv_nombre, tocadas {tocados}"
    hechos.append("P1 referente de dv_nombre (2 nodos)")

    if "P2" not in saltar:
        # ── P2 · El doble cierre ──────────────────────────────────────────────────────
        # Medido sobre la ruta real: fn_crear_lead -> cierre (frase propia del modelo) ->
        # despedida (static_text). Dos despedidas pegadas. Las tres aristas nuevas de hoy NO
        # dispararon en esa llamada: el defecto ya existia y solo se hizo visible. El cierre
        # hablado pasa a vivir en un unico sitio, y ese sitio es static_text: nunca cuelga mudo.
        _sust(nodo("cierre"), "instruction",
            "Si el usuario dice que no necesita nada mas o se despide: despidete en una frase corta, con tus\npalabras, y transiciona a end.",
            "Si el usuario dice que no necesita nada mas o se despide: NO te despidas tu, no digas adios ni\nninguna coletilla de cierre. El cierre hablado lo dice el nodo Despedida: pasa a Despedida sin anadir nada.",
            "P2a cierre")
        _sust(nodo("cierre_cita"), "instruction",
            "Si dice que no necesita nada mas o se despide: despidete SIEMPRE en voz alta con una frase corta y\ncalida antes de terminar. Nunca cuelgues en silencio.\nFRASE (no la cambies): \"Perfecto. Gracias por llamar a Centro Elphis, cuidate.\"",
            "Si dice que no necesita nada mas o se despide: NO te despidas tu ni digas ninguna frase de cierre.\nEl cierre hablado lo dice el nodo Despedida: pasa a Despedida sin anadir nada.",
            "P2b cierre_cita")
        _sust(nodo("preguntas"), "instruction",
            "Si se despide o dice que no necesita nada mas, despidete en una frase y transiciona a end.",
            "Si se despide o dice que no necesita nada mas, NO te despidas tu: pasa a Despedida sin decir nada mas, que ese nodo dice el cierre.",
            "P2c preguntas")
        # El nodo consentimiento: se toca SOLO la coletilla final. La formula RGPD literal
        # queda intacta y el gate lo verifica palabra por palabra.
        _sust(nodo("consentimiento"), "instruction",
            "que puede volver a llamar cuando quiera, y despidete.",
            "que puede volver a llamar cuando quiera, y pasa a Despedida sin despedirte tu.",
            "P2d consentimiento")
        # El finetune_example que ENSENA a despedirse en cierre (y ademas apunta a un
        # transition_node_id "end" que ya no es destino de ese nodo). Se quita por estructura,
        # no por string con coma: un sed sobre JSON minificado lo dejaria invalido.
        fe = nodo("cierre").get("finetune_examples") or []
        antes = len(fe)
        nodo("cierre")["finetune_examples"] = [e for e in fe if e.get("transition_node_id") != "end"]
        assert len(nodo("cierre")["finetune_examples"]) == antes - 1, "[P2e] no se quito exactamente 1 ejemplo"
        hechos.append("P2 doble cierre (4 nodos + 1 finetune_example)")

    def _gp(viejo, nuevo, etiqueta):
        n = f["global_prompt"].count(viejo)
        assert n == 1, f"[{etiqueta}] ancla aparece {n} veces en global_prompt, se esperaba 1"
        f["global_prompt"] = f["global_prompt"].replace(viejo, nuevo)

    _esc1 = "" if "P3c" in saltar else ("\n"
        '   SALIDA cuando la linea no da: si tras dos intentos no has conseguido entender NADA de lo que\\n   necesita, esa condicion ya no se puede cumplir. Se lo dices sin rodeos y le pides nombre y\\n   telefono para que el equipo le devuelva la llamada.\\n   Pero eso es el ultimo recurso, no el primero: si le entiendes lo que pregunta, se lo RESPONDES.\\n   Que algunos turnos lleguen rotos no es motivo para derivarle mientras el resto se entienda, y\\n   cortar a alguien que esta preguntando por su tratamiento para pedirle el telefono es peor\\n   servicio que la linea mala.')
    _esc2 = "" if "P3c" in saltar else ("\n"
        'Con la linea, primero responde y solo despues deriva: mientras entiendas lo que te pregunta, se lo\\ncontestas aunque algunos turnos lleguen rotos. Solo si tras dos intentos no has sacado nada en\\nclaro dejas de pedirle que repita —eso no se arregla insistiendo—, le dices que no se le oye bien,\\ny le pides nombre y telefono para que le llamen.')
    if "P3" not in saltar:
        # -- P3 - La exploracion necesita condicion de PARADA, no menos exploracion ------
        # Miguel dijo tres veces que solo queria conocer el centro y se le pregunto tres
        # veces, las dos ultimas casi con la misma frase. La unica parada que habia
        # ("si contesta con dos palabras o esquiva") no cubre a quien contesta CLARO que no
        # hay nada. Ajuste propio sobre lo propuesto: pedir informacion NO cierra nada
        # mientras aun no sepas a que viene — la mejor llamada del dia (Mariana) empieza
        # justo con "me gustaria pedir unas cuantas informaciones".
        _sust(nodo("intake"), "instruction",
            "Si contesta con dos palabras o esquiva, no insistas: una pregunta y sigues. Si se explaya, dejale\n   terminar y no le interrumpas con el nombre.",
            "Si contesta con dos palabras o esquiva, no insistas: una pregunta y sigues. Si se explaya, dejale\n   terminar y no le interrumpas con el nombre.\n   Esta exploracion se CIERRA en cuanto pase cualquiera de estas tres cosas: te dice que no hay\n   nada concreto o que solo quiere conocer el centro; te devuelve en lo esencial la misma respuesta\n   que ya te habia dado; o esquiva por segunda vez. Ojo: pedir informacion no cierra nada mientras\n   todavia no sepas a que viene — mucha gente, sobre todo familiares, arranca pidiendo informacion\n   y a los dos turnos te esta contando lo importante. Cierras cuando ya sabes a que viene Y te dice\n   que no hay mas." + _esc1 + "\n   Cerrada la exploracion, no vuelves a preguntarle por el motivo en el resto de la llamada: ni mas\n   adelante, ni al hilo de otra cosa, ni con otras palabras. La misma pregunta desde otro angulo\n   sigue siendo la misma pregunta, y que suene distinta no la convierte en nueva. Si el saca por su\n   cuenta una sustancia, una conducta o un malestar concreto, ahi si vuelves a explorar.\n   Mientras SIGA habiendo contenido nuevo en lo que te cuenta, la exploracion es lo mejor que haces:\n   cada pregunta nace de su ultima respuesta, nunca de una lista.",
            "P3a intake parada")
        # La seccion Registro del global_prompt empuja a preguntar sin parada y aplica en
        # TODOS los nodos: la tercera pregunta a Miguel nace ahi, ya en info_cita. Parchear
        # solo el nodo dejaria el mismo agujero abierto.
        _gp("tus palabras: pregunta por su caso, por si ha recibido tratamiento antes, o por si quiere que le\nexpliques las opciones, pero NO tienes formulas fijas para hacerlo y no debes repetir la misma\nconstruccion en dos llamadas.",
            "tus palabras: pregunta por su caso, por si ha recibido tratamiento antes, o por si quiere que le\nexpliques las opciones, pero NO tienes formulas fijas para hacerlo y no debes repetir la misma\nconstruccion en dos llamadas.\nEstas preguntas valen mientras quede algo que no te haya contado. Una vez que ya sabes a que viene,\nsi te dice que no hay un problema concreto o que solo quiere conoceros, o si te repite en lo esencial\nuna respuesta que ya te dio, dejas de preguntarle por su caso durante el resto de la llamada. No lo\nreintentes con otras palabras ni desde otro angulo: la misma pregunta reformulada sigue siendo la\nmisma, y hacerla dos veces se oye como que no le has escuchado." + _esc2 + "",
            "P3b global Registro")
        hechos.append("P3 parada de la exploracion + salida por linea ininteligible")

    if "P4" not in saltar:
        # -- P4 - El aviso de coste: sigue siendo obligatorio, deja de tener turno fijo ---
        # Sale palabra por palabra porque esta ENTRECOMILLADO en info_cita, y atracado al
        # turno del nombre porque el global lo ancla a "antes de reservar o recoger datos".
        # RIESGO ASUMIDO Y A MEDIR: se cambia un disparador posicional (que funciona, aunque
        # suene a guion) por una condicion de contenido, que es blanda. La base ya es mala:
        # 3 de las 6 llamadas que llegan a consentimiento lo piden sin haber avisado del
        # coste. Si la medicion no mejora ese contador, estos dos parches se revierten.
        _gp("- Es un centro PRIVADO. Antes de reservar o recoger datos: menciona que los tratamientos tienen un coste, y que la primera visita es gratuita.",
            "- Es un centro PRIVADO. Que los tratamientos tienen un coste y que la primera visita es gratuita es\ninformacion que la clinica quiere que se de SIEMPRE, y tiene que estar dicha antes de que la persona\nconfirme que quiere reservar. No es opcional. Lo que no tiene es turno asignado ni formula: lo dices\ndonde encaje con lo que estais hablando —al explicar como se trabaja un caso como el suyo, al hablar\nde modalidades, al responder por precios, al ofrecerle la visita— y con palabras distintas cada vez.\nPROHIBIDO soltarlo en el mismo turno en el que confirmas su nombre o le das las gracias por el: ahi\nse oye como un cambio de tema. Dicho una vez, no se repite.",
            "P4a global coste")
        _sust(nodo("info_cita"), "instruction",
            'Cuando sea el momento: "Ten en cuenta que somos un centro privado, los tratamientos tienen un coste. La primera visita con nuestro director es completamente gratuita."',
            "Que el centro es privado, que los tratamientos tienen un coste y que la primera visita es gratuita tiene que estar dicho ANTES de pasar a Consentimiento: si vas a pasar y todavia no se lo has dicho, diselo ahi mismo. No es una frase que soltar: hilalo con lo que estes explicando, con tus palabras y distintas cada llamada. Si ya se lo has dicho, no lo repitas.",
            "P4b info_cita coste")
        hechos.append("P4 aviso de coste sin turno fijo (global + info_cita)")

    if "P5" not in saltar:
        # -- P5 - El catalogo de sustancias es para reconocer, no para recitar ------------
        # A Miguel, que habia dicho tres veces que no tenia nada concreto, le enumero cinco.
        _gp("Adicciones tratadas: alcohol, benzodiacepinas, opioides, cocaína, THC, MDMA, ludopatía, sexo, pornografía, compras, trabajo, pantallas, redes, codependencia. NO nicotina.",
            "Adicciones tratadas: alcohol, benzodiacepinas, opioides, cocaína, THC, MDMA, ludopatía, sexo, pornografía, compras, trabajo, pantallas, redes, codependencia. NO nicotina. Esta lista es para que las reconozcas y para confirmar si te preguntan por una en concreto: NO se enumera en voz alta. Si la persona ya te ha dicho su motivo, hablas del suyo y de ninguno mas. Si te ha dicho que no tiene ninguno concreto y solo quiere conoceros, recitarsela sobra. Solo si te preguntan abiertamente que se trata aqui, contestas que adicciones a sustancias y tambien conductuales, con dos ejemplos como mucho.",
            "P5 catalogo")
        # Y el nodo intake, que es quien manda "aportar algo" cuando no hay material: que lo
        # que aporte salga de lo que EL conto, no un repaso general del centro.
        _sust(nodo("intake"), "instruction",
            "la siguiente intervención APORTA algo antes de volver a preguntar: qué hacéis en el centro, en qué consiste la primera visita, que de esto se sale.",
            "la siguiente intervención APORTA algo antes de volver a preguntar, y lo que aportas sale de lo que EL acaba de contarte: en qué consiste la primera visita, cómo se trabaja un caso como el suyo, que de esto se sale. Nunca un repaso general del centro ni un recorrido por todo lo que se trata aquí: eso es un folleto, no le habla a él, y suena peor cuanto menos te haya contado.",
            "P5b intake folleto")
        hechos.append("P5 catalogo de sustancias (global + intake)")

    # -- P6 - El turno del nombre deja de ser la percha de lo pendiente --------------
    # "Encantada, <Nombre>." sale literal en 7 de 15 llamadas, y en 5 de esas 7 arrastra
    # detras una obligacion (el coste o el permiso). Sin esto, P4 quita la formula pero
    # el salto de tema sigue.
    _gp('- Cuando te diga su nombre, repitelo UNA vez dentro de tu siguiente frase, con naturalidad:\n  "Encantada, Marta." Si te corrige, usa el corregido y no vuelvas a insistir.',
        "- Cuando te diga su nombre, usalo UNA vez dentro de tu siguiente frase, con naturalidad y sin\n  formula fija: no empieces siempre igual. Si te corrige, usa el corregido y no vuelvas a insistir.\n  Ese turno es para acusar el nombre y SEGUIR con lo que estabais hablando. No lo uses de percha\n  para colgar detras una obligacion pendiente —el aviso de coste, el permiso, la oferta de cita—:\n  esas cosas tienen su propio momento y pegadas ahi se oyen como un cambio de tema.",
        "P6 turno del nombre")
    hechos.append("P6 el nombre deja de ser percha (global_prompt)")

    return f, hechos
