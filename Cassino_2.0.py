import random as rd
import time
import random
import pandas as pd
import os

global game_active
global option_2
global game_round
global multi_pay
global new_card
global luck
global resets
global game


class Player:
    def __init__(self, money, pts, rank, card):
        self.money = money
        self.pts = pts
        self.rank = rank
        self.card = card


class Croupier:
    def __init__(self, card):
        self.card = card


def save():
    global game_round
    global resets
    salvar = pd.read_excel('save.xlsx')
    salvar.loc[salvar["STATS"] == 'MONEY', 'VALOR'] = int(player_1.money)
    salvar.loc[salvar["STATS"] == 'PTS', 'VALOR'] = int(player_1.pts)
    salvar.loc[salvar["STATS"] == 'RESETS', 'VALOR'] = int(resets)
    salvar.to_excel('save.xlsx', index=False)


def load():
    global game_round
    global resets
    loadar = pd.read_excel('save.xlsx')
    player_1.money = loadar.at[0, 'VALOR']
    player_1.pts = loadar.at[1, 'VALOR']
    resets = loadar.at[2, 'VALOR']
    loadar.to_excel('save.xlsx', index=False)


def game_type():
    global game
    global game_active
    game = 0
    option_3 = 0
    cls()
    while option_3 == 0:
        try:
            if game == 0:
                game = int(input('[1] - Black Jack  [2] - Slots\n[0] - Sair do jogo'))
        except:
            print('\n')
        if game == 1:
            if game_active:
                cls()
                bet()
                if bet_amount > 0:
                    ranking()
                    game_hud_bj()
                    game_over()
                    save()
                else:
                    option_3 = 1
            elif not game_active:
                option_3 = 1
        elif game == 2:
            if game_active:
                cls()
                bet_slot()
                if bet_amount > 0:
                    game_hud_slot()
                    game_over()
                    save()
                else:
                    option_3 = 1
            elif not game_active:
                option_3 = 1
        elif game == 0:
            option_3 = 1
        else:
            print('Opção Inválida!')


def t(sec):
    time.sleep(sec)


def ranking():
    global multi_pay
    if player_1.pts < 10:
        player_1.rank = 'Bronze'
        multi_pay = 1
    elif 10 <= player_1.pts < 25:
        player_1.rank = 'Silver'
        multi_pay = 1.5
    elif 25 <= player_1.pts < 50:
        player_1.rank = 'Gold'
        multi_pay = 2
    elif 50 <= player_1.pts < 100:
        player_1.rank = 'Platinum'
        multi_pay = 2.5
    elif player_1.pts >= 100:
        player_1.rank = 'Diamond'
        multi_pay = 3


def lucky():
    global new_card
    global luck
    sort = rd.randint(0, 100)
    if player_1.pts > 0:
        if sort >= (95 - int(player_1.pts / 10) - resets):
            luck = True
            print('\n*** Você se sente sortudo ***\n')
            t(1)
            new_card = 21 - player_1.card


def sight():
    global visionary
    global new_card
    vis = rd.randint(0, 100)
    if player_1.pts > 0:
        if vis >= (80 - int(player_1.pts / 10) - resets):
            visionary = True
            new_card = rd.randint(1, 11)
            t(.5)
            print('\n*** Sua intuição lhe diz que a próxima carta é um %s!***\n' % new_card)
            t(1)


def cls():
    t(.5)
    os.system('cls')


