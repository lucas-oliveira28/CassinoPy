import random as rd
import time
import pandas as pd


def save():
    global game_round
    salvar = pd.read_excel('save.xlsx')
    salvar.loc[salvar["STATS"] == 'MONEY', 'VALOR'] = player_1.money
    salvar.loc[salvar["STATS"] == 'PTS', 'VALOR'] = player_1.pts
    salvar.loc[salvar["STATS"] == 'LIMIT', 'VALOR'] = player_1.limit
    salvar.loc[salvar["STATS"] == 'DEBTS', 'VALOR'] = player_1.debts
    salvar.loc[salvar["STATS"] == 'GAMEROUND', 'VALOR'] = game_round
    salvar.to_excel('save.xlsx', index=False)


def load():
    global game_round
    loadar = pd.read_excel('save.xlsx')
    player_1.money = loadar.at[0, 'VALOR']
    player_1.pts = loadar.at[1, 'VALOR']
    player_1.limit = loadar.at[2, 'VALOR']
    player_1.debts = loadar.at[3, 'VALOR']
    game_round = loadar.at[4, 'VALOR']
    loadar.to_excel('save.xlsx', index=False)


def t(sec):
    time.sleep(sec)


class Player:
    def __init__(self, money, pts, card, limit, debts, rank):
        self.money = money
        self.pts = pts
        self.card = card
        self.limit = limit
        self.debts = debts
        self.rank = rank


class Croupier:
    def __init__(self, card):
        self.card = card


def ranking():
    global multi_pay
    if player_1.pts < 10:
        player_1.rank = 'Bronze'
        multi_pay = 1
    elif player_1.pts >= 10:
        player_1.rank = 'Silver'
        multi_pay = 1.5
    elif player_1.pts >= 25:
        player_1.rank = 'Gold'
        multi_pay = 2
    elif player_1.pts >= 50:
        player_1.rank = 'Platinum'
        multi_pay = 2.5
    elif player_1.pts >= 100:
        player_1.rank = 'Diamond'
        multi_pay = 3


def credit_card():
    credit_pay = 0
    credit_call = 0
    credit_pay_min = 20
    print('Seu limite é de R$ %s' % player_1.limit)
    if player_1.limit >= credit_pay_min:
        while credit_call == 0:
            try:
                t(.5)
                credit_pay = int(input('\nEscolha [0] para sair\nQuanto você quer emprestado?:    '))
            except:
                print('\n')
            if credit_pay == 0:
                t(.5)
                credit_call = 1
            elif credit_pay > player_1.limit:
                t(.5)
                print('\nValor excede o seu limite!')
            elif credit_pay < credit_pay_min:
                t(.5)
                print('\nValor abaixo do mínimo - R$ %s' % credit_pay_min)
            elif credit_pay_min <= credit_pay <= player_1.limit:
                t(.5)
                print('\nVocê transferiu R$ %s para sua conta!' % credit_pay)
                t(.5)
                player_1.money += credit_pay
                player_1.limit -= credit_pay
                player_1.debts += credit_pay
                credit_call = 1
    else:
        t(.5)
        print('Você não tem mais limite disponível!\n')
        t(.5)
        print('Pague seus débitos!\n')


def debits():
    check_debits = 0
    option_4 = 0
    t(.5)
    print('Seu débito é de R$ %s!' % player_1.debts)
    while check_debits == 0:
        try:
            t(.5)
            option_4 = int(input('[0] - Para sair\nQuanto você deseja pagar?:    '))
        except:
            print('\n')
        if option_4 == 0:
            check_debits = 1
        elif player_1.money >= option_4:
            if option_4 <= player_1.debts:
                player_1.debts -= option_4
                player_1.money -= option_4
                player_1.limit += option_4
                t(.5)
                print('Você R$ %s da sua dívida!' % option_4)
                t(.5)
                print('Sua dívida agora é de R$ %s' % player_1.debts)
                check_debits = 1
            else:
                player_1.money -= option_4
                troco = option_4 - player_1.debts
                player_1.money += troco
                player_1.limit += player_1.debts
                player_1.debts = 0
                t(.5)
                print('Você pagou toda sua dívida de R$ %s e recebeu R$ %s de troco!' % (player_1.debts, troco))
                check_debits = 1
        else:
            print('Opção Inválida!')


