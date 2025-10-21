import random

# BINGO mängus on 5 veergu: B, I, N, G ja O.
# Igal veerul on oma numbrivahemik (nagu päris Bingos).
bingo_reeglid = {
    'B': range(1, 16),
    'I': range(16, 31),
    'N': range(31, 46),
    'G': range(46, 61),
    'O': range(61, 76)
}

def saa_bingo_pall(kasutatud_pallid):
    """
    Loosib ühe uue bingopalli (1–75).
    Tagab, et sama number ei tuleks kaks korda.
    """
    kõik_pallid = list(range(1, 76))  # kõik võimalikud numbrid
    saadavad_pallid = set(kõik_pallid) - kasutatud_pallid  # need, mida pole veel loositud

    if saadavad_pallid:  # kui veel on midagi loosi panna
        pall = random.choice(list(saadavad_pallid))  # võta üks suvaline number
        kasutatud_pallid.add(pall)  # lisa see kasutatud numbrite hulka
        return pall  # tagasta uus pall
    return None  # kui kõik numbrid on juba välja võetud

def bingo_kaart(kaart):
    """
    Kontrollib, kas mängijal on täis rida, veerg või diagonaal.
    Kui jah, siis on see võit.
    """
    read_veerud_diag = kaart[:]  # koopia kaartist (et mitte muuta originaali)

    # lisa kõik veerud kontrollimiseks
    for c in range(5):
        read_veerud_diag.append([kaart[r][c] for r in range(5)])

    # lisa kaks diagonaali kontrollimiseks
    read_veerud_diag.append([kaart[i][i] for i in range(5)])      # vasak diagonaal
    read_veerud_diag.append([kaart[i][4 - i] for i in range(5)])  # parem diagonaal

    # kui mõni rida/veerg/diagonaal koosneb ainult X-idest → võit!
    return any(all(cell == "X" for cell in rida) for rida in read_veerud_diag)

def genereeri_kaart():
    """
    Genereerib ühe juhusliku BINGO kaardi.
    Iga veerg saab oma vahemiku numbrid.
    """
    kaart = [[0]*5 for _ in range(5)]  # loob tühja 5x5 tabeli (kaardi)
    veerud = ['B', 'I', 'N', 'G', 'O']  # veergude nimed

    # täidab iga veeru juhuslike numbritega vastavast vahemikust
    for col in range(5):
        numbrid = random.sample(list(bingo_reeglid[veerud[col]]), 5)
        for row in range(5):
            kaart[row][col] = numbrid[row]

    kaart[2][2] = "X"  # keskmine ruut on alati vaba
    return kaart  # tagastab valmis kaardi

def print_kaart(kaart, mängija_nimi=None):
    """
    Prindib kaardi ilusalt PowerShelli/konsooli.
    """
    if mängija_nimi:  # kui on antud mängija nimi, näita seda
        print(f"\n{mängija_nimi} kaart:")
    print(" B   I   N   G   O")  # veergude päis
    for row in kaart:  # iga rea kuvamine
        print(' '.join(str(x).rjust(2) for x in row))  # numbrid joondatud paremale
    print()  # tühi rida eraldamiseks

def loo_mängijad():
    """
    Küsib kasutajalt, mitu mängijat mängib.
    Loob igale mängijale ühe uue BINGO kaardi.
    """
    mängijad = []  # nimekiri mängijatest
    mitu_mängijat = int(input("Mitu mängijat mängib? "))

    # loo igale mängijale tema kaart
    for i in range(1, mitu_mängijat + 1):
        kaart = genereeri_kaart()
        mängijad.append({
            'nimi': f"Mängija {i}",
            'kaart': kaart
        })
    return mängijad

def mängi_bingot():
    """
    Peafunktsioon – juhib kogu mängu kulgu.
    """
    mängijad = loo_mängijad()  # loo mängijad ja nende kaardid
    kasutatud_pallid = set()   # hoiab meeles, mis numbrid on juba loositud

    print("\n🎲 Mäng algab! 🎲\n")

    # näita kõigi mängijate algkaarte
    for mängija in mängijad:
        print_kaart(mängija['kaart'], mängija['nimi'])

    # peamine mängutsükkel
    while True:
        pall = saa_bingo_pall(kasutatud_pallid)  # loosi uus pall

        if pall is None:  # kui kõik numbrid on juba välja loositud
            print("Kõik bingopallid on välja võetud. Mäng jäi viiki.")
            break

        print(f"\nUus bingopall: {pall}\n")  # näita uut numbrit

        # kontrolli iga mängija kaarti
        for mängija in mängijad:
            kaart = mängija['kaart']

            # märgi number X-iga, kui see kaardil on
            for i in range(5):
                for j in range(5):
                    if kaart[i][j] == pall:
                        kaart[i][j] = "X"

            # prindi uuendatud kaart välja
            print_kaart(kaart, mängija['nimi'])

            # kontrolli, kas mängija võitis
            if bingo_kaart(kaart):
                print(f"\n🎉 {mängija['nimi']} võitis! 🎉")
                return  # lõpetab mängu

        # lase mängijal vajutada Enter, et järgmine number loosida
        input("Vajuta Enter, et loosida järgmine pall...")

# Kui faili käivitatakse otse, alustatakse mängu
if __name__ == "__main__":
    mängi_bingot()