def game_hud_bj():
    global bet_amount
    global multi_pay
    global new_card
    global luck
    global visionary
    visionary = False
    luck = False
    result = 0
    option = 0
    croupier.card = 0
    croupier.card = rd.randint(1, 11)
    player_1.card = 0
    player_1.card += rd.randint(1, 11)
    print('\n------ Aposta Iniciada! ------\n')
    t(.5)
    print('O Croupier tirou\n'
          '     -----\n'
          '     | %s |\n'
          '     -----' % croupier.card)
    t(.5)
    print('\nVocê tirou\n'
          '  -----\n'
          '  | %s |\n'
          '  -----' % player_1.card)
    t(.5)

    while result == 0:
        try:
            option = int(input('O que deseja?\n[1] - Pegar Carta\n[2] - Parar:    '))
            t(.5)
        except:
            print('\n')
        if option == 1 and visionary:
            player_1.card += new_card
            if player_1.card == 21:
                print('\nVocê tirou\n'
                      '  -----\n'
                      '  | %s |\n'
                      '  -----' % new_card)
                t(.5)
                print('\nVocê fez um %s!!\n' % player_1.card)
                t(.5)
                print('Você ganhou !!')
                result = 1
                player_1.pts += 3
                player_1.money += bet_amount * multi_pay * 1.5
            elif player_1.card > 21:
                print('\nVocê tirou\n'
                      '  -----\n'
                      '  | %s |\n'
                      '  -----' % new_card)
                t(.5)
                print('\nVocê estourou com %s!!\n' % player_1.card)
                t(.5)
                print('Você perdeu!')
                player_1.pts -= 2
                result = 1
                player_1.money -= bet_amount
            else:
                print('\nVocê tirou\n'
                      '  -----\n'
                      '  | %s |\n'
                      '  -----' % new_card)
                print('\nVocê agora tem %s\n' % player_1.card)
                t(.5)
            visionary = False
        elif option == 1 and luck:
            player_1.card += new_card
            print('\nVocê tirou\n'
                  '  -----\n'
                  '  | %s |\n'
                  '  -----' % new_card)
            t(.5)
            print('\nVocê fez um %s!!\n' % player_1.card)
            t(.5)
            print('Você ganhou !!')
            result = 1
            player_1.pts += 3
            player_1.money += bet_amount * multi_pay * 1.5
            luck = False
        elif option == 1:
            new_card = rd.randint(1, 11)
            player_1.card += new_card
            if player_1.card == 21:
                print('\nVocê tirou\n'
                      '  -----\n'
                      '  | %s |\n'
                      '  -----' % new_card)
                t(.5)
                print('\nVocê fez um %s!!\n' % player_1.card)
                t(.5)
                print('Você ganhou !!')
                result = 1
                player_1.pts += 3
                player_1.money += bet_amount * multi_pay * 1.5
            elif player_1.card > 21:
                print('\nVocê tirou\n'
                      '  -----\n'
                      '  | %s |\n'
                      '  -----' % new_card)
                t(.5)
                print('\nVocê estourou com %s!!\n' % player_1.card)
                t(.5)
                print('Você perdeu!')
                player_1.pts -= 2
                result = 1
                player_1.money -= bet_amount
            else:
                print('\nVocê tirou\n'
                      '  -----\n'
                      '  | %s |\n'
                      '  -----' % new_card)
                print('\nVocê agora tem %s\n' % player_1.card)
                if player_1.card >= 10:
                    lucky()
                if player_1.card > 11 and not luck:
                    sight()
                t(.5)
        elif option == 2:
            while croupier.card < 17:
                new_card = rd.randint(1, 11)
                croupier.card += new_card
                print('O Croupier tirou\n'
                      '     -----\n'
                      '     | %s |\n'
                      '     -----' % new_card)
                print('\nO Croupier agora tem %s\n' % croupier.card)
                t(1)
            if croupier.card == 21:
                print('\nVocê perdeu!\n')
                player_1.pts -= 1
                player_1.money -= bet_amount
                result = 1
            elif croupier.card > 21:
                print('\nO Croupier estourou!\n')
                t(.5)
                print('Você ganhou!!\n')
                player_1.pts += 2
                player_1.money += bet_amount * multi_pay
                result = 1
            elif croupier.card == player_1.card:
                print('\nO Croupier e você tem um %s\n' % croupier.card)
                t(.5)
                print('Empate!\n')
                result = 1
            elif player_1.card < croupier.card < 21:
                print('\nO Croupier tem um %s e você tem um %s\n' % (croupier.card, player_1.card))
                t(.5)
                print('Você perdeu!\n')
                player_1.pts -= 1
                player_1.money -= bet_amount
                result = 1
            else:
                print('O Croupier tem um %s e você tem um %s\n' % (croupier.card, player_1.card))
                t(.5)
                print('Você ganhou!\n')
                player_1.pts += 2
                player_1.money += bet_amount * multi_pay
                result = 1
        else:
            print('Opção inválida!')
    t(.5)


def bet():
    global bet_amount

    bet_check = 0
    bet_amount = 0
    min_bet = 20
    print('Você tem R$ %s\n' % player_1.money)
    if player_1.money < min_bet:
        print('Você não tem dinheiro suficiente para iniciar uma aposta!\n')
        bet_check = 1
        game_over()
    while bet_check == 0:
        try:
            t(.5)
            bet_amount = int(input('[0] - Para sair\nQuanto deseja apostar?:   '))
        except:
            print('\n')
        if bet_amount == 0:
            bet_check = 1
            cls()
        elif bet_amount > player_1.money:
            print('Você não tem todo esse dinheiro!')
        elif bet_amount < min_bet:
            print('A aposta mínima é R$ %s!' % min_bet)
        elif min_bet <= bet_amount <= player_1.money:
            bet_check = 1
        else:
            print('Opção inválida!')
    t(.5)


