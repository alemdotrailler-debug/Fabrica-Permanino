"""Roteiro: Gedeón, nivel por nivel (Crónicas del Pergamino) — template GIBI.
Base: Jueces 6–8; Hebreos 11:32 (Reina-Valera).
Marcações: [nome] = fala de personagem (voz própria + balão); {FUEGO}/{BOOM}/{CRASH} = onomatopeia + impacto.
"""

CH = [
 (None, [
  ("g0", "Eres Gedeón. Es medianoche. Estás en lo alto de una colina, mirando un campamento enemigo que parece no tener fin. Ciento treinta y cinco mil soldados, según suman los números de Jueces. Y tú tienes trescientos hombres. Sin espadas. Solo una trompeta y un cántaro de barro con una antorcha escondida adentro."),
  ("g0b", "Vas a vivir la vida de Gedeón nivel por nivel. Y te aviso: el mejor momento de esta historia es cuando Dios te quita soldados. Quédate hasta el final."),
  ("g0b", "Y si te gustan estas historias, suscríbete ahora y activa la campanita. Cada semana abrimos un nuevo pergamino."),
 ]),
 (("NIVEL 1", "El que se escondía"), [
  ("g1a", "Nivel uno. El que se escondía. Eres Gedeón, hijo de Joás, de la tribu de Manasés. Israel lleva siete años bajo el dominio de Madián, por haber dejado a Dios."),
  ("g1b", "Cada vez que los israelitas siembran, llegan los madianitas, junto con los amalecitas y los hijos del oriente. Vienen con sus tiendas y sus camellos, que eran innumerables. Y como langostas, lo devoran todo."),
  ("g1c", "Tu pueblo ya no vive en sus casas. Se esconde en cuevas, en cavernas y en lugares fuertes de los montes. Y tú, ¿dónde estás? En un lagar, sacudiendo trigo a escondidas. Un lagar es donde se pisa la uva, un lugar bajo y oculto, para que Madián no vea ni un grano."),
  ("g1d", "Y entonces aparece alguien sentado bajo la encina. Es el ángel del Señor. Y te dice. [angel] El Señor está contigo, varón esforzado y valiente."),
  ("g1d", "Mírate. Estás escondido, con trigo en las manos y miedo en el pecho. Y Dios te llama valiente. Dios no te habla por lo que eres hoy. Te habla por lo que vas a ser."),
 ]),
 (("NIVEL 2", "El menor de la casa"), [
  ("g2a", "Nivel dos. El menor de la casa. Y tú respondes con una queja honesta. [gedeon] Señor mío, si el Señor está con nosotros, ¿por qué nos ha sobrevenido todo esto? [gedeon] ¿Dónde están todas sus maravillas?"),
  ("g2a", "El ángel no discute. Te dice. [angel] Ve con esta tu fuerza, y salvarás a Israel. [angel] ¿No soy yo quien te envía?"),
  ("g2b", "Pero tú buscas excusas. [gedeon] ¿Con qué salvaré yo a Israel? [gedeon] Mi familia es la más pobre de Manasés, y yo soy el menor en la casa de mi padre."),
  ("g2b", "Y Dios te responde con una sola promesa. [angel] Yo estaré contigo, y derrotarás a los madianitas como a un solo hombre."),
  ("g2c", "Aun así quieres una prueba. Traes un cabrito y panes sin levadura. El ángel te dice que los pongas sobre una peña. Toca la carne con la punta de su bastón. {FUEGO} Sube fuego de la peña, consume todo, y el ángel desaparece."),
  ("g2d", "Tienes miedo de morir, porque has visto a un ángel cara a cara. Pero Dios te dice. [angel] Paz a ti. [angel] No tengas temor, no morirás. Y levantas allí un altar. Lo llamas, el Señor es paz."),
 ]),
 (("NIVEL 3", "Derribador de ídolos"), [
  ("g3a", "Nivel tres. Derribador de ídolos. Esa misma noche, Dios te da un trabajo incómodo. Derribar el altar de Baal que es de tu propio padre, y cortar la imagen de Asera que está al lado."),
  ("g3b", "Con diez de tus siervos lo haces. De noche, porque tienes miedo de tu familia y de la gente del pueblo. {CRASH} Cae el altar. Cae el ídolo. Y levantas en su lugar un altar al Señor."),
  ("g3c", "Por la mañana, todo el pueblo exige tu muerte. [pueblo] ¡Entréganos a tu hijo para que muera! Pero tu padre Joás, el mismo que cuidaba el altar de Baal, se pone entre ellos y tú. [joas] ¿Vais a defender vosotros a Baal? [joas] Si es dios, que se defienda él mismo."),
  ("g3c", "Desde ese día te llaman Jerobaal. Que Baal contienda contra él. Y Baal nunca contendió."),
  ("g3d", "Antes de seguir: si te está gustando esta historia, dale like. Y cuéntanos en los comentarios: ¿cuál es el ídolo que a ti te cuesta derribar? Y suscríbete, que viene la parte más extraña."),
 ]),
 (("NIVEL 4", "Pidiendo señales"), [
  ("g4a", "Nivel cuatro. Pidiendo señales. Madián, Amalec y los hijos del oriente cruzan el Jordán y acampan en el valle de Jezreel. El Espíritu del Señor viste a Gedeón. Tocas la trompeta, y tu pueblo, el que se escondía, empieza a juntarse detrás de ti."),
  ("g4b", "Pero tienes dudas. Y le pides algo a Dios. [gedeon] Pondré un vellón de lana en la era. [gedeon] Si solo el vellón se moja con el rocío, y toda la tierra queda seca, sabré que me vas a usar para salvar a Israel."),
  ("g4b", "Te levantas temprano. El vellón está empapado, y la tierra seca. Lo exprimes, y sale un tazón lleno de agua."),
  ("g4c", "Y todavía pides más. [gedeon] No te enojes conmigo, Señor. [gedeon] Solo una vez más. [gedeon] Ahora que el vellón quede seco, y que toda la tierra tenga rocío."),
  ("g4c", "Y esa noche Dios lo hizo. Otra vez. Dios no se ofendió de tus preguntas. Tuvo paciencia con tu miedo."),
 ]),
 (("NIVEL 5", "Demasiados soldados"), [
  ("g5a", "Nivel cinco. Demasiados soldados. Reúnes a treinta y dos mil hombres junto a la fuente de Harod. Ya casi te sientes listo. Pero Dios te dice algo que no esperabas. [dios] El pueblo que está contigo es mucho. [dios] Si ganan así, dirán que fue por su propia mano."),
  ("g5b", "Dios te da la primera orden. Que se vaya a su casa el que tenga miedo. Y veintidós mil hombres, más de dos tercios de tu ejército, se dan la vuelta y se van. Te quedan diez mil."),
  ("g5c", "Y Dios te dice: todavía son muchos. Llévalos al agua. Y los separas según cómo beben. Los que se arrodillan para beber, a un lado. Y los que lamen el agua con la mano, llevándola a la boca, al otro."),
  ("g5d", "Cuentas. Trescientos. Solo trescientos hombres de treinta y dos mil. Y Dios te dice. [dios] Con estos trescientos hombres os salvaré, y entregaré a los madianitas en tus manos."),
  ("g5d", "Mira cómo funciona Dios. Tú contabas soldados. Dios los quitaba. Porque cuando por fin ganes, nadie podrá decir que fue por el número."),
  ("g5d", "Y ahora de verdad, escríbelo en los comentarios si alguna vez Dios te quitó algo para que dependieras más de Él. Aquí estamos para leerte."),
 ]),
 (("NIVEL 6", "El sueño del pan de cebada"), [
  ("g6a", "Nivel seis. El sueño del pan de cebada. Esa noche, Dios te dice. [dios] Levántate, desciende al campamento, porque lo he entregado en tus manos. [dios] Y si todavía tienes miedo, baja primero con tu criado Pura."),
  ("g6a", "Dios conoce tu miedo. Y no te regaña. Te da una última ayuda. Bajas en silencio. Y el valle está lleno de madianitas y amalecitas, tendidos como langostas. Sus camellos son como la arena a la orilla del mar."),
  ("g6b", "Escuchas a un soldado contándole su sueño a su compañero. [soldado] He tenido un sueño. [soldado] Un pan de cebada rodaba hasta nuestro campamento, golpeó la tienda, y la tienda cayó."),
  ("g6b", "Y su compañero le responde. [companero] Esto no es otra cosa que la espada de Gedeón, hijo de Joás, el israelita. [companero] Dios ha entregado a Madián en sus manos."),
  ("g6c", "El enemigo ya sabía tu nombre. Y ya tenía miedo de ti, mucho antes de que tú dejaras de tenerlo. Te arrodillas allí mismo y adoras. Y vuelves corriendo al campamento. [gedeon] Levantaos, porque el Señor ha entregado en vuestras manos el campamento de Madián."),
 ]),
 (("NIVEL 7", "Trompetas y cántaros"), [
  ("g7a", "Nivel siete. Trompetas y cántaros. Divides a tus trescientos hombres en tres grupos. Y le das a cada uno una trompeta, y un cántaro vacío con una antorcha adentro. Nada de espadas. Nada de lanzas."),
  ("g7b", "Y les explicas el plan. [gedeon] Miradme a mí, y haced como yo. [gedeon] Cuando yo toque la trompeta, vosotros tocad también, y gritad. [gedeon] Por el Señor y por Gedeón."),
  ("g7b", "Llegáis al borde del campamento justo al comenzar la guardia de la medianoche, cuando acaban de cambiar los centinelas. Todo está oscuro y en silencio."),
  ("g7c", "{BOOM} Y de repente, trescientas trompetas suenan a la vez. Y trescientos cántaros se rompen. Y trescientas antorchas se encienden en la oscuridad. [pueblo] ¡Por la espada del Señor y de Gedeón!"),
  ("g7d", "Y nadie se mueve. Los trescientos se quedan cada uno en su lugar, alrededor del campamento, sosteniendo la luz. Y todo el ejército madianita despierta, gritando, sin entender nada. Y echan a correr."),
  ("g7d", "Y Dios hizo que, en la confusión, cada soldado madianita volviera su espada contra su compañero. Huyeron hasta Bet-sita, y hasta la frontera. La Biblia dice que cayeron ciento veinte mil hombres de espada. Y tus trescientos no pelearon esa noche: solo sostuvieron la luz."),
  ("g7e", "Pides refuerzos y los de Efraín capturan a Oreb y Zeeb, dos príncipes de Madián. Persigues a los reyes Zeba y Zalmuna, con tus trescientos hombres cansados, pero todavía en pie. Y los alcanzas."),
 ]),
 (("FINAL", "Lo que vino después"), [
  ("g8a", "Después de la victoria, el pueblo te ofrece algo más grande que cualquier medalla. [pueblo] Gobiérnanos tú, y tu hijo, y el hijo de tu hijo. Quieren hacerte rey. Y tú respondes con una frase que casi nadie dice. [gedeon] No os gobernaré yo, ni mi hijo os gobernará. [gedeon] El Señor os gobernará."),
  ("g8b", "Pero la historia es honesta. Gedeón pidió a cada uno los zarcillos de oro del botín, y con ellos hizo un efod, un objeto sagrado, y lo puso en su ciudad. Y todo Israel se desvió detrás de él. Fue un tropiezo para Gedeón y para su casa."),
  ("g8c", "Aun así, la tierra tuvo paz cuarenta años. Gedeón murió en buena vejez. Y siglos después, el libro de Hebreos lo pone en la lista de los hombres de fe. El que se escondía en un lagar, terminó en la galería de los valientes."),
  ("g8d", "Tres cosas que tu historia nos enseña. Primera: Dios te llama por lo que serás, no por lo que eres hoy; Gedeón se escondía, y Dios lo llamó valiente. Segunda: Dios achica tu ejército para que sepas de quién es la victoria. Y tercera: tener miedo no te descalifica; Dios tuvo paciencia con las dudas de Gedeón, y la tendrá con las tuyas. Pero cuidado con lo que haces después de ganar: la victoria también se puede volver un ídolo."),
  ("g8d", "Oremos. Señor, cuando me escondo, llámame valiente. Cuando me sobran números, enséñame a confiar en ti. Y cuando gane, que no me olvide de quién fue la victoria. Amén. Si crees en esto, escribe amén en los comentarios."),
  ("g9", "Si esta historia te tocó, imagina vivir treinta días así. En el libro Héroes del Pergamino tienes treinta mañanas con los personajes que cambiaron la historia de la fe, por menos que un café. El link está en la descripción. Comparte este video con alguien que se siente pequeño hoy. Suscríbete, y nos vemos en la próxima crónica."),
 ]),
]

