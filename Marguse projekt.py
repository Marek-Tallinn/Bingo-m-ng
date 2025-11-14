import random
import time
import sys
import os
from operator import itemgetter
from datetime import datetime, timedelta

leaderboard_fail = "leaderboard.txt"

sümbolid = ['🍒', '🍋', '🍉', '𝟕']

pank = 250
panus = 0
kasutaja = ""

# Statistika
keerude_arv = 0
kokku_võidetud = 0
kokku_kaotatud = 0
sümbolite_loendur = {'🍒':0, '🍋':0, '🍉':0, '𝟕':0}

# Kuvab rulle aeglaselt
def aeglane_rull():
    rullid = [' ', ' ', ' ', ' ']
    lõpuseis = []
    
    for j in range(4):
        for _ in range(10):
            rullid[j] = random.choice(sümbolid)
            sys.stdout.write('\r' + ' | '.join(rullid) + '  ')
            sys.stdout.flush()
            time.sleep(0.1)
        lõpuseis.append(random.choice(sümbolid))
        rullid[j] = lõpuseis[-1]
        sys.stdout.write('\r' + ' | '.join(rullid))
        sys.stdout.flush()
        time.sleep(0.2)
    print('\n')
    for sümbol in lõpuseis:
        sümbolite_loendur[sümbol] += 1
    return tuple(lõpuseis)

# Edetabeli salvestamine (3 päeva säilitamist)
def salvesta_edetabel(nimi, lõppsaldo):

    algne_saldo = 250
    mängija_võitis = lõppsaldo - algne_saldo

    if mängija_võitis <= 0:
        return
    
    # Kui fail eksisteerib, kontrollime vanust
    if os.path.exists(leaderboard_fail):
        try:
            tabel_aeg = datetime.fromtimestamp(os.path.getmtime(leaderboard_fail))
            if datetime.now() - tabel_aeg > timedelta(days=3):
                open(leaderboard_fail, "w").close()  # Tühjenda edetabel
        except Exception:
            pass

    try:
        with open(leaderboard_fail, "r", encoding="utf-8") as f:
            read_data = f.readlines()
        tulemused = []
        nimed_failis = set()
        for rida in read_data:
            osa = rida.strip().split(",")
            if len(osa) == 2:
                nimi_exist = osa[0].strip()
                võit_exist = int(osa[1].replace('€', '').strip(1))
                tulemused.append([nimi_exist, võit_exist])
                nimed_failis.add(nimi_exist)
    except FileNotFoundError:
        tulemused = []
        nimed_failis = set()
    
    if nimi not in nimed_failis:
        tulemused.append([nimi, mängija_võitis])

    tulemused = sorted(tulemused, key=itemgetter(1), reverse=True)

    with open(leaderboard_fail, "w", encoding="utf-8") as f:
        for nimi_, võit in tulemused[:10]:
            f.write(f"{nimi_}, {võit}€\n")

# Edetabeli kuvamine
def kuva_statistika_ja_edetabel():
    kogusaldo = pank - 250
    print("\n=== MÄNGU STATISTIKA ===")
    print(f"Keerutasid kokku {keerude_arv} korda.")
    print(f"Kogukaotus: -{kokku_kaotatud}€")
    print(f"Koguvõit: {kokku_võidetud}€")
    if kogusaldo >= 0:
        print(f"Kogusaldo: {kogusaldo}€")
    else:
        print(f"Kogusaldo: {kogusaldo}€")
    print("Sümbolite sagedus mängu jooksul:")
    for sümbol, arv in sümbolite_loendur.items():
        print(f"{sümbol}: {arv} korda")

    
    print("\n=== EDETABEL (TOP 5)===")
    if not os.path.exists(leaderboard_fail):
        print("(Edetabel on tühi)")
        return
    with open(leaderboard_fail, "r", encoding="utf-8") as f:
        read_data = f.readlines()
        if not read_data:
            print("(Edetabel on tühi)")
            return
        
        medaljonid = ["🥇", "🥈", "🥉"]
        for i, rida in enumerate(read_data[:5], start=1):
            medal = medaljonid[i-1] if i <= 3 else f"{i}."
            print(f"{medal} {rida.strip()}")

# Mäng
def mäng():
    global pank, panus, keerude_arv, kokku_võidetud, kokku_kaotatud, kasutaja

    kasutaja = input("Sisesta oma kasutajanimi: ")
    print("🎰 Tere tulemast slottide juurde! 🎰\n")
    print(f"Sul on praegu {pank}€.")

    while pank > 0:
        sisend = input("\nSisesta arv (arvulise väärtusena), mida soovite panustada ('Exit' lõpetamiseks): ")

        if sisend.lower() == "exit":
            print(f"Mäng läbi. Lõppsaldo: {pank}€")
            break

        try:
            panus = int(sisend)
        except ValueError:
            print("Sisesta sobilik täisarv.")
            continue

        if panus > pank:
            print("Sa oled liiga vaene selle panuse jaoks.")
        elif panus < 0:
            print("Sisesta positiivne täisarv...")
            continue

        pank -= panus
        kokku_kaotatud += panus
        r1, r2, r3, r4 = aeglane_rull()
        keerude_arv += 1

        if r1 == r2 == r3 == r4:
            võit = panus * 10
            pank += võit
            kokku_võidetud += võit
            print(f"🎉 JACKPOT 🎉\nVõitsid {võit}€.")
        elif r1 == r2 == r3 or r1 == r3 == r4 or r2 == r3 == r4 or r1 == r2 == r4:
            võit = panus * 2
            pank += võit
            kokku_võidetud += võit
            print(f"Võit!\nSinu võidu summa on {võit}€.")
        else:
            print("Kaotasid selle korra.\n")

        print(f"Praegune saldo: {pank}€")

    if pank == 0:
        print("\nMäng läbi, sattusid omadega nulli.")

    # Lõppstatistika

    salvesta_edetabel(kasutaja, pank)
    kuva_statistika_ja_edetabel()
mäng()