def bet_slot():
    global bet_amount

    bet_check = 0
    bet_amount = 0
    min_bet = 1
    print('Você tem R$ %s\n' % player_1.money)
    if player_1.money < min_bet:
        print('Você não tem dinheiro suficiente para iniciar uma aposta!\n')
        bet_check = 1
        game_over()
    while bet_check == 0:
        try:
            t(.5)
            bet_amount = int(input('[0] - Para sair\nQuanto deseja apostar?:   '))
        except:
            print('\n')
        if bet_amount == 0:
            bet_check = 1
            cls()
        elif bet_amount > player_1.money:
            print('Você não tem todo esse dinheiro!')
        elif bet_amount < min_bet:
            print('A aposta mínima é R$ %s!' % min_bet)
        elif min_bet <= bet_amount <= player_1.money:
            bet_check = 1
        else:
            print('Opção inválida!')
    t(.5)


def game_over():
    global game_active
    global option_2
    global game_round
    global resets
    global playing

    if player_1.money < 1:
        print('\nVocê está quebrado!!\n')
        t(1)
        print(C['R'], '---- GAME OVER ----\n', C['E'])
        t(1)
        print('***** Obrigado por jogar!! *****')
        t(2)
        player_1.money = 100
        player_1.pts = 0
        game_round = 0
        save()
        game_active = False
        option_2 = 1
        playing = False
    elif player_1.money >= 1000000000:
        print('\nVocê está bilionário!!\n')
        t(1)
        print('---- GAME OVER ----\n')
        t(1)
        print('***** Obrigado por jogar!! *****')
        t(2)
        player_1.money = 100
        player_1.pts = resets * 20
        save()
        game_active = False
        option_2 = 1


def graphic_slot():
    slot_1 = random.choice(symbol)
    slot_2 = random.choice(symbol)
    slot_3 = random.choice(symbol)
    slot_4 = random.choice(symbol)
    slot_5 = random.choice(symbol)
    slot_6 = random.choice(symbol)
    slot_7 = random.choice(symbol)
    slot_8 = random.choice(symbol)
    slot_9 = random.choice(symbol)

    print(' | %s | %s | %s | ( )\n'
          ' ----------------  |\n'
          ' | %s | %s | %s |  |\n'
          ' ----------------  |\n'
          ' | %s | %s | %s |\n' % (slot_1, slot_2, slot_3, slot_4, slot_5, slot_6, slot_7, slot_8, slot_9))
    print('\n\nSaldo Atual: R$ %s\n' % (player_1.money - bet_amount))
    time.sleep(.5)
    os.system('cls')
    print(' | %s | %s | %s |   ( )\n'
          ' ----------------   /\n'
          ' | %s | %s | %s |  /\n'
          ' ---------------- /\n'
          ' | %s | %s | %s |\n' % (slot_1, slot_2, slot_3, slot_4, slot_5, slot_6, slot_7, slot_8, slot_9))
    print('\n\nSaldo Atual: R$ %s\n' % (player_1.money - bet_amount))
    time.sleep(.1)
    os.system('cls')
    print(' | %s | %s | %s |\n'
          ' ----------------\n'
          ' | %s | %s | %s |\n'
          ' ---------------- -----( )\n'
          ' | %s | %s | %s |\n' % (slot_1, slot_2, slot_3, slot_4, slot_5, slot_6, slot_7, slot_8, slot_9))
    print('\n\nSaldo Atual: R$ %s\n' % (player_1.money - bet_amount))
    time.sleep(.1)
    os.system('cls')
    print(' | %s | %s | %s |\n'
          ' ----------------\n'
          ' | %s | %s | %s |\n'
          ' ---------------- \\\n'
          ' | %s | %s | %s |  \\\n'
          '                    \\\n'
          '                    ( )\n ' % (slot_1, slot_2, slot_3, slot_4, slot_5, slot_6, slot_7, slot_8, slot_9))
    print('Saldo Atual: R$ %s\n' % (player_1.money - bet_amount))
    time.sleep(.1)
    os.system('cls')
    print(' | %s | %s | %s |\n'
          ' ----------------\n'
          ' | %s | %s | %s |\n'
          ' ----------------  |\n'
          ' | %s | %s | %s |  |\n'
          '                   |\n'
          '                  ( )\n ' % (slot_1, slot_2, slot_3, slot_4, slot_5, slot_6, slot_7, slot_8, slot_9))
    print('Saldo Atual: R$ %s\n' % (player_1.money - bet_amount))
    time.sleep(.1)


