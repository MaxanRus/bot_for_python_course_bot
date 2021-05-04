import json

import telebot
import requests

headers_query = {
    'Host': 'castlots.org',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://castlots.org/shar-predskazanij/',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Length': '0',
    'Origin': 'https://castlots.org',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}

bot = telebot.TeleBot('1751838573:AAFA46T5oPxIp9OC74pMCQ_x6zHuHYeK5pA')


@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.from_user.id, "Привет, я бот - магический шар, можешь задвать мне любые вопросы.\nТак же у "
                                       "меня есть много команд, которые вы можете увидеть если напишете /")


@bot.message_handler(commands=['get_password'])
def create_password(msg):
    def get_len(msg):
        def get_passwords(length):
            href = "https://castlots.org/generator-parolej-online/parol.php"
            params = {"val": str(length), "sma": "yes", "big": "yes", "spe": "no", "easy": ""}
            response = requests.post(href, data=params, headers=headers_query)
            return json.loads(response.text)['arr_parol']

        try:
            if int(msg.text) < 1:
                raise ValueError
            bot.send_message(msg.from_user.id, '\n'.join(get_passwords(int(msg.text))))
        except ValueError:
            bot.send_message(msg.from_user.id, "Не понял тебя, ты идиот и не смог написать число?")

    bot.send_message(msg.from_user.id, "Введите желаемую длину")
    bot.register_next_step_handler(msg, get_len)


@bot.message_handler(commands=['get_random_number'])
def create_random_number(msg):
    def get_max(msg):
        def get_random_number(max_number):
            href = "https://castlots.org/generator-sluchajnyh-chisel/generate.php"
            params = {"val": "1", "ot": "1", "do": str(max_number), "iskl": "no", "ent": "yes"}
            response = requests.post(href, data=params, headers=headers_query)
            return json.loads(response.text)['a'][0]

        try:
            bot.send_message(msg.from_user.id, get_random_number(int(msg.text)))
        except ValueError:
            bot.send_message(msg.from_user.id, "Не понял тебя, ты идиот и не смог написать число?")

    bot.send_message(msg.from_user.id, "Вы хотите число от 1 до скольки?")
    bot.register_next_step_handler(msg, get_max)


@bot.message_handler(commands=['get_rhyme'])
def create_random_number(msg):
    def get_word(msg):
        def get_rhyme(word):
            href = "https://castlots.org/podbor-rifmi-k-slovu/generate.php"
            params = {"word": word}
            response = requests.post(href, data=params, headers=headers_query)
            return json.loads(response.text)['va']

        try:
            rhymes = str(get_rhyme(str(msg.text)))
            if len(rhymes) > 4:
                bot.send_message(msg.from_user.id, rhymes)
            else:
                bot.send_message(msg.from_user.id, "Рифм не нашлось")
        except ValueError:
            bot.send_message(msg.from_user.id, "Хз как ты смог меня сломать")

    bot.send_message(msg.from_user.id, "Введите слово на русском")
    bot.register_next_step_handler(msg, get_word)


@bot.message_handler(commands=['get_position'])
def create_random_position(msg):
    num = int(json.loads(requests.post("https://castlots.org/generator-poz-dlja-seksa/generate.php", data={},
                                       headers=headers_query).text)['va'])
    data = requests.get("https://castlots.org/img/kamasutra/" + str(num) + ".jpg")
    bot.send_photo(msg.from_user.id, data.content)


@bot.message_handler(commands=['get_quote'])
def get_quote(msg):
    data = requests.post("https://castlots.org/generator-citat-online/generate.php", headers=headers_query)
    bot.send_message(msg.from_user.id, json.loads(data.text)['va'])


@bot.message_handler(commands=['get_fact'])
def get_fact(msg):
    params = {"hid": "yes"}
    data = requests.post("https://castlots.org/generator-interesnykh-faktov/generate.php", data=params,
                         headers=headers_query)
    bot.send_message(msg.from_user.id, json.loads(data.text)['va'])


@bot.message_handler(commands=['get_anecdote'])
def get_anecdote(msg):
    data = requests.post("https://castlots.org/generator-anekdotov-online/generate.php", headers=headers_query)
    bot.send_message(msg.from_user.id, json.loads(data.text.replace("<br \\/>", " "))['va'])


@bot.message_handler(commands=['get_card'])
def create_random_position(msg):
    params = {"val": "1", "t": "yes", "p": "yes", "c": "yes", "b": "yes", "number": "52", "hid": "yes"}
    card = json.loads(requests.post("https://castlots.org/generator-igralnyh-kart/karti.php", data=params,
                                    headers=headers_query).text)['res'][0]
    data = requests.get("	https://castlots.org/img/cards/" + str(card) + ".jpg")
    bot.send_photo(msg.from_user.id, data.content)


@bot.message_handler(commands=['get_compliment_woman'])
def get_compliment_woman(msg):
    data = requests.post("https://castlots.org/generator-komplimentov-devushke/generate.php", headers=headers_query)
    bot.send_message(msg.from_user.id, json.loads(data.text.replace("<br \\/>", " "))['va'])


@bot.message_handler(commands=['get_compliment_man'])
def get_compliment_man(msg):
    data = requests.post("https://castlots.org/generator-komplimentov-muzhchine/generate.php", headers=headers_query)
    bot.send_message(msg.from_user.id, json.loads(data.text.replace("<br \\/>", " "))['va'])


@bot.message_handler(content_types=['text'])
def message(msg):
    params = {"que": msg.text}
    response = requests.post('https://castlots.org/shar-predskazanij/generate.php', data=params, headers=headers_query)
    json_response = json.loads(response.text.replace("<br \\/>", " ").encode().decode('unicode_escape'))
    bot.reply_to(msg, json_response["va"])


bot.polling(none_stop=True, interval=0)