# ---------- configuração do vídeo ----------
SLUG = "gedeon"
TEMPLATE = "gibi"
FORMATO = "longo"
VOZ = "em_alex"
VOZES = {"gedeon": "em_santa", "angel": "ef_dora", "joas": "em_alex", "pueblo": "em_santa",
         "soldado": "em_alex", "dios": "em_alex", "companero": "em_santa"}
VELOCIDADE = 0.9
CORTE_SEG = 5.0
MUSICA = ["menor", "menor", "menor", "maior", "menor", "maior", "menor", "maior", "maior"]

TITULO = "Gedeón: 300 Hombres Contra 135.000 (y Ganó Sin Pelear)"
DESCRICAO = """📖 30 días con los héroes de la fe: https://pay.kiwify.com/2YlTx14

Trescientos hombres, trompetas, cántaros de barro y antorchas contra un ejército de 135.000. Gedeón empezó escondido en un lagar, sacudiendo trigo por miedo… y Dios lo llamó valiente.

Pero lo más sorprendente de esta historia es que Dios le quitó 31.700 soldados antes de la batalla. Vive la historia de Gedeón como un cómic animado, nivel por nivel.

CAPÍTULOS
{CAPITULOS}

📜 Jueces 6–8 · Hebreos 11:32

🙏 Escribe AMÉN si hoy te sientes pequeño y Dios te está llamando valiente, y suscríbete a Crónicas del Pergamino.

📖 El libro: https://pay.kiwify.com/2YlTx14

#gedeon #historiasbiblicas #bibliaanimada #jueces #biblia"""
TAGS = ["gedeón", "gedeon", "gedeón y los 300", "gedeón y los madianitas", "los 300 de gedeón", "vellón de gedeón",
        "jueces 6", "jueces 7", "trompetas y cántaros", "fuente de harod", "historias bíblicas", "historias biblicas",
        "biblia animada", "cómic bíblico", "héroes de la biblia", "nivel por nivel", "crónicas del pergamino"]
COMENTARIO = "¿Cuál es el ídolo que a ti más te cuesta derribar? 👇 Y si hoy te sientes pequeño: Dios te llama valiente. Si quieres 30 mañanas con los héroes de la fe: https://pay.kiwify.com/2YlTx14"