def game_hud_slot():
    cls()
    global bet_amount
    global playing
    playing = True
    rounds = 0
    while playing:
        try:
            if rounds > 0 and player_1.money >= bet_amount:
                option_5 = 1848
            else:
                option_5 = int(input('\nENTER para girar!    [1] - Automático    [0] - Para mudar valor'))
        except:
            option_5 = 1848
        if option_5 == 1:
            rounds = 0
            option_6 = 0
            option_7 = 0
            while option_6 == 0:
                try:
                    option_7 = int(input('[1] - 5 Giros\n[2] - 10 Giros\n[3] - 20 Giros\n[0] - Voltar'))
                except:
                    print('\n')
                if option_7 == 1:
                    rounds = 5
                    option_6 = 1
                elif option_7 == 2:
                    rounds = 10
                    option_6 = 1
                elif option_7 == 3:
                    rounds = 20
                    option_6 = 1
                elif option_7 == 0:
                    option_6 = 1
                else:
                    print('Opção Inválida!')
        elif option_5 == 1848:
            spin = 17
            slot_1 = random.choice(symbol)
            slot_2 = random.choice(symbol)
            slot_3 = random.choice(symbol)
            slot_4 = random.choice(symbol)
            slot_5 = random.choice(symbol)
            slot_6 = random.choice(symbol)
            slot_7 = random.choice(symbol)
            slot_8 = random.choice(symbol)
            slot_9 = random.choice(symbol)
            cls()
            graphic_slot()
            while spin > 0:
                os.system('cls')
                if spin > 11:
                    slot_7 = slot_4
                    slot_8 = slot_5
                    slot_9 = slot_6
                    slot_4 = slot_1
                    slot_5 = slot_2
                    slot_6 = slot_3
                    slot_1 = random.choice(symbol)
                    slot_2 = random.choice(symbol)
                    slot_3 = random.choice(symbol)
                    print(' | %s | %s | %s |\n'
                          ' ----------------\n'
                          ' | %s | %s | %s |\n'
                          ' ----------------\n'
                          ' | %s | %s | %s |\n' % (
                           slot_1, slot_2, slot_3, slot_4, slot_5, slot_6, slot_7, slot_8, slot_9))
                    print('\n\nSaldo Atual: R$ %s\n' % (player_1.money - bet_amount))
                    if rounds > 0:
                        print('Giros restantes: %s\n' % (rounds - 1))
                    time.sleep(.2)
                elif 11 >= spin >= 6:
                    slot_8 = slot_5
                    slot_9 = slot_6
                    slot_5 = slot_2
                    slot_6 = slot_3
                    slot_2 = random.choice(symbol)
                    slot_3 = random.choice(symbol)
                    print(C["G"], ' | %s |' % slot_1, C["E"], '| %s | %s |\n' % (slot_2, slot_3),
                          C["G"], '------', C["E"], '-----------\n',
                          C["G"], '| %s |' % slot_4, C["E"], '| %s | %s |\n' % (slot_5, slot_6),
                          C["G"], '------', C["E"], '-----------\n',
                          C["G"], '| %s |' % slot_7, C["E"], '| %s | %s |\n' % (slot_8, slot_9))
                    print('\n\nSaldo Atual: R$ %s\n' % (player_1.money - bet_amount))
                    if rounds > 0:
                        print('Giros restantes: %s\n' % (rounds - 1))
                    time.sleep(.2)
                elif 0 < spin < 6:
                    slot_9 = slot_6
                    slot_6 = slot_3
                    slot_3 = random.choice(symbol)
                    print(C["G"], ' | %s | %s |' % (slot_1, slot_2), C["E"], '| %s |\n' % slot_3,
                          C["G"], '-----------', C["E"], '------\n',
                          C["G"], '| %s | %s |' % (slot_4, slot_5), C["E"], '| %s |\n' % slot_6,
                          C["G"], '-----------', C["E"], '------\n',
                          C["G"], '| %s | %s |' % (slot_7, slot_8), C["E"], '| %s |\n' % slot_9, )
                    print('\n\nSaldo Atual: R$ %s\n' % (player_1.money - bet_amount))
                    if rounds > 0:
                        print('Giros restantes: %s\n' % (rounds - 1))
                    time.sleep(.2)
                if spin == 1:
                    os.system('cls')
                    print(C["G"], ' | %s | %s | %s |\n'
                          '  ----------------\n'
                          '  | %s | %s | %s |\n'
                          '  ----------------\n'
                          '  | %s | %s | %s |\n' % (
                          slot_1, slot_2, slot_3, slot_4, slot_5, slot_6, slot_7, slot_8, slot_9), C["E"])
                    print('\n\nSaldo Atual: R$ %s\n' % (player_1.money - bet_amount))
                    if rounds > 0:
                        print('Giros restantes: %s\n' % (rounds - 1))
                spin -= 1

            win = False
            multi = 0
            rounds -= 1
            t(.5)
            if slot_2 == slot_1 and slot_1 == slot_3:
                print('Você ganhou na horizontal 1')
                win = True
                if slot_2 == symbol[0]:
                    multi += 4
                elif slot_2 == symbol[1]:
                    multi += 2
                elif slot_2 == symbol[2]:
                    multi += 1
                elif slot_2 == symbol[3]:
                    multi += .5
            if slot_1 == slot_5 and slot_5 == slot_9:
                print('Você ganhou na diagonal 1')
                win = True
                if slot_1 == symbol[0]:
                    multi += 6
                elif slot_1 == symbol[1]:
                    multi += 3
                elif slot_1 == symbol[2]:
                    multi += 2
                elif slot_1 == symbol[3]:
                    multi += 1
            if slot_3 == slot_5 and slot_5 == slot_7:
                print('Você ganhou na diagonal 2')
                win = True
                if slot_1 == symbol[0]:
                    multi += 6
                elif slot_1 == symbol[1]:
                    multi += 3
                elif slot_1 == symbol[2]:
                    multi += 2
                elif slot_1 == symbol[3]:
                    multi += 1
            if slot_4 == slot_5 and slot_5 == slot_6:
                print('Você ganhou na horizontal 2')
                win = True
                if slot_4 == symbol[0]:
                    multi += 14
                elif slot_4 == symbol[1]:
                    multi += 10
                elif slot_4 == symbol[2]:
                    multi += 6
                elif slot_4 == symbol[3]:
                    multi += 4
            if slot_7 == slot_8 and slot_8 == slot_9:
                print('Você ganhou na horizontal 3')
                win = True
                if slot_2 == symbol[0]:
                    multi += 4
                elif slot_2 == symbol[1]:
                    multi += 2
                elif slot_2 == symbol[2]:
                    multi += 1
                elif slot_2 == symbol[3]:
                    multi += .5
            time.sleep(0.5)
            if not win:
                player_1.money -= bet_amount
                print(C['R'], '\nVocê não ganhou nada!', C['E'])
                game_over()
                save()
            else:
                premio = (bet_amount * multi) + bet_amount
                player_1.money += (premio - bet_amount)
                print(C['G'], '\nVocê ganhou um premio total de R$ %s!' % premio, C['E'])
                save()
        elif option_5 == 0:
            playing = False
        else:
            print('\nOpção Inválida!\n')


