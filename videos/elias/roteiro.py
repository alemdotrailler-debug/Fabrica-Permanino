"""Roteiro: Elías, nivel por nivel (Crónicas del Pergamino) — template GIBI.
Base: 1 Reyes 17–19; 2 Reyes 1:8; 2 Reyes 2:11; Santiago 5:17 (Reina-Valera).
Marcações: [nome] = fala de personagem (voz própria + balão); {FUEGO}/{BOOM} = onomatopeia + impacto.
"""

CH = [
 (None, [
  ("e0", "Eres Elías. Estás en la cima de un monte, frente a cuatrocientos cincuenta profetas de un dios falso. Tienes un altar empapado en agua. Y le acabas de pedir a Dios que mande fuego del cielo."),
  ("e0b", "Vas a vivir la vida de Elías nivel por nivel. Y el nivel más difícil no es el del fuego. Es el que viene después. Quédate hasta el final."),
  ("e0b", "Y si te gustan estas historias, suscríbete ahora y activa la campanita. Cada semana abrimos un nuevo pergamino."),
 ]),
 (("NIVEL 1", "El profeta que nadie esperaba"), [
  ("e1a", "Nivel uno. El profeta que nadie esperaba. Eres Elías, el tisbita, de Galaad. Vistes ropa de pelo y un cinto de cuero. Nadie sabe de dónde saliste."),
  ("e1b", "Israel tiene un rey llamado Acab. Y una reina llamada Jezabel, que llenó el país con el culto a Baal, el dios de la tormenta y de la lluvia."),
  ("e1c", "Entras al palacio. Miras al rey a los ojos. Y le dices. [elias] Vive el Señor, Dios de Israel, que no habrá lluvia ni rocío en estos años, sino por mi palabra."),
  ("e1c", "Un profeta solo acaba de declararle la guerra al dios de la lluvia. Con una sequía."),
 ]),
 (("NIVEL 2", "Fugitivo"), [
  ("e2a", "Nivel dos. Fugitivo. Dios te dice que te escondas junto al arroyo de Querit. Bebes del arroyo. Y la comida llega volando."),
  ("e2b", "Los cuervos te traen pan y carne por la mañana, y pan y carne por la tarde. El hombre más buscado del reino tiene comida a domicilio."),
  ("e2c", "Pero no llueve. Y un día, el arroyo se seca."),
 ]),
 (("NIVEL 3", "Huésped de una viuda"), [
  ("e3a", "Nivel tres. Huésped de una viuda. Dios te manda a Sarepta, en tierra de Sidón. La tierra de Jezabel. La encuentras recogiendo leña. Le pides agua, y un pedazo de pan."),
  ("e3b", "[viuda] Vive el Señor tu Dios, que no tengo pan cocido. [viuda] Solo un puñado de harina y un poco de aceite. [viuda] Lo voy a cocinar para mí y para mi hijo, lo comeremos, y moriremos."),
  ("e3b", "Y tú le pides lo imposible. [elias] No tengas temor. [elias] Hazme primero a mí una torta pequeña. [elias] Porque la harina no se acabará, ni el aceite faltará, hasta el día en que el Señor mande lluvia."),
  ("e3c", "Ella obedece. Y la harina no se acaba. Día tras día. Un puñado de harina alimenta a tres personas en plena sequía."),
  ("e3d", "Un día, el hijo de la viuda se enferma y muere. Lo tomas en tus brazos, lo subes a tu cuarto y clamas a Dios. Y el niño vuelve a respirar."),
  ("e3d", "[viuda] Ahora sé que eres varón de Dios, y que la palabra del Señor en tu boca es verdad."),
 ]),
 (("NIVEL 4", "Retador"), [
  ("e4a", "Nivel cuatro. Retador. Pasan más de tres años sin lluvia. Y Dios te dice: ve y preséntate ante Acab, porque voy a mandar lluvia."),
  ("e4b", "El rey te ve y te dice. [acab] ¿Eres tú el que turba a Israel? [elias] Yo no he turbado a Israel, sino tú, porque dejaste los mandamientos del Señor y seguiste a los baales."),
  ("e4c", "Y lanzas un desafío. Reúne a todo Israel en el monte Carmelo. Y a los cuatrocientos cincuenta profetas de Baal."),
  ("e4d", "Frente a todo el pueblo, gritas. [elias] ¿Hasta cuándo vacilaréis entre dos opiniones? [elias] Si el Señor es Dios, seguidle. [elias] Y si Baal, id en pos de él. Y el pueblo no responde ni una palabra."),
  ("e4d", "Antes de seguir: si llegaste hasta aquí, comenta de qué lado habrías estado tú ese día. Dale like si la historia te está atrapando. Y suscríbete, porque viene fuego."),
 ]),
 (("NIVEL 5", "Duelo en el Carmelo"), [
  ("e5a", "Nivel cinco. Duelo en el Carmelo. Las reglas son simples. Dos bueyes, dos altares, nada de fuego. El dios que responda con fuego, ese es el Dios verdadero."),
  ("e5b", "Los profetas de Baal van primero. Desde la mañana hasta el mediodía gritan. [profetas] ¡Baal, respóndenos! Y saltan alrededor del altar. Nadie responde."),
  ("e5c", "Al mediodía, tú te burlas. [elias] Gritad más fuerte, porque es un dios. [elias] Quizá está ocupado, o de viaje. [elias] O tal vez duerme, y hay que despertarlo."),
  ("e5d", "Ellos gritan más fuerte. Hasta la tarde. Y no hay voz. No hay respuesta. No hay nadie que escuche."),
 ]),
 (("NIVEL 6", "Fuego del cielo"), [
  ("e6a", "Nivel seis. Fuego del cielo. Ahora es tu turno. Tomas doce piedras, una por cada tribu de Israel, y reconstruyes el altar del Señor. Cavas una zanja alrededor."),
  ("e6b", "Y pides algo que nadie entiende. Cuatro cántaros de agua sobre el altar. Otra vez. Y otra vez. Doce cántaros de agua, en plena sequía. El agua corre alrededor del altar y llena la zanja."),
  ("e6c", "Te acercas y oras. Sin gritar. Sin saltar. [elias] Señor, Dios de Abraham, de Isaac y de Israel, sea hoy manifiesto que tú eres Dios en Israel. [elias] Respóndeme, Señor, respóndeme."),
  ("e6d", "{FUEGO} Y cae fuego del Señor. Consume el holocausto, la leña, las piedras y el polvo. Y lame el agua que estaba en la zanja."),
  ("e6e", "Todo el pueblo cae sobre su rostro. [pueblo] ¡El Señor es el Dios! [pueblo] ¡El Señor es el Dios!"),
  ("e6f", "Subes a la cima del Carmelo y oras con el rostro entre las rodillas. Siete veces mandas a tu criado a mirar el mar. La séptima vuelve con una noticia. [criado] Veo una nube pequeña, como la palma de la mano de un hombre, que sube del mar."),
  ("e6g", "{BOOM} Y el cielo se oscurece. Viento. Y una lluvia enorme. Después de más de tres años, vuelve a llover. Y tú corres delante del carro del rey, todo el camino hasta Jezreel."),
 ]),
 (("NIVEL 7", "El héroe que quiso morir"), [
  ("e7a", "Nivel siete. El héroe que quiso morir. Jezabel se entera de todo. Y te manda un mensaje. [jezabel] Así me hagan los dioses, si mañana a esta hora no he acabado con tu vida."),
  ("e7a", "El hombre que hizo caer fuego del cielo, sale huyendo por una sola amenaza."),
  ("e7b", "Caminas un día entero por el desierto. Te sientas bajo un enebro. Y le pides a Dios. [elias] Basta ya, Señor. [elias] Quítame la vida, que no soy mejor que mis padres."),
  ("e7c", "Te duermes. Y un ángel te toca. [angel] Levántate y come. A tu lado hay un pan cocido sobre piedras y una vasija de agua. Comes, bebes, y te vuelves a dormir."),
  ("e7c", "El ángel vuelve. [angel] Levántate y come, porque largo camino te resta. Dios no te dio un sermón. Te dio pan, agua y descanso."),
  ("e7d", "Con la fuerza de esa comida caminas cuarenta días y cuarenta noches, hasta Horeb, el monte de Dios. Y te metes en una cueva."),
  ("e7e", "{BOOM} Un viento fuerte parte los montes y quiebra las peñas. Pero el Señor no está en el viento. Después, un terremoto. Pero el Señor no está en el terremoto. Después, un fuego. Pero el Señor no está en el fuego."),
  ("e7f", "Y después del fuego, un silbo apacible y delicado. Un susurro. Y ahí estaba Dios."),
  ("e7f", "El Dios que respondió con fuego en el Carmelo, en tu peor día te habló en voz baja."),
 ]),
 (("FINAL", "El carro de fuego"), [
  ("e8a", "Tu historia no termina en una cueva. Dios te da una nueva misión y un sucesor, Eliseo. Un día, mientras caminan juntos, aparece un carro de fuego con caballos de fuego. {FUEGO} Y subes al cielo en un torbellino."),
  ("e8b", "El hombre que pidió morir bajo un enebro, nunca murió."),
  ("e8c", "Tres cosas que tu historia nos enseña. Dios te cuida incluso junto al arroyo seco, a veces con cuervos y a veces con una viuda. La fe no grita más fuerte, confía más profundo. Y hasta los héroes se cansan: cuando estás agotado, Dios no te condena, te alimenta y te susurra."),
  ("e8c", "Oremos. Señor, en mis días de fuego y en mis días de cueva, háblame. Dame tu pan, tu descanso y tu voz suave. Amén. Si crees en esto, escribe amén en los comentarios."),
  ("e8d", "Y si hoy estás bajo tu propio enebro, cansado, escribe en los comentarios: levántate y come. Alguien que lo lea lo va a necesitar."),
  ("e9", "Si esta historia te tocó, imagina vivir treinta días así. En el libro Héroes del Pergamino tienes treinta mañanas con los personajes que cambiaron la historia de la fe, por menos que un café. El link está en la descripción. Comparte este video con alguien que necesita fuerzas hoy. Suscríbete, y nos vemos en la próxima crónica."),
 ]),
]

