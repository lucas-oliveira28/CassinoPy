import random as rd
import time


def t(sec):
    time.sleep(sec)


class Player:
    def __init__(self, money, pts, card):
        self.money = money
        self.pts = pts
        self.card = card


class Croupier:
    def __init__(self, card):
        self.card = card


player_1 = Player(100, 0, 0)
croupier = Croupier(0)


def ia_croupier():
    global bet_amount
    result = 0
    option = 0
    croupier.card = 0
    croupier.card = rd.randint(1, 11)
    player_1.card = 0
    player_1.card += rd.randint(1, 11)
    print('\n------ Aposta Iniciada! ------\n')
    t(.5)
    print('O Croupier tirou um %s!' % croupier.card)
    t(.5)
    print('Você tirou um %s' % player_1.card)
    t(.5)

    while result == 0:
        try:
            option = int(input('O que deseja?\n[1] - Pegar Carta\n[2] - Parar:    '))
            t(.5)
        except:
            print('\n')
        if option == 1:
            new_card = rd.randint(1, 11)
            player_1.card += new_card
            if player_1.card == 21:
                print('\nVocê tirou %s e fez um %s!!\n' % (new_card, player_1.card))
                t(.5)
                print('Você ganhou !!')
                result = 1
                player_1.pts += 3
                player_1.money += bet_amount
                t(.5)
            elif player_1.card > 21:
                print('\nVocê tirou %s e estourou com %s!!\n' % (new_card, player_1.card))
                t(.5)
                print('Você perdeu!')
                player_1.pts -= 2
                result = 1
                player_1.money -= bet_amount
                t(.5)
            else:
                print('\nVocê tirou %s e agora tem %s' % (new_card, player_1.card))
                t(.5)
        elif option == 2:
            while croupier.card < 17:
                new_card = rd.randint(1, 11)
                croupier.card += new_card
                print('O Croupier tirou %s e agora tem %s\n' % (new_card, croupier.card))
                t(1)
            if croupier.card == 21:
                print('Você perdeu!\n')
                player_1.pts -= 1
                player_1.money -= bet_amount
                result = 1
            elif croupier.card > 21:
                print('O Croupier estourou!\n')
                t(.5)
                print('Você ganhou!!')
                player_1.pts += 1
                player_1.money += bet_amount
                result = 1
            elif croupier.card == player_1.card:
                print('O Croupier e você tem um %s' % croupier.card)
                t(.5)
                print('Empate!')
                result = 1
            elif player_1.card < croupier.card < 21:
                print('O Croupier tem um %s e você tem um %s\n' % (croupier.card, player_1.card))
                t(.5)
                print('Você perdeu!\n')
                player_1.pts -= 1
                player_1.money -= bet_amount
                result = 1
            else:
                print('O Croupier tem um %s e você tem um %s\n' % (croupier.card, player_1.card))
                t(.5)
                print('Você ganhou!\n')
                player_1.pts += 1
                player_1.money += bet_amount
                result = 1
        else:
            print('Opção inválida!')


def bet():
    global bet_amount

    bet_check = 0
    bet_amount = 0
    print('Você tem R$ %s\n' % player_1.money)
    while bet_check == 0:
        try:
            t(.5)
            bet_amount = int(input('Quanto deseja apostar?:   '))
        except:
            print('\n')
        if bet_amount > player_1.money:
            print('Você não tem todo esse dinheiro!')
        elif bet_amount <= 0:
            print('Opção inválida!')
        elif 0 < bet_amount <= player_1.money:
            bet_check = 1
        else:
            print('Opção inválida!')


def game_over():
    global game_active
    global option_2
    if player_1.money == 0:
        print('Você está quebrado!!\n')
        t(1)
        print('---- GAME OVER ----')
        t(1)
        print('***** Obrigado por jogar!! *****')
        game_active = False
        option_2 = 1


global game_active
global option_2

game_active = True

while game_active:
    print('***** Bem Vindo ao CASSINO ROYALE! *****')
    option_2 = 0
    answer = 0
    t(.5)
    while option_2 == 0:
        try:
            answer = int(input('[1] - Iniciar jogo   [2] - Ver Status   [3] - Sair do Jogo:   '))
            t(.5)
        except:
            print('\n')
        if answer == 1:
            bet()
            ia_croupier()
            game_over()
        elif answer == 2:
            print('Dinheiro: %s\nPontos: %s' % (player_1.money, player_1.pts))
            t(.5)
        elif answer == 3:
            print('***** Obrigado por jogar!! *****')
            option_2 = 1
            game_active = False
        else:
            print('Opção Inválida!!')
