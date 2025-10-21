import tkinter as tk
import random
from tkinter import messagebox

# Loome BINGO kaardi
def loo_kaart():
    veerud = {
        'B': range(1, 16),
        'I': range(16, 31),
        'N': range(31, 46),
        'G': range(46, 61),
        'O': range(61, 76)
    }
    kaart = []
    for v in ['B', 'I', 'N', 'G', 'O']:
        kaart.append(random.sample(veerud[v], 5))
    kaart = [list(rida) for rida in zip(*kaart)]
    kaart[2][2] = "X"  # keskkoht on vaba
    return kaart

def on_võit(kaart):
    # read
    for rida in kaart:
        if all(x == "X" for x in rida):
            return True
    # veerud
    for j in range(5):
        if all(kaart[i][j] == "X" for i in range(5)):
            return True
    # diagonaalid
    if all(kaart[i][i] == "X" for i in range(5)) or all(kaart[i][4 - i] == "X" for i in range(5)):
        return True
    return False

class BingoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lihtne Bingo")
        self.kasutatud = set()
        self.kaart = loo_kaart()

        self.raam = tk.Frame(root)
        self.raam.pack(pady=10)

        # Näita BINGO kaarti
        self.lahtrid = []
        for i in range(5):
            rida = []
            for j in range(5):
                lbl = tk.Label(self.raam, text=str(self.kaart[i][j]), width=4, height=2,
                               relief="ridge", font=("Arial", 12))
                lbl.grid(row=i, column=j, padx=2, pady=2)
                rida.append(lbl)
            self.lahtrid.append(rida)

        # Loosimise nupp
        self.pall_label = tk.Label(root, text="Pole veel loosi", font=("Arial", 14))
        self.pall_label.pack(pady=5)

        tk.Button(root, text="🎱 Uus pall", command=self.loosipall).pack(pady=5)

    def loosipall(self):
        kõik = set(range(1, 76))
        saadaval = list(kõik - self.kasutatud)
        if not saadaval:
            messagebox.showinfo("Lõpp", "Kõik pallid on välja võetud!")
            return

        pall = random.choice(saadaval)
        self.kasutatud.add(pall)
        self.pall_label.config(text=f"Uus pall: {pall}")

        # Märgi X, kui leidub
        for i in range(5):
            for j in range(5):
                if self.kaart[i][j] == pall:
                    self.kaart[i][j] = "X"
                    self.lahtrid[i][j].config(text="X", bg="lightgreen")

        # Kontrolli võitu
        if on_võit(self.kaart):
            messagebox.showinfo("🎉 Võit!", "Sul on BINGO!")
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BingoApp(root)
    root.mainloop()