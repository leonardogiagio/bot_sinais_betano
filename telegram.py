# importar biblioteca para requisições http
import requests

# mostra o id do último grupo adicionado
def last_chat_id(token):
    try:
        url = "https://api.telegram.org/bot{}/getUpdates".format(token)
        response = requests.get(url)
        if response.status_code == 200:
            json_msg = response.json()
            for json_result in reversed(json_msg['result']):
                # print(json_result)
                message_keys = list(json_result.keys())
                if ('message_id' == message_keys[1]) or ('group_chat_created' == message_keys[1]) or ('message' == message_keys[1]):
                    # print(json_result[message_keys[1]])
                    return json_result[message_keys[1]]
                elif('channel_post' == message_keys[1]):
                    # print(json_result['channel_post']['chat']['id'])
                    return json_result['channel_post']['chat']['id']
            # print('Nenhum grupo encontrado')
        else:
            print('A resposta falhou, código de status: {}'.format(response.status_code))
    except Exception as e:
        print("Erro no getUpdates:", e)

# enviar mensagens utilizando o bot para um chat específico
def send_message(token, chat_id, message):
    try:
        data = {"chat_id": chat_id, "text": message}
        url = "https://api.telegram.org/bot{}/sendMessage".format(token)
        requests.post(url, data)
    except Exception as e:
        print("Erro no sendMessage:", e)

# token = '6711575896:AAEO1bNBZ6boE6zKrJcGP7wNhnlPvODagZM'
# chat_id = last_chat_id(token)
# send_message(token, -1002011158039, 'teste')
