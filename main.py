import time
import pandas as pd
import numpy as np
import datetime as dt

import pytz
timezone = pytz.timezone('America/Sao_Paulo')

import warnings
warnings.filterwarnings('ignore')

import cryptocompare
cryptocompare_api_key = '00ff6c8217eec5d6894a77d4bc335d5306072e0e22fc1af970bf0f68f00eb6bf'
#cryptocompare.cryptocompare._set_api_key_parameter(api_key=cryptocompare_api_key)

import telebot
telegram_chat_id = '452513294'  # CMS  - '452513294'   # Mae - '1031430125'
telegram_token = '1238835452:AAGTATI9bldZfHtD2iMrvHiVztz9DguLHck'  # TamoNaBolsa
telegram_token = '1853621782:AAEv8V-r8engZScvTQLolfMKOmeJ0DXv5dU'  # CMSCriptoBot

def decimal_to_str(valor: float = 0.0, formato: str = "{0:,.2f}") -> str:
    try:
        return formato.format(valor).replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        try:
            return "{0:,.2f}".format(valor)
        except:
            return valor

def get_price(moeda: str):
    try:
        coin, currency = moeda.split('/')
        # result = cryptocompare.get_price(coin=coin, currency=currency)
        # value = result[coin][currency] if result and result[coin] and result[coin][currency] else 0.0
        result = cryptocompare.get_price(coin=coin, currency=currency, full=True)
        value = result['RAW'][coin][currency]['PRICE']  # result['DISPLAY'][coin][currency]['PRICE']
        change = result['RAW'][coin][currency]['CHANGEPCT24HOUR']  # result['DISPLAY'][coin][currency]['CHANGEPCT24HOUR']
        return value, change
    except:
        return 0.0, 0.0