os.system("color")
C = {
    "H": "\033[95m",
    "B": "\033[94m",
    "G": "\033[92m",
    "R": "\033[91m",
    "E": "\033[0m",
}
game_round = 0
symbol = ['💲', '❤️', '🌟', '🍒']
player_1 = Player(0, 0, 'Bronze', 0)
croupier = Croupier(0)
resets = 0
game_active = True

while game_active:
    global bet_amount
    global game
    load()
    print('***** Bem Vindo ao CASSINO ROYALE! *****')
    option_2 = 0
    answer = 0
    ranking()
    t(.5)
    while option_2 == 0:
        try:
            t(.5)
            answer = int(input('[1] - Iniciar jogo   [2] - Ver Status'
                               '   [3] - Sair do Jogo:   '))
        except:
            print('\n')
        if answer == 1:
            cls()
            game_type()
        elif answer == 2:
            cls()
            print('Dinheiro: %s\nPontos: %s\nRank: %s\nResets: %s' % (
                player_1.money, player_1.pts, player_1.rank, resets))
        elif answer == 3:
            cls()
            print('***** Obrigado por jogar!! *****\n')
            print('Autor do jogo: Lucas Monteiro de Oliveira')
            t(2)
            option_2 = 1
            game_active = False
        else:
            print('Opção Inválida!!')
