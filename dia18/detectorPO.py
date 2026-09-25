from urllib import request
from urllib.error import URLError

lpo = ["coño", "bobo", "culiao", "pinche", "estupido", "estupida"]


def verificar_web(url):
    try:
        # Agregamos un User-Agent para que Wikcionario no bloquee la petición
        req = request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/115.0.0.0 Safari/537.36"
                )
            },
        )
        with request.urlopen(req) as response:
            # Leemos el contenido HTML y lo pasamos a texto en minúsculas
            html_texto = response.read().decode("utf-8").lower()

    except URLError as e:
        return f"¡Error al acceder a la URL ({url}): {e}!"

    # Buscamos qué palabras de la lista están presentes en el contenido
    palabras_encontradas = [palabra for palabra in lpo if palabra in html_texto]

    return palabras_encontradas


# Prueba del script
url = "https://es.wiktionary.org/wiki/Wikcionario:Insultos_regionales"

print("\n----------------------------------------\n")
print("Informe de sitio:")
print(verificar_web(url))