def fees():
    global game_round
    if player_1.debts > 0:
        game_round += 1
        if game_round < 5:
            t(.5)
            print('\nPague seus débitos em até %s dias, ou irá sofrer juros!' % (5 - game_round))
        elif game_round == 5:
            t(.5)
            player_1.debts *= 1.03
            print('\nSeus juros começão hoje! Cuidado para não acumular dívidas!')
        elif game_round > 5:
            player_1.debts *= 1.03
    else:
        game_round = 0


def ia_croupier():
    global bet_amount
    global multi_pay
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
                player_1.money += bet_amount * multi_pay
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
                player_1.money += bet_amount * multi_pay
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
                player_1.money += bet_amount * multi_pay
                result = 1
        else:
            print('Opção inválida!')


def bet():
    global bet_amount

    bet_check = 0
    bet_amount = 0
    min_bet = 20
    print('Você tem R$ %s\n' % player_1.money)
    if player_1.money < min_bet:
        print('Você não tem dinheiro suficiente para iniciar uma aposta!\n')
        t(.5)
        print('Tente conseguir um empréstimo\n')
        bet_check = 1
        game_over()
    while bet_check == 0:
        try:
            t(.5)
            bet_amount = int(input('Quanto deseja apostar?:   '))
        except:
            print('\n')
        if bet_amount > player_1.money:
            print('Você não tem todo esse dinheiro!')
        elif bet_amount < min_bet:
            print('A aposta mínima é R$ %s!' % min_bet)
        elif min_bet <= bet_amount <= player_1.money:
            bet_check = 1
        else:
            print('Opção inválida!')


def game_over():
    global game_active
    global option_2
    global game_round

    if player_1.money < 20 and player_1.limit < 20:
        print('Você está quebrado!!\n')
        t(1)
        print('---- GAME OVER ----')
        t(1)
        print('***** Obrigado por jogar!! *****')
        player_1.money = 100
        player_1.pts = 0
        player_1.limit = 200
        player_1.debts = 0
        game_round = 0
        save()
        game_active = False
        option_2 = 1


global game_active
global option_2
global game_round
global multi_pay

game_round = 0
player_1 = Player(0, 0, 0, 0, 0, 'Bronze')
croupier = Croupier(0)

game_active = True

while game_active:
    global bet_amount
    load()
    print('***** Bem Vindo ao CASSINO ROYALE! *****')
    option_2 = 0
    answer = 0
    t(.5)
    while option_2 == 0:
        try:
            t(.5)
            answer = int(input('[1] - Iniciar jogo   [2] - Cartão de Crédito   [3] - Ver Status'   
                               '   [4] - Sair do Jogo:   '))
            t(.5)
        except:
            print('\n')
        if answer == 1:
            bet()
            if bet_amount > 0:
                ranking()
                ia_croupier()
                fees()
                game_over()
                save()
        elif answer == 2:
            t(.5)
            print('O que você deseja?')
            check = 0
            option_3 = 0
            while check == 0:
                try:
                    t(.5)
                    option_3 = int(input('\n[1] - Pegar Dinheiro\n[2] - Pagar Débito\n[3] - Voltar ao Menu'))
                except:
                    print('\n')
                if option_3 == 1:
                    credit_card()
                    check = 1
                elif option_3 == 2:
                    debits()
                    check = 1
                elif option_3 == 3:
                    t(.5)
                    check = 1
                else:
                    print('Opção Inválida!')
            save()
        elif answer == 3:
            t(.5)
            print('Dinheiro: %s\nPontos: %s\nLimite: R$ %s\nDébito: R$ %s\nRank: %s' % (
                  player_1.money, player_1.pts, player_1.limit, player_1.debts, player_1.rank))
        elif answer == 4:
            t(.5)
            print('***** Obrigado por jogar!! *****')
            option_2 = 1
            game_active = False
        else:
            print('Opção Inválida!!')
