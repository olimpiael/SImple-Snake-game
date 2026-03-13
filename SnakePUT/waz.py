import tkinter
import random
import os
import tkinter.messagebox
directory = os.path.dirname(os.path.abspath(__file__))

WIERSZE = 25
KOLUMNY = 25
TILE_SIZE = 25

SZER_OKNA = TILE_SIZE * WIERSZE
WYS_OKNA = TILE_SIZE * KOLUMNY

class Tile:
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
    directory = os.path.dirname(os.path.abspath(__file__))
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
    directory = os.path.dirname(os.path.abspath(__file__))
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
                        print(f"Nieprawidłowy format danych w linii: {line}")
        # Sortowanie wyników po liczbie punktów
        wyniki.sort(key=lambda x: x[1], reverse=True)

        # Wyświetlanie wyników
        rysowanie_tablica.create_text(SZER_OKNA // 2, 50, text="Najlepsze wyniki", fill="white", font=("Arial", 20))
        for i, (name, points, moves) in enumerate(wyniki, start=1):
            rysowanie_tablica.create_text(50, 100 + i * 30, anchor="w", text=f"{i}. {name}: {points} punktów, {moves} ruchów", fill="white", font=("Arial", 12))
    else:
        rysowanie_tablica.create_text(SZER_OKNA // 2, WYS_OKNA // 2, text="Brak wyników", fill="white", font=("Arial", 20))

    tablica.mainloop()

def save_score(over, pole, punkty, licznik_ruchow):
    directory = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(directory, "wyniki.txt"), "a") as f:
        f.write(pole.get() + " " + str(punkty) + " " + str(licznik_ruchow) + "\n")

def color_selection():
    menu.withdraw()
    selection_menu = tkinter.Tk()
    selection_menu.title("Wybór koloru")
    directory = os.path.dirname(os.path.abspath(__file__))
    selection_menu.iconbitmap(os.path.join(directory, 'snake.ico'))
    selection_menu.geometry(f"{SZER_OKNA}x{WYS_OKNA}+{int((szer_ekranu - SZER_OKNA) / 2)}+{int((wys_ekranu - WYS_OKNA) / 2)}")
    selection_menu.configure(bg="black")
    
    def start_game_color(color):
        selection_menu.destroy()
        start_game(color)

    napis = tkinter.Label(selection_menu, text="Wybierz kolor węża", bg="black", fg="white", font=("Arial", 16))
    napis.pack(pady=10)

    button_frame = tkinter.Frame(selection_menu, bg="black")
    button_frame.pack(pady=10)

    colors = [("      ", "blue"), ("      ", "green"), ("      ", "pink"), ("      ", "purple"), ("      ", "yellow"), ("      ", "orange")]

    for text, color in colors:
        button = tkinter.Button(button_frame, text=text, command=lambda c=color: start_game_color(c), bg=color, fg="white")
        button.pack(side="left", padx=10,pady=100)

    selection_menu.mainloop()



def start_game(color="lime green"):
    global okienko, game_over
    menu.withdraw() # Zamykanie okna menu
    # okno gry
    okienko = tkinter.Tk()
    okienko.title("snake")
    okienko.resizable(False, False)
    rysowanie = tkinter.Canvas(okienko, bg="black", width=SZER_OKNA, height=WYS_OKNA, borderwidth=0, highlightthickness=0)

    rysowanie.pack()

    szer_ekranu = okienko.winfo_screenwidth()
    wys_ekranu = okienko.winfo_screenheight()
    okienko.geometry(f"{SZER_OKNA}x{WYS_OKNA}+{int((szer_ekranu - SZER_OKNA) / 2)}+{int((wys_ekranu - WYS_OKNA) / 2)}")
    # inicjalizacja gry
    global waz, jedzenie, cialo_weza, velocityX, velocityY, licznik_ruchow, punkty, game_over,paused
    waz = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
    jedzenie = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)
    cialo_weza = []
    velocityX = 0
    velocityY = 0
    licznik_ruchow = 0
    punkty = 0
    game_over = False
    paused = False
    def exit_confirmation():
        global paused
        response = tkinter.messagebox.askyesno("Potwierdzenie wyjścia", "Czy na pewno chcesz wyjść z gry?", icon='question', detail='')
        if response is not None:
            if response:
                exit_game()
            else:
                paused = False
                okienko.focus_force()
    okienko.title("snake")
    directory = os.path.dirname(os.path.abspath(__file__))
    okienko.iconbitmap(os.path.join(directory, 'snake.ico'))
    def change_direction(e):
        global velocityX, velocityY, game_over, licznik_ruchow, paused
        if not paused:
            if e.keysym == "Up" and velocityY != 1:
                licznik_ruchow += 1
                velocityX = 0
                velocityY = -1
            elif e.keysym == "Down" and velocityY != -1:
                licznik_ruchow += 1
                velocityX = 0
                velocityY = 1
            elif e.keysym == "Left" and velocityX != 1:
                licznik_ruchow += 1
                velocityX = -1
                velocityY = 0
            elif e.keysym == "Right" and velocityX != -1:
                licznik_ruchow += 1
                velocityX = 1
                velocityY = 0

        if e.keysym == "p":
            paused = not paused
        if e.keysym == "Escape":
            paused=not paused
            exit_confirmation()
            

    okienko.bind("<KeyPress>", change_direction)
    
    def move():
        global waz, jedzenie, cialo_weza, game_over, punkty, paused
        if not paused:
            # Jeśli wąż wychodzi poza granice okna, przenieś go na przeciwną stronę
            if waz.x < 0:
                waz.x = SZER_OKNA - TILE_SIZE
            elif waz.x >= SZER_OKNA:
                waz.x = 0
            elif waz.y < 0:
                waz.y = WYS_OKNA - TILE_SIZE
            elif waz.y >= WYS_OKNA:
                waz.y = 0

            for tile in cialo_weza:
                if waz.x == tile.x and waz.y == tile.y:
                    game_over = True
                    def return_menu():
                        over.destroy()
                        menu.deiconify()
                    okienko.withdraw()
                    over = tkinter.Tk()
                    over.title("Przegrales!")
                    over.resizable(False, False)
                    szer_ekranu = over.winfo_screenwidth()
                    wys_ekranu = over.winfo_screenheight()
                    over.geometry(f"{SZER_OKNA}x{WYS_OKNA}+{int((szer_ekranu - SZER_OKNA) / 2)}+{int((wys_ekranu - WYS_OKNA) / 2)}")
                    rysowanie_over = tkinter.Canvas(over, bg="black", width=SZER_OKNA, height=WYS_OKNA, borderwidth=0, highlightthickness=0)
                    rysowanie_over.create_text(SZER_OKNA / 2, WYS_OKNA / 2-120, text="Game Over", fill="red", font=("Arial", 32))
                    rysowanie_over.create_text(60, WYS_OKNA / 2-60, text="Wynik:", fill="white", font=("Arial", 20))
                    rysowanie_over.create_text(60, WYS_OKNA / 2-40, text="liczba ruchow:"+str(licznik_ruchow), fill="white", font=("Arial", 10))
                    rysowanie_over.create_text(60, WYS_OKNA / 2-20, text="liczba punktow:"+str(punkty), fill="white", font=("Arial", 10))
                    #pole do wpisania imienia
                    pole = tkinter.Entry(over)
                    pole.place(relx=0.5, rely=0.4, anchor="center")
                    zapiszWynik_button = tkinter.Button(over, text="Zapisz Wynik", command=lambda: save_score(over, pole, punkty, licznik_ruchow))
                    zapiszWynik_button.place(relx=0.5, rely=0.5, anchor="center")
                    zakoncz_button = tkinter.Button(over, text="Zakoncz gre", command=exit_game)
                    zakoncz_button.place(relx=0.5, rely=0.6, anchor="center")
                    powrot_button = tkinter.Button(over, text="powrot do menu", command=return_menu)
                    powrot_button.place(relx=0.5, rely=0.7, anchor="center")
                    rysowanie_over.pack()
                    over.mainloop()

            # zjadanie
            if waz.x == jedzenie.x and waz.y == jedzenie.y:
                cialo_weza.append(Tile(jedzenie.x, jedzenie.y))
                punkty += 1
                jedzenie.x = random.randint(0, KOLUMNY - 1) * TILE_SIZE
                jedzenie.y = random.randint(0, WIERSZE - 1) * TILE_SIZE

            # aktualizacja długości węża
            for i in range(len(cialo_weza) - 1, -1, -1):
                tile = cialo_weza[i]
                if i == 0:
                    tile.x = waz.x
                    tile.y = waz.y
                else:
                    prev_tile = cialo_weza[i - 1]
                    tile.x = prev_tile.x
                    tile.y = prev_tile.y
            waz.x += velocityX * TILE_SIZE
            waz.y += velocityY * TILE_SIZE
    
    POZYCJA_STAT = 10
    def draw():
        global waz, licznik_ruchow
        
        if not paused:
            okienko.focus_force()
            move()
        rysowanie.delete("all")
        # rysuj jedzenie
        rysowanie.create_rectangle(jedzenie.x, jedzenie.y, jedzenie.x + TILE_SIZE, jedzenie.y + TILE_SIZE, fill="red")

        # rysuj weza
        rysowanie.create_rectangle(waz.x, waz.y, waz.x + TILE_SIZE, waz.y + TILE_SIZE, fill=color)
        #czytaj pozycje weza:
        
        for tile in cialo_weza:
            rysowanie.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill=color)
            rysowanie.create_text(POZYCJA_STAT, WYS_OKNA - 30, anchor="sw", text="Ruchy: " + str(licznik_ruchow), fill="white", font=("Arial", 14))
            rysowanie.create_text(POZYCJA_STAT, WYS_OKNA - 10, anchor="sw", text="Punkty: " + str(punkty), fill="white", font=("Arial", 14))
        if paused:
            rysowanie.create_text(SZER_OKNA // 2, WYS_OKNA // 2, text="PAUZA", fill="red", font=("Arial", 40, 'bold'))
        
        okienko.after(100, draw)   
    licznik_ruchow = 0
    punkty = 0

    draw()
    okienko.mainloop()

# okno menu gry
menu = tkinter.Tk()
menu.title("Menu")

menu.resizable(False, False)

szer_ekranu = menu.winfo_screenwidth()
wys_ekranu = menu.winfo_screenheight()
menu.geometry(f"{SZER_OKNA}x{WYS_OKNA}+{int((szer_ekranu - SZER_OKNA) / 2)}+{int((wys_ekranu - WYS_OKNA) / 2)}")

rysowanie_menu = tkinter.Canvas(menu, bg="black", width=SZER_OKNA, height=WYS_OKNA, borderwidth=0, highlightthickness=0)
rysowanie_menu.pack()
directory = os.path.dirname(os.path.abspath(__file__))
menu.iconbitmap(os.path.join(directory, 'snake.ico'))
rysowanie_menu.create_text(SZER_OKNA // 2, 50, text="Snake 🐍", fill="white", font=("Arial", 40))
start_button = tkinter.Button(menu, text="Rozpocznij grę", command=color_selection)
start_button.place(relx=0.5, rely=0.5, anchor="center")
wyniki_button = tkinter.Button(menu, text="Tablica Wynikow", command=tablica_wynikow)
wyniki_button.place(relx=0.5, rely=0.55, anchor="center")
wyjscie_button = tkinter.Button(menu, text="Wyjdz", command=exit_game)
wyjscie_button.place(relx=0.5, rely=0.6, anchor="center")

menu.mainloop()