def buscar_trades():
    try:

        htmlTrades = """

CONTA	TRADE	PAR	TIPO	QUANTIDADE	PREÇO	TOTAL	TAXA	DATA
258442	4424429	ETH/BRL	Compra	Ξ 0,19637191	R$ 12.745,03	R$ 2.502,76	Ξ 0,00098185	10-06-2021 14:07
258442	4424428	LINK/BRL	Compra	LINK 31,62555344	R$ 126,44	R$ 3.998,73	LINK 0,15812776	10-06-2021 14:07
258442	4424426	XRP/BRL	Compra	XRP 895,499884	R$ 4,465	R$ 3.999,212	XRP 4,477499	10-06-2021 14:07
258442	4424423	LTC/BRL	Compra	Ł 3,49210304	R$ 863,41	R$ 3.015,15	Ł 0,01746051	10-06-2021 14:06
258442	4424422	LTC/BRL	Compra	Ł 1,13988600	R$ 863,29	R$ 984,06	Ł 0,00569943	10-06-2021 14:06

CONTA	TRADE	PAR	TIPO	QUANTIDADE	PREÇO	TOTAL	TAXA	DATA
258442	4398809	ETH/BRL	Compra	Ξ 0,39277378	R$ 12.787,50	R$ 5.022,59	Ξ 0,00196386	08-06-2021 08:05
258442	4398805	LINK/BRL	Compra	LINK 74,18803514	R$ 123,63	R$ 9.171,86	LINK 0,37094017	08-06-2021 08:05
258442	4398804	LINK/BRL	Compra	LINK 6,96420000	R$ 123,02	R$ 856,80	LINK 0,03482100	08-06-2021 08:05
258442	4398798	XRP/BRL	Compra	XRP 370,735389	R$ 4,450	R$ 1.649,772	XRP 1,853676	08-06-2021 08:05
258442	4398797	XRP/BRL	Compra	XRP 1.839,412000	R$ 4,443	R$ 8.172,507	XRP 9,197060	08-06-2021 08:05
258442	4398796	XRP/BRL	Compra	XRP 40,000000	R$ 4,443	R$ 177,719	XRP 0,200000	08-06-2021 08:05
258442	4398794	LTC/BRL	Compra	Ł 12,14033854	R$ 819,26	R$ 9.946,09	Ł 0,06070169	08-06-2021 08:05

CONTA	TRADE	PAR	TIPO	QUANTIDADE	PREÇO	TOTAL	TAXA	DATA
258442	4337482	ETH/BRL	Compra	Ξ 0,12784441	R$ 13.444,12	R$ 1.718,75	Ξ 0,00063922	31-05-2021 10:20
258442	4337481	ETH/BRL	Compra	Ξ 0,00712229	R$ 13.444,00	R$ 95,75	Ξ 0,00003561	31-05-2021 10:20
258442	4337480	ETH/BRL	Compra	Ξ 0,46047100	R$ 13.443,99	R$ 6.190,57	Ξ 0,00230235	31-05-2021 10:20
258442	4337479	XRP/BRL	Compra	XRP 804,574710	R$ 5,346	R$ 4.301,256	XRP 4,022873	31-05-2021 10:20
258442	4337478	XRP/BRL	Compra	XRP 1.066,000000	R$ 5,342	R$ 5.695,531	XRP 5,330000	31-05-2021 10:20
258442	4337475	LINK/BRL	Compra	LINK 4,49679114	R$ 157,02	R$ 706,08	LINK 0,02248395	31-05-2021 10:19
258442	4337474	LINK/BRL	Compra	LINK 59,00000000	R$ 156,79	R$ 9.251,15	LINK 0,29500000	31-05-2021 10:19
258442	4337473	LINK/BRL	Compra	LINK 6,65030000	R$ 156,79	R$ 1.042,76	LINK 0,03325150	31-05-2021 10:19
258442	4337469	LTC/BRL	Compra	Ł 13,33552196	R$ 974,70	R$ 12.998,13	Ł 0,06667760	31-05-2021 10:19

CONTA	TRADE	PAR	TIPO	QUANTIDADE	PREÇO	TOTAL	TAXA	DATA
258442	4144545	ETH/BRL	Compra	Ξ 1,89948130	R$ 13.699,64	R$ 26.022,20	Ξ 0,00949740	19-05-2021 08:53
258442	4144495	LINK/BRL	Compra	LINK 49,23601049	R$ 177,07	R$ 8.718,22	LINK 0,24618005	19-05-2021 08:52
258442	4144494	LINK/BRL	Compra	LINK 7,21970000	R$ 177,06	R$ 1.278,39	LINK 0,03609850	19-05-2021 08:52
258442	4144488	XRP/BRL	Compra	XRP 411,565455	R$ 7,371	R$ 3.033,648	XRP 2,057827	19-05-2021 08:52
258442	4144487	XRP/BRL	Compra	XRP 943,000000	R$ 7,370	R$ 6.950,758	XRP 4,715000	19-05-2021 08:52
258442	4144400	LTC/BRL	Compra	Ł 6,35135801	R$ 1.321,29	R$ 8.391,98	Ł 0,03175679	19-05-2021 08:50
258442	4144399	LTC/BRL	Compra	Ł 1,21654500	R$ 1.321,28	R$ 1.607,40	Ł 0,00608272	19-05-2021 08:50

CONTA	TRADE	PAR	TIPO	QUANTIDADE	PREÇO	TOTAL	TAXA	DATA
258442	3990900	XRP/BRL	Compra	XRP 372,648305	R$ 7,807	R$ 2.909,265	XRP 1,863241	11-05-2021 20:26

CONTA	TRADE	PAR	TIPO	QUANTIDADE	PREÇO	TOTAL	TAXA	DATA
258442	3872788	CHZ/BRL	Venda	CHZ 21,41489504	R$ 2,860	R$ 61,246	R$ 0,306	04-05-2021 17:56
258442	3872787	CHZ/BRL	Venda	CHZ 17,42160278	R$ 2,870	R$ 49,999	R$ 0,249	04-05-2021 17:56
258442	3872786	CHZ/BRL	Venda	CHZ 86,80555554	R$ 2,880	R$ 249,999	R$ 1,249	04-05-2021 17:56
258442	3872785	CHZ/BRL	Venda	CHZ 17,31826715	R$ 2,880	R$ 49,876	R$ 0,249	04-05-2021 17:56
258442	3872784	CHZ/BRL	Venda	CHZ 1,00000000	R$ 2,900	R$ 2,900	R$ 0,014	04-05-2021 17:56
258442	3872783	CHZ/BRL	Venda	CHZ 338,44938108	R$ 2,900	R$ 981,503	R$ 4,907	04-05-2021 17:56
258442	3858089	CHZ/BRL	Venda	CHZ 482,40970161	R$ 2,820	R$ 1.360,395	R$ 6,801	04-05-2021 08:47

CONTA	TRADE	PAR	TIPO	QUANTIDADE	PREÇO	TOTAL	TAXA	DATA
258442	3812272	CHZ/BRL	Compra	CHZ 969,66774193	R$ 3,100	R$ 3.005,969	CHZ 4,84833870	01-05-2021 14:24

CONTA	TRADE	PAR	TIPO	QUANTIDADE	PREÇO	TOTAL	TAXA	DATA
258442	3771523	LINK/BRL	Compra	LINK 15,12554199	R$ 198,32	R$ 2.999,69	LINK 0,07562770	28-04-2021 15:14
258442	3771521	XRP/BRL	Compra	XRP 404,154710	R$ 7,414	R$ 2.996,766	XRP 2,020773	28-04-2021 15:13
258442	3771518	LTC/BRL	Compra	Ł 2,12693551	R$ 1.410,03	R$ 2.999,04	Ł 0,01063467	28-04-2021 15:13

CONTA	TRADE	PAR	TIPO	QUANTIDADE	PREÇO	TOTAL	TAXA	DATA
258442	3751921	LTC/BRL	Compra	Ł 3,60227952	R$ 1.387,60	R$ 4.998,52	Ł 0,01801139	27-04-2021 00:41

CONTA	TRADE	PAR	TIPO	QUANTIDADE	PREÇO	TOTAL	TAXA	DATA
258442	3727392	LINK/BRL	Compra	LINK 26,18075191	R$ 190,98	R$ 4.999,99	LINK 0,13090375	25-04-2021 10:38

CONTA	TRADE	PAR	TIPO	QUANTIDADE	PREÇO	TOTAL	TAXA	DATA
258442	3719789	XRP/BRL	Compra	XRP 830,523840	R$ 6,209	R$ 5.157,469	XRP 4,152619	24-04-2021 09:12

CONTA	TRADE	PAR	TIPO	QUANTIDADE	PREÇO	TOTAL	TAXA	DATA
258442	3716590	ETH/BRL	Compra	Ξ 0,31163302	R$ 12.799,98	R$ 3.988,89	Ξ 0,00155816	23-04-2021 23:47
258442	3716589	ETH/BRL	Compra	Ξ 0,02016491	R$ 12.799,98	R$ 258,11	Ξ 0,00010082	23-04-2021 23:47
258442	3716588	ETH/BRL	Compra	Ξ 0,05904694	R$ 12.752,39	R$ 752,98	Ξ 0,00029523	23-04-2021 23:47
        """

        return htmlTrades

    except Exception as e:
        print(f'Falha Geral - buscar_trades: {str(e)}')

def montar_trades(html):
    try:

        def montar_listas(html):
            lstTrades = html.split('\n')  # criar lista por quebra de linha
            lstTrades = [row for row in lstTrades if str(row).strip() != '']  # remover linhas em branco
            lstTrades = [row.split('\t') for row in lstTrades]  # criar colunas, por tab = \t
            lstTrades = [[row.strip() for row in trade if str(row).strip() != ''] for trade in lstTrades]  # remover colunas em branco
            return lstTrades

        def montar_dataframe(lstTrades):

            data = lstTrades[1:]  # os registros são do indice 1 até o penultimo indice
            columns = lstTrades[:1][0]  # o indice 1 é as colunas

            df = pd.DataFrame(data=data, columns=columns)

            # df.columns = ['CONTA', 'TRADE', 'PAR',      'TIPO', 'QUANTIDADE', 'PRECO', 'TOTAL', 'TAXA', 'DATA']
            df.columns = ['CONTA', 'TRADE', 'MOEDA', 'TIPO', 'QUANTIDADE', 'PRECO', 'TOTAL', 'TAXA', 'DATA']

            df.drop(df.loc[df['CONTA'] == 'CONTA'].index, inplace=True)
            df.sort_index(ascending=False, inplace=True)
            df.reset_index(inplace=True)

            df['CONTA'] = df['CONTA'].apply(pd.to_numeric, errors='ignore')  # df['CONTA'] = pd.to_numeric(df['CONTA'])
            df['TRADE'] = df['TRADE'].apply(pd.to_numeric, errors='ignore')
            df['QUANTIDADE'] = df['QUANTIDADE'].map(lambda x: ''.join([i for i in x if i.isdigit() or i == '.' or i == ',']).replace('.', '').replace(',', '.')).astype(np.float64)
            df['PRECO'] = df['PRECO'].map(lambda x: ''.join([i for i in x if i.isdigit() or i == '.' or i == ',']).replace('.', '').replace(',', '.')).astype(np.float64)
            df['TOTAL'] = df['TOTAL'].map(lambda x: ''.join([i for i in x if i.isdigit() or i == '.' or i == ',']).replace('.', '').replace(',', '.')).astype(np.float64)
            df['TAXA'] = df['TAXA'].map(lambda x: ''.join([i for i in x if i.isdigit() or i == '.' or i == ',']).replace('.', '').replace(',', '.')).astype(np.float64)
            df['DATA'] = pd.to_datetime(df['DATA'], errors='ignore', format="%d-%m-%Y %H:%M")

            df = df[['DATA', 'MOEDA', 'TIPO', 'QUANTIDADE', 'PRECO', 'TOTAL', 'TAXA']]

            # Compra == TAXA ==  XRP 1,863241 /  CHZ 4,84833870 / LINK 0,07562770 / Ł 0,01801139 / Ξ 0,00155816	 # LTC = Ł # ETH = Ξ
            # Venda    == TAXA ==  R$ 0,306

            df['IDX'] = df.index.map(lambda x: int(x))
            df['TOTAL'] = df.apply(lambda x: x.TOTAL * -1 if x.TIPO == 'Venda' else x.TOTAL, axis=1)
            df['QTDE_AJUSTADA'] = df.apply(lambda x: float(float(x.QUANTIDADE) * -1) if x.TIPO == 'Venda' else float(x.QUANTIDADE) - (float(x.TAXA) if x.TAXA else 0.0), axis=1, )
            df['QTDE_CUSTODIA'] = 0.0
            df['QTDE_CUSTODIA_ANT'] = 0.0
            df['PRECO_MEDIO'] = 0.0
            df['PRECO_ATUAL'] = 0.0
            df['VALRZ_ATUAL'] = 0.0

            return df

        def calcular_dataframe(df):

            for moeda in df['MOEDA'].unique():

                df['QTDE_CUSTODIA'].loc[df['MOEDA'] == moeda] = df['QTDE_AJUSTADA'].loc[df['MOEDA'] == moeda].cumsum()
                df['QTDE_CUSTODIA'].loc[df['MOEDA'] == moeda] = df['QTDE_CUSTODIA'].apply(lambda x: float(x) if round(x, 2) > 0.0 else 0.0)
                df['QTDE_CUSTODIA_ANT'].loc[df['MOEDA'] == moeda] = df['QTDE_CUSTODIA'].loc[df['MOEDA'] == moeda].shift(1, fill_value=0)

                preco_atual, valoriz_atual = get_price(moeda=moeda)
                df['PRECO_ATUAL'].loc[df['MOEDA'] == moeda] = float(preco_atual)
                df['VALRZ_ATUAL'].loc[df['MOEDA'] == moeda] = float(valoriz_atual)

                df_ativo = df.loc[df['MOEDA'] == moeda].copy()
                df_ativo.reset_index(drop=True, inplace=True)
                df_ativo.fillna(0, inplace=True)
                df.fillna(0, inplace=True)

                for idx, row in df_ativo.iterrows():
                    if row['QTDE_AJUSTADA'] > 0:
                        preco_medio_atual = df_ativo['PRECO_MEDIO'].shift(1, fill_value=df_ativo['PRECO'].iloc[0])[idx]
                        qtd_custodia_anterior = df_ativo['QTDE_CUSTODIA_ANT'][idx]
                        valor_da_compra_atual = row['TOTAL']
                        preco_medio = (valor_da_compra_atual + (preco_medio_atual * qtd_custodia_anterior)) / df_ativo['QTDE_CUSTODIA'][idx]
                        df_ativo.loc[idx, 'PRECO_MEDIO'] = preco_medio  # df_ativo.iloc[idx, df_ativo.columns == 'PRECO_MEDIO'] = preco_medio
                        df['PRECO_MEDIO'].loc[(df['MOEDA'] == moeda) & (df['IDX'] == row['IDX'])] = preco_medio
                    else:
                        pass
                        try:
                            preco_medio_atual = df_ativo['PRECO_MEDIO'][idx - 1]
                            df_ativo.loc[idx, 'PRECO_MEDIO'] = preco_medio_atual
                            df['PRECO_MEDIO'].loc[(df['MOEDA'] == moeda) & (df['IDX'] == row['IDX'])] = preco_medio_atual
                        except:
                            pass

            df.fillna(0, inplace=True)

            return df

        lstTrades = montar_listas(html=html)
        df = montar_dataframe(lstTrades=lstTrades)
        df = calcular_dataframe(df=df)

        return df

    except Exception as e:
        print(f'Falha Geral - buscar_trades: {str(e)}')

