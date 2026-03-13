
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
def exit_game():
    menu.destroy() # ukryj okno menu
    exit()

def tablica_wynikow():
    menu.withdraw()
    tablica = tkinter.Tk()
    tablica.title("Tablica Wynikow")
    directory = os.getcwd()
    tablica.iconbitmap(os.path.join(directory, 'snake.ico'))
    tablica.resizable(False, False)

    szer_ekranu = tablica.winfo_screenwidth()
    wys_ekranu = tablica.winfo_screenheight()
    tablica.geometry(f"{SZER_OKNA}x{WYS_OKNA}+{int((szer_ekranu - SZER_OKNA) / 2)}+{int((wys_ekranu - WYS_OKNA) / 2)}")

    # Ramka z paskiem przewijania
    ramka = tkinter.Frame(tablica)
    ramka.pack(fill="both", expand=True)

    # Pasek przewijania
    scrollbar = tkinter.Scrollbar(ramka)
    scrollbar.pack(side="right", fill="y")

    rysowanie_tablica = tkinter.Canvas(ramka, bg="black", width=SZER_OKNA, height=WYS_OKNA, borderwidth=0, highlightthickness=0, yscrollcommand=scrollbar.set)
    rysowanie_tablica.pack(side="left", fill="both", expand=True)

    # Konfiguracja paska przewijania
    scrollbar.config(command=rysowanie_tablica.yview)

    def back_to_menu():
        tablica.destroy()
        menu.deiconify()

    back_button = tkinter.Button(tablica, text="Powrot", command=back_to_menu)
    back_button.place(relx=0.5, rely=0.7, anchor="center")

    # Odczytanie wyników z pliku
    wyniki = []
    directory = os.getcwd()
    file_path = os.path.join(directory, "wyniki.txt")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            for line in file:
                data = line.split()
                if len(data) >= 3:
                    name = " ".join(data[:-2])
                    try:
                        points = int(data[-2])
                        moves = int(data[-1])
                        wyniki.append((name, points, moves))
                    except ValueError: