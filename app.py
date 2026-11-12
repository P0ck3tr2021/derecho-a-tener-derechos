# ==================================================
# BAJO LA PIEL
# Juego educativo sobre derechos para tatuadores
# Basado en la serie "Derechos. Son tuyos. Defiéndelos."
# de Espacios Abiertos y el Centro de Periodismo Investigativo
# ==================================================
import os
import unicodedata
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
try:
    from streamlit_image_coordinates import streamlit_image_coordinates
    HAY_CLICK = True
except ImportError:  # falta la librería: el juego sigue funcionando con botones
    HAY_CLICK = False

# --------------------------------------------------
# 1. Configuración general
# --------------------------------------------------
st.set_page_config(
    page_title="Bajo la piel",
    page_icon="🖋️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

URL_PROYECTO = "https://espaciosabiertos.org/derecho-a-tener-derechos-2/"
URL_APP = ""  # Pega aquí el enlace de tu app cuando ya lo tengas
CARPETA_IMG = "imagenes"
TOTAL = 7
MODO_CALIBRACION = True  # Cambia a False cuando termines de ubicar los objetos

# --------------------------------------------------
# 2. Contenido (separado del diseño)
# Cada derecho tiene: escena, 3 pistas, decisión y "conoce el derecho"
# Imágenes esperadas en la carpeta imagenes/:
#   exterior_shop.png, escena_1.png ... escena_7.png, logo_1.png ... logo_7.png
# --------------------------------------------------
DERECHOS = [
    {
        "nombre": "Derecho a tener derechos",
        "icono": "⚖️",
        "acento": "#7A1F2B",
        "fondo": "#FBECEE",
        "escena": (
            "Un hombre sin hogar entra al estudio a preguntar por un tatuaje "
            "conmemorativo. El encargado le dice que «gente como él no tiene "
            "derecho a nada» y le pide que salga."
        ),
        "alt": (
            "Ilustración de la recepción de un tattoo shop: un hombre con "
            "mochila está frente al mostrador mientras el encargado señala la puerta."
        ),
        "pistas": [
            ("🔍", "¿Qué está pasando?",
             "Al cliente se le niega un trato digno por su situación social, "
             "sin siquiera escuchar lo que necesita."),
            ("👥", "¿Quién se afecta?",
             "El cliente, de forma directa. También quienes presencian la escena "
             "y aprenden que algunas personas valen menos."),
            ("⚖️", "¿Qué derecho está en juego?",
             "El derecho a tener derechos: nadie deja de ser sujeto de derechos "
             "por su condición social, política o ideológica."),
        ],
        "pregunta": "Estás en la sala de espera y ves lo que ocurre. ¿Qué haces?",
        "opciones": [
            ("Me quedo en silencio para no meterme en problemas.", False,
             "Se entiende el temor, pero el silencio deja al cliente solo. "
             "Hay formas seguras de apoyar sin confrontar."),
            ("Le hablo al cliente con respeto y le digo al encargado que toda "
             "persona merece ser escuchada.", True,
             "Reconoces a la persona como alguien con derechos y cuestionas el "
             "trato sin agredir."),
            ("Me río con el encargado para evitar tensión.", False,
             "La burla refuerza la idea de que unas personas valen menos que otras."),
        ],
        "explicacion": (
            "El derecho a tener derechos es el primero porque permite reclamar "
            "todos los demás. Nadie lo pierde por su condición social, política "
            "o ideológica."
        ),
        "resumen": (
            "Todas las personas tienen derecho a tener derechos. Esta idea, que se "
            "atribuye a Hannah Arendt, sostiene que nadie debe quedar fuera de la "
            "protección de la ley, y es la base para reclamar todos los demás derechos."
        ),
        "video": "rMizWVmnEZA",
        "pdf": "https://espaciosabiertos.org/wp-content/uploads/Derecho-FINAL.pdf",
        "pdf_bn": "https://espaciosabiertos.org/wp-content/uploads/EA-DERECHOS-01-Derechos-BW.pdf",
    },
    {
        "nombre": "Derecho a la educación",
        "icono": "📚",
        "acento": "#1F4E79",
        "fondo": "#E8F1FB",
        "escena": (
            "Una tatuadora sorda quiere tomar el curso obligatorio de "
            "bioseguridad, pero quien lo ofrece no tiene intérprete ni "
            "materiales accesibles."
        ),
        "alt": (
            "Ilustración en el tattoo shop: una tatuadora muestra el folleto de "
            "un curso a sus compañeros; una nota en la pared dice que no hay "
            "intérprete disponible."
        ),
        "pistas": [
            ("🔍", "¿Qué está pasando?",
             "Una barrera de acceso: el curso existe, pero no está pensado para "
             "todas las personas. Sin él, ella no puede ejercer su oficio."),
            ("👥", "¿Quién se afecta?",
             "La tatuadora y cualquier estudiante con necesidades especiales "
             "que quede fuera de la oferta educativa."),
            ("⚖️", "¿Qué derecho está en juego?",
             "El derecho a la educación, que debe reconocer la diversidad y las "
             "necesidades especiales de cada estudiante."),
        ],
        "pregunta": "Eres compañera o compañero de trabajo. ¿Qué haces?",
        "opciones": [
            ("Le sugiero que busque un oficio más fácil.", False,
             "Eso traslada la responsabilidad a ella en vez de corregir la barrera."),
            ("La ayudo a pedir por escrito un intérprete y materiales accesibles, "
             "y apoyo su reclamo.", True,
             "Exiges que la educación se adapte a las personas, no al revés."),
            ("Le digo que espere a que algún día lo arreglen.", False,
             "Esperar sin actuar deja la barrera intacta y la deja sin oportunidades."),
        ],
        "explicacion": (
            "La educación debe atender las necesidades de cada estudiante y "
            "ofrecerse sin discriminación. La barrera la pone el sistema, no la persona."
        ),
        "resumen": (
            "La Constitución de Puerto Rico reconoce una educación pública, gratuita "
            "y sin sectarismo, que busque el desarrollo pleno de la persona, que "
            "respete la diversidad y las necesidades especiales y que se ofrezca "
            "sin discriminación."
        ),
        "video": "fMN7G4piQV0",
        "pdf": "https://espaciosabiertos.org/wp-content/uploads/Educacion-FINAL.pdf",
        "pdf_bn": "https://espaciosabiertos.org/wp-content/uploads/EA-DERECHOS-02-Educacion-BW.pdf",
    },
    {
        "nombre": "Derecho al acceso a la información",
        "icono": "📰",
        "acento": "#5B3F8C",
        "fondo": "#F1ECFA",
        "escena": (
            "Un grupo de tatuadores pide por escrito a una agencia pública los "
            "requisitos y costos de las nuevas licencias para estudios. Pasan "
            "semanas y nadie les responde."
        ),
        "alt": (
            "Ilustración: en la pared del shop hay un tablón con cartas sin "
            "respuesta y varios tatuadores revisan sus correos con gesto de preocupación."
        ),
        "pistas": [
            ("🔍", "¿Qué está pasando?",
             "Se solicita información pública y la agencia no responde. Sin datos, "
             "el gremio no sabe qué debe cumplir."),
            ("👥", "¿Quién se afecta?",
             "Todos los estudios, en especial los pequeños, que no pueden "
             "planificar ni cumplir con lo que no conocen."),
            ("⚖️", "¿Qué derecho está en juego?",
             "El acceso a la información: el Gobierno debe actuar con transparencia."),
        ],
        "pregunta": "Tu estudio necesita esa información para abrir. ¿Qué haces?",
        "opciones": [
            ("Adivino los requisitos y abro de todas formas.", False,
             "Te expones a multas y problemas por falta de datos claros."),
            ("Repito la solicitud por escrito, guardo copia y me uno a otros "
             "tatuadores para exigir respuesta.", True,
             "Documentar y organizarse fortalece el reclamo."),
            ("Dejo de insistir; seguro no me van a contestar.", False,
             "Rendirse deja el silencio como respuesta y a ti sin información."),
        ],
        "explicacion": (
            "Tienes derecho a conocer la información pública que afecta tu vida "
            "y tu trabajo. Documentar y organizarse fortalece el reclamo."
        ),
        "resumen": (
            "El Gobierno debe actuar con transparencia. Tener acceso a la "
            "información pública permite conocer cómo se usan los fondos, evaluar "
            "a quienes gobiernan y participar con criterio en las decisiones."
        ),
        "video": "1ZD-S44Y36E",
        "pdf": "https://espaciosabiertos.org/wp-content/uploads/Informacion-FINAL.pdf",
        "pdf_bn": "https://espaciosabiertos.org/wp-content/uploads/EA-DERECHOS-03-Informacion-BW.pdf",
    },
    {
        "nombre": "Derecho a la participación política",
        "icono": "🗣️",
        "acento": "#8A4B00",
        "fondo": "#FFF1E0",
        "escena": (
            "El Gobierno prepara nuevas reglas para los estudios de tatuajes, "
            "pero no ha invitado a los tatuadores a opinar."
        ),
        "alt": (
            "Ilustración: un afiche en la vitrina del shop anuncia una vista "
            "pública mientras dos tatuadores discuten si vale la pena ir."
        ),
        "pistas": [
            ("🔍", "¿Qué está pasando?",
             "Se toman decisiones sobre un gremio sin escuchar su experiencia."),
            ("👥", "¿Quién se afecta?",
             "Tatuadores y clientes, que viven las reglas aunque no participaron "
             "en crearlas."),
            ("⚖️", "¿Qué derecho está en juego?",
             "La participación política: no es solo votar, es que las voces de los "
             "grupos afectados se consideren con seriedad."),
        ],
        "pregunta": "Hay una vista pública la próxima semana. ¿Qué haces?",
        "opciones": [
            ("Me quejo en redes sociales y nada más.", False,
             "Expresarte es válido, pero hay espacios formales donde tu voz pesa más."),
            ("Preparo un comentario, convoco a colegas y participo en la vista pública.",
             True,
             "Participas de forma organizada en la decisión que te afecta."),
            ("Espero a que otro gremio lo haga por mí.", False,
             "Si no participas, tu experiencia no se toma en cuenta."),
        ],
        "explicacion": (
            "Participar es proponer, opinar y ser escuchado en las decisiones que "
            "te afectan, de forma individual o en conjunto."
        ),
        "resumen": (
            "Participar políticamente es más que votar o pertenecer a un partido. "
            "Es lograr que las voces y propuestas de distintos grupos se tomen en "
            "serio en las decisiones que los afectan."
        ),
        "video": "KL3BpPgW2FY",
        "pdf": "https://espaciosabiertos.org/wp-content/uploads/Opinion-Politica-FINAL.pdf",
        "pdf_bn": "https://espaciosabiertos.org/wp-content/uploads/EA-DERECHOS-04-PartPolitica-BW.pdf",
    },
    {
        "nombre": "Derecho al acceso a la justicia",
        "icono": "🏛️",
        "acento": "#1F6B4F",
        "fondo": "#E6F5EE",
        "escena": (
            "Una tatuadora independiente trabajó meses en un shop y no le pagaron "
            "lo acordado. Cree que reclamar no vale la pena porque no puede "
            "pagar un abogado."
        ),
        "alt": (
            "Ilustración: una tatuadora sentada en el mostrador del shop con "
            "papeles y mensajes sin responder en su teléfono."
        ),
        "pistas": [
            ("🔍", "¿Qué está pasando?",
             "Hay un incumplimiento, pero ella siente que reclamar es imposible "
             "por su situación económica."),
            ("👥", "¿Quién se afecta?",
             "Ella y cualquier persona que renuncie a un reclamo justo por falta "
             "de recursos."),
            ("⚖️", "¿Qué derecho está en juego?",
             "El acceso a la justicia: las herramientas legales deben estar "
             "disponibles en igualdad de condiciones."),
        ],
        "pregunta": "Ella te cuenta lo que pasó. ¿Qué le recomiendas?",
        "opciones": [
            ("Que lo deje pasar; los reclamos son complicados.", False,
             "Renunciar al reclamo deja el incumplimiento sin consecuencias."),
            ("Que reúna evidencia (mensajes, acuerdos, fotos) y busque orientación "
             "legal gratuita o de organizaciones.", True,
             "Ordenas la evidencia y buscas apoyo para usar las vías legales."),
            ("Que se presente al shop a amenazar al dueño.", False,
             "La confrontación puede empeorar la situación y debilitar su reclamo."),
        ],
        "explicacion": (
            "No poder pagar un abogado no debe cerrar la puerta a la justicia. "
            "Reunir evidencia y buscar apoyo ayuda a reclamar por vías legales."
        ),
        "resumen": (
            "Acceder a la justicia es poder usar tribunales y otros mecanismos "
            "legales en igualdad de condiciones. Sin este derecho, otros derechos "
            "no se pueden exigir."
        ),
        "video": "YurWptHGE5M",
        "pdf": "https://espaciosabiertos.org/wp-content/uploads/Acceso-Justicia-FINAL.pdf",
        "pdf_bn": "https://espaciosabiertos.org/wp-content/uploads/EA-DERECHOS-05-Justicia-BW.pdf",
    },
    {
        "nombre": "Derecho al trabajo",
        "icono": "🛠️",
        "acento": "#8A2D12",
        "fondo": "#FDEBE4",
        "escena": (
            "En un shop se exige trabajar horas extra todas las semanas sin paga, "
            "y el área de esterilización casi no tiene ventilación ni equipo "
            "de protección."
        ),
        "alt": (
            "Ilustración: un reloj marca la medianoche en el shop mientras un "
            "tatuador agotado limpia equipo en un cuarto pequeño y sin ventilación."
        ),
        "pistas": [
            ("🔍", "¿Qué está pasando?",
             "Condiciones injustas: trabajo sin compensación y riesgos de seguridad."),
            ("👥", "¿Quién se afecta?",
             "Los tatuadores del shop y también los clientes, si el equipo no "
             "se maneja bien."),
            ("⚖️", "¿Qué derecho está en juego?",
             "El derecho al trabajo: paga digna, ambiente seguro y libre de "
             "discriminación, y derecho a organizarse."),
        ],
        "pregunta": "Eres parte del equipo. ¿Qué haces?",
        "opciones": [
            ("Acepto todo para no perder el empleo.", False,
             "Aceptar sin más mantiene las condiciones injustas."),
            ("Documento las horas y condiciones, converso con mis compañeros y "
             "buscamos orientación para reclamar juntos.", True,
             "Reclamar en grupo y con evidencia da más fuerza al reclamo."),
            ("Renuncio sin decir nada a nadie.", False,
             "Es una decisión personal posible, pero el problema queda igual "
             "para quienes se quedan."),
        ],
        "explicacion": (
            "El derecho al trabajo incluye paga justa, condiciones seguras y "
            "organizarse para defender intereses. Muchas protecciones actuales "
            "nacieron de luchas colectivas."
        ),
        "resumen": (
            "Incluye elegir libremente un trabajo, recibir paga digna, trabajar en "
            "un ambiente seguro y sin discriminación, y organizarse para defender "
            "los intereses de quienes trabajan."
        ),
        "video": "p4gJn6G36VM",
        "pdf": "https://espaciosabiertos.org/wp-content/uploads/Trabajo-FINAL.pdf",
        "pdf_bn": "https://espaciosabiertos.org/wp-content/uploads/EA-DERECHOS-06-Trabajo-BW.pdf",
    },
    {
        "nombre": "Derecho a la dignidad",
        "icono": "🤝",
        "acento": "#8A1C5C",
        "fondo": "#FBE9F3",
        "escena": (
            "Un cliente se burla del acento y de la apariencia de una tatuadora "
            "mientras ella trabaja. El dueño dice: «el cliente siempre tiene "
            "la razón»."
        ),
        "alt": (
            "Ilustración: una tatuadora trabaja mientras un cliente sonríe con "
            "burla; al fondo, el dueño encoge los hombros."
        ),
        "pistas": [
            ("🔍", "¿Qué está pasando?",
             "Se normaliza un trato humillante hacia una persona por su forma de ser."),
            ("👥", "¿Quién se afecta?",
             "La tatuadora y el ambiente de todo el shop."),
            ("⚖️", "¿Qué derecho está en juego?",
             "La dignidad: el valor de toda persona por ser persona, sin "
             "discriminación por apariencia, origen u otras condiciones."),
        ],
        "pregunta": "Estás en el shop y ves la escena. ¿Qué haces?",
        "opciones": [
            ("Me río para que el cliente no se incomode.", False,
             "La risa legitima la burla y deja sola a tu compañera."),
            ("Pongo un límite al cliente, apoyo a mi compañera y propongo una "
             "política de trato respetuoso en el shop.", True,
             "Defiendes la dignidad de tu compañera y cambias la regla del lugar."),
            ("No digo nada; no es mi problema.", False,
             "La indiferencia también sostiene el maltrato."),
        ],
        "explicacion": (
            "La dignidad se respeta cuando se valora por igual a las personas. "
            "Un trato respetuoso es parte del servicio, no un favor."
        ),
        "resumen": (
            "La dignidad es el valor que tiene toda persona por ser persona. Exige "
            "trato igual y respetuoso, celebra la diversidad y abre la puerta a otros "
            "derechos como la salud, la educación y la vivienda."
        ),
        "video": "yTGCsf9OpmA",
        "pdf": "https://espaciosabiertos.org/wp-content/uploads/Dignidad-FINAL.pdf",
        "pdf_bn": "https://espaciosabiertos.org/wp-content/uploads/EA-DERECHOS-07-Dignidad-BW.pdf",
    },
]

# --------------------------------------------------
# 2b. Objetos interactivos (hotspots) de cada escena
# Formato: (nombre del objeto, x %, y %, radio %)
#   x, y  = centro del objeto, en porcentaje del ancho y alto de la imagen
#   radio = tamaño de la zona, en porcentaje del ancho de la imagen
# El orden coincide con las 3 pistas: 1) qué pasa, 2) quién se afecta, 3) qué derecho.
# Los números de abajo son provisionales: ajústalos con el modo calibración.
# --------------------------------------------------
HOTSPOTS = {
    0: [("La puerta", 82, 55, 9), ("La mochila del cliente", 28, 72, 8), ("El cartel de la pared", 52, 22, 8)],
    1: [("El folleto del curso", 25, 60, 8), ("La tatuadora", 50, 50, 9), ("La nota sin intérprete", 78, 30, 8)],
    2: [("El tablón de cartas", 22, 35, 9), ("Los tatuadores frente a la laptop", 52, 60, 9), ("El sello de la agencia", 80, 30, 8)],
    3: [("El afiche de la vista pública", 22, 35, 9), ("Los dos tatuadores", 55, 62, 9), ("El micrófono vacío", 82, 55, 8)],
    4: [("Los mensajes sin responder", 25, 58, 8), ("La tatuadora", 52, 50, 9), ("La puerta de la oficina", 82, 40, 9)],
    5: [("El reloj", 22, 25, 8), ("El cuarto sin ventilación", 78, 50, 10), ("El tatuador agotado", 48, 62, 9)],
    6: [("El cliente que se burla", 25, 55, 9), ("La tatuadora", 52, 55, 9), ("El dueño", 80, 50, 9)],
}

# --------------------------------------------------
# 3. Estado de la aplicación
# --------------------------------------------------
ESTADO_INICIAL = {
    "pantalla": "home",   # home, selector, escena, conoce, final
    "actual": 0,          # índice del derecho que se está jugando
    "completados": [],    # índices de derechos terminados
    "pistas": {},         # {indice: [pistas reveladas]}
    "decisiones": {},     # {indice: opción escogida}
}
for clave, valor in ESTADO_INICIAL.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor


def ir_a(pantalla):
    st.session_state.pantalla = pantalla
    st.rerun()


# --------------------------------------------------
# 4. Estilos visuales
# --------------------------------------------------
st.markdown(
    """
<style>
.block-container { max-width: 1100px; padding-top: 1.5rem; padding-bottom: 4rem; }
.hero {
  padding: 2rem; border-radius: 22px; margin-bottom: 1.2rem;
  background: linear-gradient(135deg, #14110F 0%, #3A2A24 100%); color: #FFFFFF;
}
.hero h1 { color: #FFFFFF; margin: 0; font-size: 3rem; line-height: 1.05; }
.hero p { font-size: 1.15rem; line-height: 1.55; margin: 0.8rem 0 0 0; max-width: 760px; }
.hero .sello { font-size: 0.95rem; font-weight: 700; letter-spacing: .08em; opacity: .85; }
.placeholder {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  background: #F2EDE6; border: 2px dashed #8C7B6B; border-radius: 18px;
  padding: 1.5rem; text-align: center; color: #2B2320; margin-bottom: 0.6rem;
}
.ph-emoji { font-size: 3.5rem; }
.ph-text { font-size: 1.05rem; line-height: 1.5; max-width: 640px; }
.card-derecho {
  border-radius: 18px; padding: 1.2rem; margin-bottom: 0.4rem;
  border: 1px solid rgba(30, 40, 50, 0.12); min-height: 150px;
}
.card-icono { font-size: 2.2rem; }
.card-titulo { font-size: 1.2rem; font-weight: 750; margin: 0.3rem 0; }
.card-estado { font-size: 1rem; font-weight: 650; color: #2B2320; }
.situacion {
  background: #F7F8FA; border-left: 6px solid #304D6D; border-radius: 10px;
  padding: 1.1rem 1.3rem; font-size: 1.1rem; line-height: 1.55; margin: 0.8rem 0 1rem 0;
  color: #1B1B1B;
}
.explicacion {
  background: #EDF8F0; border-left: 6px solid #27653A; border-radius: 10px;
  padding: 1.1rem 1.3rem; font-size: 1.1rem; line-height: 1.55; margin: 1rem 0; color: #1B1B1B;
}
.pie { text-align: center; color: #4A525A; font-size: 0.9rem; margin-top: 3rem; }
div[data-testid="stButton"] button { width: 100%; border-radius: 999px; min-height: 3rem; font-weight: 650; }
@media (max-width: 700px) {
  .hero h1 { font-size: 2.1rem; }
  .hero { padding: 1.3rem; }
}
</style>
""",
    unsafe_allow_html=True,
)


# --------------------------------------------------
# 5. Funciones de ayuda
# --------------------------------------------------
def bloque(html):
    """Muestra HTML sin sangrías ni líneas vacías (evita que Markdown lo rompa)."""
    limpio = "\n".join(l.strip() for l in html.splitlines() if l.strip())
    st.markdown(limpio, unsafe_allow_html=True)


def mostrar_imagen(archivo, alt, emoji, altura=300):
    """Muestra la imagen si existe en imagenes/; si no, un marcador con su descripción."""
    ruta = os.path.join(CARPETA_IMG, archivo)
    if os.path.exists(ruta):
        st.image(ruta, caption=alt)
    else:
        bloque(
            f"""
            <div class="placeholder" role="img" aria-label="{alt}" style="min-height:{altura}px;">
            <div class="ph-emoji">{emoji}</div>
            <div class="ph-text">{alt}</div>
            </div>
            """
        )


def barra_superior():
    """Botón de inicio y barra de progreso, presentes en todas las pantallas internas."""
    col_inicio, col_progreso = st.columns([1, 3])
    with col_inicio:
        if st.button("🏠 Inicio", key="btn_inicio"):
            ir_a("home")
    with col_progreso:
        hechos = len(st.session_state.completados)
        st.progress(hechos / TOTAL, text=f"Progreso: {hechos} de {TOTAL} derechos")


def pie_de_pagina():
    bloque(
        """
        <div class="pie">
        Contenido basado en la serie «Derechos. Son tuyos. Defiéndelos.» de Espacios Abiertos
        y el Centro de Periodismo Investigativo. Logos y materiales pertenecen a sus autores.
        Esta aplicación no recopila ni guarda datos personales.
        </div>
        """
    )


# --------------------------------------------------
# 6. Pantallas
# --------------------------------------------------
def pantalla_home():
    mostrar_imagen(
        "exterior_shop.png",
        "Ilustración de la fachada de un tattoo shop con un letrero luminoso y la puerta abierta.",
        "🏚️",
        altura=360,
    )
    bloque(
        """
        <div class="hero">
        <div class="sello">JUEGO EDUCATIVO</div>
        <h1>Bajo la piel</h1>
        <p>Entra al estudio, mira lo que pasa y descubre qué derechos están en juego
        en el día a día de quienes tatúan.</p>
        </div>
        """
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🖋️ Empezar", type="primary", key="btn_empezar"):
            ir_a("selector")
    with col2:
        st.link_button("📖 Sobre el proyecto", URL_PROYECTO)
    if URL_APP:
        st.caption("Comparte el juego copiando este enlace:")
        st.code(URL_APP, language=None)
    pie_de_pagina()


def pantalla_selector():
    barra_superior()
    st.markdown("## ¿Cuánto conoces tus derechos?")
    st.write("Escoge un derecho para entrar a la escena. Completa los 7 para terminar el juego.")
    columnas = st.columns(3, gap="medium")
    for i, d in enumerate(DERECHOS):
        with columnas[i % 3]:
            hecho = i in st.session_state.completados
            estado = "✓ Completado" if hecho else "Pendiente"
            bloque(
                f"""
                <div class="card-derecho" style="background:{d['fondo']}; border-top:6px solid {d['acento']};">
                <div class="card-icono">{d['icono']}</div>
                <div class="card-titulo" style="color:{d['acento']};">{i + 1}. {d['nombre']}</div>
                <div class="card-estado">{estado}</div>
                </div>
                """
            )
            etiqueta = "Repasar" if hecho else "Jugar"
            if st.button(etiqueta, key=f"sel_{i}"):
                st.session_state.actual = i
                ir_a("escena")
    pie_de_pagina()


@st.dialog("¿Qué harías tú?")
def dialogo_decision(i):
    d = DERECHOS[i]
    st.write(d["pregunta"])
    textos = [op[0] for op in d["opciones"]]
    seleccion = st.radio("Escoge una opción:", textos, index=None, key=f"radio_{i}")
    if st.button("Confirmar", type="primary", key=f"confirmar_{i}"):
        if seleccion is None:
            st.warning("Escoge una opción antes de confirmar.")
        else:
            st.session_state.decisiones[i] = textos.index(seleccion)
            st.rerun()  # cierra la ventana


def sin_tildes(texto):
    """La fuente por defecto de Pillow no dibuja tildes; solo se usa en el lienzo provisional."""
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


def fuente(tamano):
    try:
        return ImageFont.load_default(size=tamano)
    except TypeError:
        return ImageFont.load_default()


def cargar_escena(i):
    """Abre imagenes/escena_N.png; si no existe, crea un lienzo provisional."""
    ruta = os.path.join(CARPETA_IMG, f"escena_{i + 1}.png")
    real = os.path.exists(ruta)
    if real:
        img = Image.open(ruta).convert("RGB")
    else:
        img = Image.new("RGB", (1200, 675), "#F2EDE6")
        d = ImageDraw.Draw(img)
        d.rectangle([6, 6, 1193, 668], outline="#8C7B6B", width=4)
        d.text((40, 30), f"Escena {i + 1}: aqui ira tu ilustracion (imagenes/escena_{i + 1}.png)",
               fill="#2B2320", font=fuente(26))
    if img.width > 1200:
        img = img.resize((1200, int(img.height * 1200 / img.width)))
    return img, real


def dibujar_marcas(img, i, reveladas, ayuda, real):
    """Dibuja ✓ en los objetos encontrados y, si hay ayuda, marcas en los pendientes."""
    d = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    for k, (nombre, x, y, r) in enumerate(HOTSPOTS[i]):
        cx, cy, rad = x / 100 * w, y / 100 * h, r / 100 * w
        caja = [cx - rad, cy - rad, cx + rad, cy + rad]
        if k in reveladas:
            d.ellipse(caja, outline=(39, 101, 58, 255), width=6, fill=(39, 101, 58, 90))
            d.line([(cx - rad * 0.4, cy), (cx - rad * 0.1, cy + rad * 0.4), (cx + rad * 0.45, cy - rad * 0.4)],
                   fill=(255, 255, 255, 255), width=8)
        elif ayuda or not real:
            d.ellipse(caja, outline=(255, 200, 0, 255), width=5, fill=(255, 200, 0, 60))
            d.text((cx, cy), "?", fill=(40, 30, 0, 255), font=fuente(int(rad * 1.2)), anchor="mm")
            if not real:
                d.text((cx, cy + rad + 14), sin_tildes(nombre), fill=(43, 35, 32, 255), font=fuente(20), anchor="mm")
    return img


def pantalla_escena():
    i = st.session_state.actual
    d = DERECHOS[i]
    barra_superior()
    st.markdown(f"## {d['icono']} {d['nombre']}")
    bloque(f'<div class="situacion">{d["escena"]}</div>')

    reveladas = st.session_state.pistas.setdefault(i, [])
    st.markdown("### Toca los objetos de la escena para descubrir las pistas")
    ayuda = st.checkbox("💡 Mostrar ayuda (marca los objetos pendientes)", key=f"ayuda_{i}")

    img, real = cargar_escena(i)
    img = dibujar_marcas(img, i, reveladas, ayuda, real)
    click = None
    if HAY_CLICK:
        try:
            click = streamlit_image_coordinates(img, key=f"img_{i}", use_column_width=True)
        except TypeError:
            click = streamlit_image_coordinates(img, key=f"img_{i}")
    else:
        st.image(img)
        st.warning(
            "No se cargó la librería de clic sobre la imagen (revisa requirements.txt). "
            "Mientras tanto, usa estos botones."
        )
        for k, (nombre, _x, _y, _r) in enumerate(HOTSPOTS[i]):
            if st.button(f"🔎 {nombre}", key=f"obj_{i}_{k}"):
                if k not in reveladas:
                    reveladas.append(k)
    st.caption(d["alt"])

    px = py = None
    if click:
        px = click["x"] / click["width"] * 100
        py = click["y"] / click["height"] * 100
        if st.session_state.get(f"ultimo_click_{i}") != click["unix_time"]:
            st.session_state[f"ultimo_click_{i}"] = click["unix_time"]
            w, h = img.size
            for k, (nombre, x, y, r) in enumerate(HOTSPOTS[i]):
                dx = (px - x) / 100 * w
                dy = (py - y) / 100 * h
                if dx * dx + dy * dy <= (r / 100 * w) ** 2:
                    if k not in reveladas:
                        reveladas.append(k)
                    st.rerun()  # redibuja la imagen con la marca ✓
            else:
                st.caption("🔎 Ahí no hay nada. Sigue buscando.")

    st.markdown(f"**Pistas encontradas: {len(reveladas)} de 3**")
    for k in sorted(reveladas):
        icono, titulo, texto = d["pistas"][k]
        nombre = HOTSPOTS[i][k][0]
        st.info(f"{icono} **{titulo}** · _{nombre}_\n\n{texto}")

    if MODO_CALIBRACION:
        with st.expander("🛠️ Modo calibración (solo para quien diseña)"):
            st.write("Toca el centro de cada objeto en la imagen y copia estos valores en HOTSPOTS.")
            if px is not None:
                st.code(f"x = {px:.0f}, y = {py:.0f}", language=None)
            else:
                st.caption("Aún no has tocado la imagen.")

    decision = st.session_state.decisiones.get(i)
    if decision is None:
        todas = len(reveladas) == 3
        if not todas:
            st.caption("Encuentra las 3 pistas para poder continuar.")
        if st.button("Continuar →", type="primary", disabled=not todas, key=f"cont_{i}"):
            dialogo_decision(i)
    else:
        texto_op, _, retro = d["opciones"][decision]
        st.markdown("### Tu decisión")
        st.write(f"**{texto_op}**")
        st.write(retro)
        bloque(f'<div class="explicacion">{d["explicacion"]}</div>')
        if st.button("Conoce el derecho →", type="primary", key=f"conoce_{i}"):
            ir_a("conoce")
    pie_de_pagina()


def pantalla_conoce():
    i = st.session_state.actual
    d = DERECHOS[i]
    barra_superior()
    st.markdown("## Conoce el derecho")
    mostrar_imagen(
        f"logo_{i + 1}.png",
        f"Logo del derecho: {d['nombre']}, de la serie Derechos. Son tuyos. Defiéndelos.",
        d["icono"],
        altura=160,
    )
    bloque(
        f"""
        <div class="card-derecho" style="background:{d['fondo']}; border-top:6px solid {d['acento']};">
        <div class="card-titulo" style="color:{d['acento']};">{d['nombre']}</div>
        <div style="font-size:1.1rem; line-height:1.6; color:#1B1B1B;">{d['resumen']}</div>
        </div>
        """
    )
    st.markdown("### Video")
    st.video(f"https://www.youtube.com/watch?v={d['video']}")
    st.markdown("### Material para profundizar")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("📄 Material educativo (PDF)", d["pdf"])
    with col2:
        st.link_button("🖨️ Formato libro B/N (PDF)", d["pdf_bn"])

    st.write("")
    if st.button("Continuar →", type="primary", key=f"seguir_{i}"):
        if i not in st.session_state.completados:
            st.session_state.completados.append(i)
        if len(st.session_state.completados) == TOTAL:
            ir_a("final")
        else:
            ir_a("selector")
    pie_de_pagina()


def pantalla_final():
    barra_superior()
    st.balloons()
    bloque(
        """
        <div class="hero">
        <div class="sello">¡MISIÓN CUMPLIDA!</div>
        <h1>Felicitaciones</h1>
        <p>Ahora eres un tatuador o tatuadora que comprende sus derechos. Ya sabes
        reconocerlos en el estudio, hablar de ellos y defenderlos junto a tu comunidad.</p>
        </div>
        """
    )
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("📖 Conoce más sobre la serie", URL_PROYECTO)
    with col2:
        if st.button("🔄 Jugar de nuevo", key="btn_reiniciar"):
            for clave, valor in ESTADO_INICIAL.items():
                st.session_state[clave] = type(valor)() if isinstance(valor, (list, dict)) else valor
            st.session_state.pantalla = "selector"
            st.rerun()
    if URL_APP:
        st.caption("Comparte el juego copiando este enlace:")
        st.code(URL_APP, language=None)
    pie_de_pagina()


# --------------------------------------------------
# 7. Navegación principal
# --------------------------------------------------
PANTALLAS = {
    "home": pantalla_home,
    "selector": pantalla_selector,
    "escena": pantalla_escena,
    "conoce": pantalla_conoce,
    "final": pantalla_final,
}
PANTALLAS[st.session_state.pantalla]()