# ---------- configuração do vídeo ----------
SLUG = "elias"
TEMPLATE = "gibi"
FORMATO = "longo"
VOZ = "em_alex"
VOZES = {"elias": "em_santa", "acab": "em_alex", "jezabel": "ef_dora", "viuda": "ef_dora", "angel": "ef_dora",
         "profetas": "em_alex", "pueblo": "em_santa", "criado": "em_alex"}
VELOCIDADE = 0.9
CORTE_SEG = 5.0
MUSICA = ["menor", "menor", "maior", "maior", "menor", "menor", "maior", "menor", "maior"]

TITULO = "Elías: 1 Hombre Contra 450 Profetas de Baal (y Cayó Fuego)"
DESCRICAO = """📖 30 días con los héroes de la fe: https://pay.kiwify.com/2YlTx14

Un solo profeta frente a 450 profetas de Baal, un altar empapado con doce cántaros de agua… y fuego del cielo. Elías detuvo la lluvia, fue alimentado por cuervos y resucitó a un niño.

Pero el nivel más difícil de su vida no fue el del fuego: fue el día en que quiso rendirse. Vive la historia de Elías como un cómic animado, nivel por nivel.

CAPÍTULOS
{CAPITULOS}

📜 1 Reyes 17–19 · 2 Reyes 2

🙏 Escribe AMÉN si Dios te levantó en tu día más cansado, y suscríbete a Crónicas del Pergamino.

📖 El libro: https://pay.kiwify.com/2YlTx14

#elias #historiasbiblicas #bibliaanimada #montecarmelo #biblia"""
TAGS = ["elías", "elias", "profeta elías", "elías y los profetas de baal", "monte carmelo", "fuego del cielo",
        "elías y jezabel", "acab y jezabel", "elías y la viuda", "carro de fuego", "historias bíblicas", "historias biblicas",
        "biblia animada", "cómic bíblico", "1 reyes 18", "héroes de la biblia", "nivel por nivel", "crónicas del pergamino"]
COMENTARIO = "¿De qué lado habrías estado ese día en el Carmelo? 👇 Y si hoy estás cansado: levántate y come. Si quieres 30 mañanas con los héroes de la fe: https://pay.kiwify.com/2YlTx14"