def gerar_msg_alerta_cripto(df, somenteSaldo: bool = False) -> str:

    msg = ''
    msg += f'<u><b>Alerta Cripto</b></u><br><br>'

    geral_total_invest = 0.0
    geral_total_atual = 0.0
    geral_total_lucro = 0.0
    geral_percent_lucro = 0.0

    for moeda in df['MOEDA'].unique():

        df_new_ativo = df.loc[df['MOEDA'] == moeda].copy()

        item_quantidade = df_new_ativo.iloc[-1]['QTDE_CUSTODIA']

        if float(item_quantidade) <= 0.0:
            continue

        item_preco_medio = df_new_ativo.iloc[-1]['PRECO_MEDIO']
        # item_preco_atual, item_percent_valoriz_atual = get_price(moeda=moeda)
        item_preco_atual = df_new_ativo.iloc[-1]['PRECO_ATUAL']
        item_percent_valoriz_atual = df_new_ativo.iloc[-1]['VALRZ_ATUAL']
        item_total_invest = item_preco_medio * item_quantidade
        item_total_atual = item_preco_atual * item_quantidade
        item_total_lucro = item_total_atual - item_total_invest
        item_percent_lucro = (item_total_lucro / item_total_invest)

        geral_total_invest += item_total_invest
        geral_total_atual += item_total_atual

        item_quantidade = decimal_to_str(valor=item_quantidade, formato="{0:,.10f}")
        item_preco_medio = decimal_to_str(valor=item_preco_medio, formato="{0:,.6f}")
        item_preco_atual = decimal_to_str(valor=item_preco_atual)
        item_percent_valoriz_atual = decimal_to_str(valor=item_percent_valoriz_atual)
        item_total_invest = decimal_to_str(valor=item_total_invest)
        item_total_atual = decimal_to_str(valor=item_total_atual)
        item_total_lucro = decimal_to_str(valor=item_total_lucro)
        item_percent_lucro = decimal_to_str(valor=item_percent_lucro, formato="{0:,.2%}")

        if not somenteSaldo:
            msg += f'<b>{moeda}</b><br>'
            msg += f'Qtd: {item_quantidade}<br>'
            msg += f'P.Médio: R$ {item_preco_medio}<br>'
            msg += f'P.Atual: R$ {item_preco_atual}<b> ({item_percent_valoriz_atual}%)</b><br>'
            msg += f'T.Invest: R$ {item_total_invest}<br>'
            msg += f'T.Atual: R$ {item_total_atual}<br>'
            msg += f'<b>Valrz: R$ {item_total_lucro} ({item_percent_lucro})</b><br>'
            msg += f'<br>'
            print(f'{moeda:15}\t Qtd: {str(item_quantidade):30} \t Preço Médio: R$ {str(item_preco_medio):25} \t Preço Atual: R$ {str(item_preco_atual):20} ({item_percent_valoriz_atual:6}%) \t Total Invest.: R$ {str(item_total_invest):20} \t Total Atual: R$ {str(item_total_atual):20} \t Lucro: R$ {str(item_total_lucro):20} ({item_percent_lucro:6})')

    geral_total_lucro = geral_total_atual - geral_total_invest
    geral_percent_lucro = (geral_total_lucro / geral_total_invest)

    geral_total_invest = decimal_to_str(valor=geral_total_invest)
    geral_total_atual = decimal_to_str(valor=geral_total_atual)
    geral_total_lucro = decimal_to_str(valor=geral_total_lucro)
    geral_percent_lucro = decimal_to_str(valor=geral_percent_lucro, formato="{0:,.2%}")

    msg += f'<b>TOTAL</b><br>'
    msg += f'T.Invest: R$ {geral_total_invest}<br>'
    msg += f'T.Atual: R$ {geral_total_atual}<br>'
    msg += f'<b>Valrz: R$ {geral_total_lucro} ({geral_percent_lucro})</b><br>'
    msg += f'<br>'

    print(f'')
    print(f'TOTAL\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t Total Invest.: R$ {geral_total_invest:20} \t Total Atual: R$ {str(geral_total_atual):20} \t Lucro: R$ {str(geral_total_lucro):20} ({geral_percent_lucro:6})')

    msg += f'<i><u>{dt.datetime.now(tz=timezone).strftime("%d/%m/%Y %H:%M:%S")}</u></i><br>'

    return msg

