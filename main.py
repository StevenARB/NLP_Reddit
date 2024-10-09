import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
import matplotlib.pyplot as plt
import textwrap

# Colores para los sentimientos
COLORS = {
    'Positivo': '\033[92m',  # Verde
    'Negativo': '\033[91m',  # Rojo
    'Neutral': '\033[90m'     # Gris
}
RESET = '\033[0m'  # Reiniciar color

# Autenticación en Reddit
reddit = praw.Reddit(
    client_id='7-J0stycVBf6p3muSuUBBw',
    client_secret='eit27nQjpWe2oHxvw7QnuwsycFkj2Q',
    user_agent='Agent'
)

# Inicializar el traductor
translator = Translator()

# Función para recolectar publicaciones
def recolectar_publicaciones(subreddit_name, limite=100):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        publicaciones = []
        for post in subreddit.new(limit=limite):
            publicaciones.append({
                'titulo': post.title,
                'contenido': post.selftext if post.selftext else "No hay contenido."
            })
        if not publicaciones:
            raise ValueError("No se encontraron publicaciones.")
        return publicaciones
    except praw.exceptions.PRAWException as e:
        print(f"Error al conectarse a Reddit: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Función para analizar sentimiento usando VADER
def analizar_sentimiento(texto):
    try:
        # Traducir el texto al inglés
        texto_traducido = translator.translate(texto, dest='en').text
        print(textwrap.fill("Traductor: " + texto_traducido, width=70))
        analyzer = SentimentIntensityAnalyzer()
        puntajes = analyzer.polarity_scores(texto_traducido)
        if puntajes['compound'] > 0.05:
            return 'Positivo'
        elif puntajes['compound'] < -0.05:
            return 'Negativo'
        else:
            return 'Neutral'
    except Exception as e:
        print(f"Error al analizar el sentimiento: {e}")

# Recolectar y analizar publicaciones
publicaciones = recolectar_publicaciones('Ticos', 10)

# Resultados del análisis de sentimientos
resultados_sentimiento = {'Positivo': 0, 'Negativo': 0, 'Neutral': 0}

if publicaciones:
    for post in publicaciones:
        print(f"Título: {post['titulo']}")
        print("\n")
        print(textwrap.fill(f"Contenido: {post['contenido']}", width=70))
        print("\n")
        sentimiento = analizar_sentimiento(post['contenido'])
        if sentimiento:
            color = COLORS[sentimiento]
            print(f"\n{color}Sentimiento: {sentimiento}{RESET}")
            print("-----------------------------------------------------\n\n")
            resultados_sentimiento[sentimiento] += 1

# Crear gráfico de barras
labels = resultados_sentimiento.keys()
sizes = resultados_sentimiento.values()

plt.bar(labels, sizes, color=['green', 'red', 'gray'])
plt.title('Distribución de Sentimientos de los Ticos')
plt.xlabel('Sentimiento')
plt.ylabel('Cantidad')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--')

# Mostrar el gráfico
plt.tight_layout()
plt.show()




