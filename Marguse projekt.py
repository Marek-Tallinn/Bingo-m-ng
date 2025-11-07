import random
import time
import sys

sümbolid = ['🍒', '🍋', '🍉', '𝟕']

pank = 100
panus = 0

# Statistika
keerude_arv = 0 #testimise jaoks
kokku_võidetud = 0
kokku_kaotatud = 0
sümbolite_loendur = {'🍒':0, '🍋':0, '🍉':0, '𝟕':0}

#kuvab rulle aeglaselt
def aeglane_rull():
    rullid = [' ', ' ', ' ', ' ']       # Algselt tühjad
    for i in range(10):     # Mitu korda rullid keerlevad
        for j in range(4):
            rullid[j] = random.choice(sümbolid)
        sys.stdout.write('\r' + ' | '.join(rullid) + '  ')
        sys.stdout.flush()
        time.sleep(0.1 + j*0.05)     # Iga rull peatub veidi hiljem
    print('\n')
    time.sleep(0.67)
    for sümbol in rullid:
        sümbolite_loendur[sümbol] += 1
    return tuple(rullid)

#mäng ise
def mäng():
    global pank, panus, keerude_arv, kokku_võidetud, kokku_kaotatud
    print("🎰 Tere tulemast slottide juurde! 🎰\n")
    print(f'Sul on praegu {pank}€.')
    while pank > 0:
        sisend = input("\nSisesta arv, mida soovite panustada ('Exit' lõpetamiseks): ")

        if sisend.lower() == "exit":
            print(f'Mäng läbi. Lõppsaldo: {pank}€')
            break       # Kui kirjutad 'exit' siis mäng lõppeb.

        try:
            panus = int(sisend)
        except ValueError:
            print("Sisesta sobilik täisarv.")
            continue        # Kontrollib kas see on number.

        if panus > pank:
            print('Sa oled liiga vaene selle panuse jaoks.')
            continue        # Rikkuse kontroll

        pank -= panus
        kokku_kaotatud += panus
        r1, r2, r3, r4 = aeglane_rull()
        keerude_arv += 1        # Keerutamise loendur

        if r1 == r2 == r3 == r4:        # JACKPOT
            võit = panus * 10
            pank += võit
            kokku_võidetud += võit
            print(f'🎉 JACKPOT 🎉\nVõitsid {võit}€.')
        elif r1 == r2 == r3 or r1 == r3 == r4 or r2 == r3 == r4 or r1 == r2 == r4:      # Noobide võit
            võit = panus * 2
            pank += võit
            kokku_võidetud += võit
            print(f'Võit!\nSinu võidu summa on {võit}€.')
        else:
            print("Kaotasid selle korra.\n")      # Kaotamise jaoks
        
        print(f'Praegune saldo: {pank}€')       # Lõpptulemus

    if pank == 0:
        print('\nMäng läbi, sattusid omadega nulli.')     # Kui raha saab otsa, siis enam mängida ei saa

    # Lõppstatistika
    print('\n=== MÄNGU STATISTIKA ===')
    print(f'Keerutasid kokku {keerude_arv} korda.')
    print(f'Kogukaotus: {kokku_kaotatud}€')
    print(f'Koguvõit: {kokku_võidetud}€')
    print(f'Lõppsaldo: {pank}€')
    print("Sümbolite sagedus mängu jooksul:")
    for sümbol, arv in sümbolite_loendur.items():
        print(f'{sümbol}: {arv} korda')
mäng()