def processar():
    try:

        bot = telebot.TeleBot(token=telegram_token)
        try:

            def get_user_name(message):
                try:
                    if (message.from_user.first_name != ''):
                        return message.from_user.first_name + (f" {message.from_user.last_name}" if (message.from_user.last_name != '') else "")
                    elif (message.from_user.username != ''):
                        return message.from_user.username
                    return ""
                except Exception as e:
                    return ""

            def get_msg_padrao(message):
                try:

                    username = get_user_name(message)

                    text = ""
                    text += "Olá!" if (username == '') else f"Olá, {username}!"
                    text += f"\nEu sou o ChatBot do <b>TamoNaBolsaFatos</b>."
                    text += f"\n\nSalve o seu ID: <b>{str(message.chat.id)}</b>, ele será muito importante.\n\n"
                    text += "<b>O que você gostaria de saber?</b>\n\n"
                    text += "/saldo - Saldo\n"
                    text += "/portfolio - Portfólio\n"
                    text += "\n\n"

                    return text

                except Exception as e:
                    return ""

            @bot.message_handler(commands=['start'])
            def send_welcome(message):
                try:

                    text = get_msg_padrao(message=message)
                    msg = bot.send_message(chat_id=message.chat.id, text=text, parse_mode="HTML", disable_web_page_preview=False)

                except Exception as e:
                    bot.send_message(chat_id=message.chat.id, text='Ops!\nOcorreu um erro inesperado.\nPor favor, tente novamente mais tarde.')
                    print(f'Falha Geral - send_welcome: {str(e)}')

            @bot.message_handler(commands=['help', 'Help', 'ajuda', 'Ajuda'])
            def send_help(message):
                try:

                    text = get_msg_padrao(message=message)
                    msg = bot.send_message(chat_id=message.chat.id, text=text, parse_mode="HTML")

                except Exception as e:
                    bot.send_message(chat_id=message.chat.id, text='Ops!\nOcorreu um erro inesperado.\nPor favor, tente novamente mais tarde.')
                    print(f'Falha Geral - send_help: {str(e)}')

            @bot.message_handler(commands=['portfolio'])
            def send_portfolio(message):
                try:
                    
                    if str(telegram_chat_id) != str(message.chat.id):
                        msg = bot.send_message(chat_id=message.chat.id, text='Não autorizado!', parse_mode="HTML", disable_web_page_preview=False)
                        return

                    msg = bot.send_message(chat_id=message.chat.id, text='Consultando Dados\nAguarde...', parse_mode="HTML", disable_web_page_preview=False)

                    html = buscar_trades()
                    df = montar_trades(html=html)
                    chat_text = gerar_msg_alerta_cripto(df=df)
                    chat_text = chat_text.replace('<br>', '\n')

                    msg = bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=chat_text, parse_mode="HTML", disable_web_page_preview=False)
                    # msg = bot.send_message(chat_id=message.chat.id, text=chat_text, parse_mode="HTML", disable_web_page_preview=False)

                except Exception as e:
                    bot.send_message(chat_id=message.chat.id, text='Ops!\nOcorreu um erro inesperado.\nPor favor, tente novamente mais tarde.')
                    print(f'Falha Geral - send_portfolio: {str(e)}')

            @bot.message_handler(commands=['saldo'])
            def send_saldo(message):
                try:
                    
                    if str(telegram_chat_id) != str(message.chat.id):
                        msg = bot.send_message(chat_id=message.chat.id, text='Não autorizado!', parse_mode="HTML", disable_web_page_preview=False)
                        return

                    msg = bot.send_message(chat_id=message.chat.id, text='Consultando Dados\nAguarde...', parse_mode="HTML", disable_web_page_preview=False)

                    html = buscar_trades()
                    df = montar_trades(html=html)
                    chat_text = gerar_msg_alerta_cripto(df=df, somenteSaldo=True)
                    chat_text = chat_text.replace('<br>', '\n')

                    msg = bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=chat_text, parse_mode="HTML", disable_web_page_preview=False)
                    # msg = bot.send_message(chat_id=message.chat.id, text=chat_text, parse_mode="HTML", disable_web_page_preview=False)

                except Exception as e:
                    bot.send_message(chat_id=message.chat.id, text='Ops!\nOcorreu um erro inesperado.\nPor favor, tente novamente mais tarde.')
                    print(f'Falha Geral - send_saldo: {str(e)}')

            @bot.message_handler(func=lambda m: True)
            def send_all(message):
                try:

                    text = get_msg_padrao(message=message)
                    msg = bot.send_message(chat_id=message.chat.id, text=text)

                except Exception as e:
                    bot.send_message(chat_id=message.chat.id, text='Ops!\nOcorreu um erro inesperado.\nPor favor, tente novamente mais tarde.')
                    print(f'Falha Geral - send_all: {str(e)}')

            try:
                bot.enable_save_next_step_handlers(delay=120)
            except Exception as e:
                pass

            try:
                bot.load_next_step_handlers()
            except Exception as e:
                pass

            while True:
                try:
                    bot.polling(none_stop=True, interval=0, timeout=60)
                except Exception as e:
                    print(f'Falha Geral - polling: {str(e)}')
                    time.sleep(10)
                finally:
                    bot.stop_polling()

        except:
            pass
        finally:
            bot.stop_bot()

    except Exception as e:
        print(f'Falha Geral - processar: {str(e)}')


processar()

# pip freeze > requirements.txt
# pip install -r requirements.txt

# heroku ps:scale worker=1 --app=cms-cripto-bot-worker
# heroku ps:scale worker=0 --app=cms-cripto-bot-worker

# pip install --upgrade pip
# pip install --upgrade setuptools
# pip install pytz
# pip install pandas --upgrade --no-cache-dir
# pip install numpy --upgrade --no-cache-dir
# pip install pyTelegramBotAPI --upgrade --no-cache-dir
# pip install cryptocompare --upgrade --no-cache-dir
