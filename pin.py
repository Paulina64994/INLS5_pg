import tkinter as tk
import random

# Parametry planszy
szerokosc = 800
wysokosc = 400
paletka_dlugosc = 100
paletka_szerokosc = 10
pilka_promien = 20
paletka_predkosc = 10
pilka_predkosc_x = 10
pilka_predkosc_y = 10

# Inicjalizacja okna Tkinter
root = tk.Tk()
root.title("Ping Pong")

# Inicjalizacja canvas
canvas = tk.Canvas(root, width=szerokosc, height=wysokosc)
canvas.pack()

# Paletki
paletka_A = canvas.create_rectangle(
    50, wysokosc // 2 - paletka_dlugosc // 2,
    50 + paletka_szerokosc, wysokosc // 2 + paletka_dlugosc // 2,
    fill="blue"
)

paletka_B = canvas.create_rectangle(
    szerokosc - 50 - paletka_szerokosc, wysokosc // 2 - paletka_dlugosc // 2,
    szerokosc - 50, wysokosc // 2 + paletka_dlugosc // 2,
    fill="red"
)

# Piłka
pilka = canvas.create_oval(
    szerokosc // 2 - pilka_promien, wysokosc // 2 - pilka_promien,
    szerokosc // 2 + pilka_promien, wysokosc // 2 + pilka_promien,
    fill="green"
)

# Dodaj flagę, która wskazuje, czy gra jest w trakcie
gra_w_trakcie = False

# Funkcja do rozpoczęcia gry po wciśnięciu przycisku "Start"
def rozpocznij_gre():
    global gra_w_trakcie
    if not gra_w_trakcie:
        gra_w_trakcie = True
        przycisk_start.destroy()  # Usuń przycisk "Start"
        przycisk_restart.pack_forget()  # Usuń przycisk "Restart", jeśli istnieje
        
        # Inicjalizacja pozycji piłki
        global pilka_x, pilka_y, pilka_predkosc_x, pilka_predkosc_y
        pilka_x = szerokosc // 2
        pilka_y = wysokosc // 2
        pilka_predkosc_x = 10
        pilka_predkosc_y = 10
        
        # Rozpocznij ruch piłki
        ruch_pilka()

# Funkcje do ruchu paletki A
def ruch_paletka_A_gora(event):
    pozycja_paletki_A = canvas.coords(paletka_A)
    if pozycja_paletki_A[1] > 0:
        canvas.move(paletka_A, 0, -paletka_predkosc)

def ruch_paletka_A_dol(event):
    pozycja_paletki_A = canvas.coords(paletka_A)
    if pozycja_paletki_A[3] < wysokosc:
        canvas.move(paletka_A, 0, paletka_predkosc)

# Funkcje do ruchu paletki B
def ruch_paletka_B_gora(event):
    pozycja_paletki_B = canvas.coords(paletka_B)
    if pozycja_paletki_B[1] > 0:
        canvas.move(paletka_B, 0, -paletka_predkosc)

def ruch_paletka_B_dol(event):
    pozycja_paletki_B = canvas.coords(paletka_B)
    if pozycja_paletki_B[3] < wysokosc:
        canvas.move(paletka_B, 0, paletka_predkosc)

# Funkcja do ruchu piłki
def ruch_pilka():
    global pilka_x, pilka_y, pilka_predkosc_x, pilka_predkosc_y
    
    # Aktualizacja pozycji piłki
    pilka_x += pilka_predkosc_x
    pilka_y += pilka_predkosc_y
    
    # Odbicie piłki od górnej i dolnej krawędzi planszy
    if pilka_y - pilka_promien <= 0 or pilka_y + pilka_promien >= wysokosc:
        pilka_predkosc_y = -pilka_predkosc_y
    
    # Sprawdzenie kolizji z paletkami
    pozycja_paletki_A = canvas.coords(paletka_A)
    pozycja_paletki_B = canvas.coords(paletka_B)
    
    if (pilka_x - pilka_promien <= pozycja_paletki_A[2] and
        pozycja_paletki_A[1] <= pilka_y <= pozycja_paletki_A[3]):
        pilka_predkosc_x = -pilka_predkosc_x
    
    if (pilka_x + pilka_promien >= pozycja_paletki_B[0] and
        pozycja_paletki_B[1] <= pilka_y <= pozycja_paletki_B[3]):
        pilka_predkosc_x = -pilka_predkosc_x
    
    # Resetowanie pozycji piłki, jeśli wyleci poza planszę
    if pilka_x - pilka_promien <= 0 or pilka_x + pilka_promien >= szerokosc:
        pilka_x = szerokosc // 2
        pilka_y = wysokosc // 2
        pilka_predkosc_x = -pilka_predkosc_x
        pilka_predkosc_y = random.choice([-1, 1]) * pilka_predkosc_y
        
        # Wywołaj funkcję rozpoczęcia gry ponownie
        rozpocznij_gre()
    
    # Przesunięcie piłki na nową pozycję
    canvas.coords(pilka, pilka_x - pilka_promien, pilka_y - pilka_promien,
                  pilka_x + pilka_promien, pilka_y + pilka_promien)
    
    # Wywołanie funkcji ponownie po pewnym czasie
    if gra_w_trakcie:
        root.after(50, ruch_pilka)

# Funkcja do restartu gry
def zrestartuj_gre():
    global gra_w_trakcie
    gra_w_trakcie = False
    przycisk_restart.pack_forget()  # Usuń przycisk "Restart"
    przycisk_start.pack()  # Wyświetl przycisk "Start" ponownie

# Przypisanie funkcji do przycisków
root.bind("w", ruch_paletka_A_gora)
root.bind("s", ruch_paletka_A_dol)
root.bind("<Up>", ruch_paletka_B_gora)
root.bind("<Down>", ruch_paletka_B_dol)

# Dodaj przycisk do rozpoczęcia gry
przycisk_start = tk.Button(root, text="Start", command=rozpocznij_gre)
przycisk_start.pack()

# Dodaj przycisk do restartu gry
przycisk_restart = tk.Button(root, text="Restart", command=zrestartuj_gre)

# Uruchomienie aplikacji
root.mainloop()