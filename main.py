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

class RedditAnalyzer:
    def __init__(self, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        self.translator = Translator()
        self.analyzer = SentimentIntensityAnalyzer()

    def recolectar_publicaciones(self, subreddit_name, limite=100):
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            publicaciones = [
                {
                    'titulo': post.title,
                    'contenido': post.selftext or "No hay contenido."
                } for post in subreddit.new(limit=limite)
            ]
            if not publicaciones:
                raise ValueError("No se encontraron publicaciones.")
            return publicaciones
        except praw.exceptions.PRAWException as e:
            print(f"Error al conectarse a Reddit: {e}")
        except Exception as e:
            print(f"Ocurrió un error: {e}")

    def analizar_sentimiento(self, texto):
        try:
            # Traducir el texto al inglés
            texto_traducido = self.translator.translate(texto, dest='en').text
            print(textwrap.fill("Traductor: " + texto_traducido, width=70))
            puntajes = self.analyzer.polarity_scores(texto_traducido)
            if puntajes['compound'] > 0.05:
                return 'Positivo'
            elif puntajes['compound'] < -0.05:
                return 'Negativo'
            else:
                return 'Neutral'
        except Exception as e:
            print(f"Error al analizar el sentimiento: {e}")

    def analizar_publicaciones(self, subreddit_name, limite=10):
        publicaciones = self.recolectar_publicaciones(subreddit_name, limite)
        resultados_sentimiento = {'Positivo': 0, 'Negativo': 0, 'Neutral': 0}

        if publicaciones:
            for post in publicaciones:
                self.mostrar_publicacion(post)
                sentimiento = self.analizar_sentimiento(post['contenido'])
                if sentimiento:
                    color = COLORS[sentimiento]
                    print(f"\n{color}Sentimiento: {sentimiento}{RESET}")
                    print("-----------------------------------------------------\n\n")
                    resultados_sentimiento[sentimiento] += 1

        self.visualizar_resultados(resultados_sentimiento)

    def mostrar_publicacion(self, post):
        print(f"Título: {post['titulo']}\n")
        print(textwrap.fill(f"Contenido: {post['contenido']}", width=70))
        print("\n")

    def visualizar_resultados(self, resultados_sentimiento):
        labels = resultados_sentimiento.keys()
        sizes = resultados_sentimiento.values()

        plt.bar(labels, sizes, color=['green', 'red', 'gray'])
        plt.title('Distribución de Sentimientos')
        plt.xlabel('Sentimiento')
        plt.ylabel('Cantidad')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--')

        # Mostrar el gráfico
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Autenticación en Reddit
    CLIENT_ID = '7-J0stycVBf6p3muSuUBBw'
    CLIENT_SECRET = 'eit27nQjpWe2oHxvw7QnuwsycFkj2Q'
    USER_AGENT = 'Agent'

    analizador = RedditAnalyzer(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
    analizador.analizar_publicaciones('Ticos', 10)





