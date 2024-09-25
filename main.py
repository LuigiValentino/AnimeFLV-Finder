import animeflv
import webbrowser
from colorama import Fore, Style, init

init(autoreset=True)

def mostrar_bienvenida():
    print(Fore.CYAN + Style.BRIGHT + "="*50)
    print(Fore.YELLOW + Style.BRIGHT + "Bienvenido a AnimeFLV Finder!")
    print(Fore.CYAN + Style.BRIGHT + "="*50)
    print(Fore.WHITE + "Busca y reproduce tus animes favoritos desde la terminal.")
    print(Fore.CYAN + "="*50)

def mostrar_instrucciones():
    print(Fore.GREEN + "\nInstrucciones:")
    print(Fore.WHITE + "1. Ingresa el nombre del anime que deseas buscar.")
    print(Fore.WHITE + "2. Elige el anime de la lista de resultados.")
    print(Fore.WHITE + "3. Selecciona el episodio y la calidad que deseas ver.")
    print(Fore.WHITE + "4. Disfruta el episodio en tu navegador.")
    print(Fore.CYAN + "="*50)

def mostrar_footer():
    print(Fore.CYAN + "="*50)
    print(Fore.YELLOW + Style.BRIGHT + "Gracias por usar AnimeFLV Finder!")
    print(Fore.WHITE + "Programado por Luigi Adducci")
    print(Fore.BLUE + "GitHub: " + Fore.LIGHTBLUE_EX + "https://github.com/LuigiValentino")
    print(Fore.BLUE + "API de AnimeFLV: " + Fore.LIGHTBLUE_EX + "https://pypi.org/project/animeflv/")
    print(Fore.CYAN + "="*50)

def buscar_anime(nombre):
    with animeflv.AnimeFLV() as api:
        resultados = api.search(nombre)
        if resultados:
            print(Fore.CYAN + f"\nSe encontraron {len(resultados)} resultados:")
            for i, resultado in enumerate(resultados):
                print(Fore.YELLOW + f"{i + 1}. {resultado.title}")
            selection = int(input(Fore.GREEN + "\nElige el número del anime que deseas ver: ")) - 1
            info = api.get_anime_info(resultados[selection].id)
            info.episodes.reverse()
            for j, episodio in enumerate(info.episodes):
                print(Fore.YELLOW + f"{j + 1} | Episodio - {episodio.id}")
            return info
        else:
            print(Fore.RED + "\nNo se encontraron resultados.")
            return None

def obtener_enlace_video(info):
    with animeflv.AnimeFLV() as api:
        index_episode = int(input(Fore.GREEN + "\nElige el número del episodio que deseas ver: ")) - 1
        serie = info.id
        capitulo = info.episodes[index_episode].id
        results = api.get_links(serie, capitulo)
        if results:
            print(Fore.CYAN + "\nEnlaces de video disponibles:")
            for i, result in enumerate(results):
                quality = getattr(result, 'quality', 'No disponible')
                print(Fore.YELLOW + f"{i + 1}. {result.server} -- {quality} -- {result.url}")
            selection = int(input(Fore.GREEN + "\nElige el número del servidor/calidad que prefieras: ")) - 1
            return results[selection].url
        else:
            print(Fore.RED + "\nNo se encontraron enlaces de video.")
            return None

def reproducir_anime(enlace):
    webbrowser.open(enlace)
    print(Fore.GREEN + "Reproduciendo en el navegador...")

if __name__ == "__main__":
    mostrar_bienvenida()
    mostrar_instrucciones()
    
    nombre_anime = input(Fore.GREEN + "Ingresa el nombre del anime que deseas ver: ")
    info = buscar_anime(nombre_anime)
    
    if info:
        enlace_video = obtener_enlace_video(info)
        if enlace_video:
            reproducir_anime(enlace_video)
    
    mostrar_footer()
