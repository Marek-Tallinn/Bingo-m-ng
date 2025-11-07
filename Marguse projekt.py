import random
import time

sümbolid = ['🍒', '🍋', '🍉', '𝟕']

pank = 100
panus = 0
keerude_arv = 0 #testimise jaoks

#kuvab rulle aeglaselt
def aeglane_rull():
    rull_1 = random.choice(sümbolid)
    rull_2 = random.choice(sümbolid)
    rull_3 = random.choice(sümbolid)
    rull_4 = random.choice(sümbolid)
    print('Rullimine...\n')
    time.sleep(0.67)
    print(f"[ {rull_1}  |  {rull_2}  |  {rull_3}  |  {rull_4}  ]\n")
    return rull_1, rull_2, rull_3, rull_4

#mäng ise
def mäng():
    global pank, panus, keerude_arv
    print("🎰 Tere tulemast slottide juurde! 🎰\n")
    print(f'Sul on praegu {pank}€.')
    while pank > 0:     # Rullimine ise

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
        r1, r2, r3, r4 = aeglane_rull()
        keerude_arv += 1        # Keerutamise loendur

        if r1 == r2 == r3 == r4:        # Võidu kontroll
            võit = panus * 10
            pank += võit
            print(f'🎉 JACKPOT 🎉\nVõitsid {võit}€.')
        elif r1 == r2 == r3 or r1 == r3 == r4 or r2 == r3 == r4 or r1 == r2 == r4:      # Noobide võit
            võit = panus * 2
            pank += võit
            print(f'Võit!\nSinu võidu summa on {võit}€.')
        else:
            print("Kaotasid selle korra.")      # Kaotamise jaoks
        
        print(f'Praegune saldo: {pank}€')       # Lõpptulemus

    if pank == 0:
        print('Mäng läbi, sattusid omadega nulli.')     # Kui raha saab otsa, siis enam mängida ei saa
    
    print(f'Keerutasid kokku {keerude_arv} korda.')     # Statistika
mäng()
