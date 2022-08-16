import requests
from bs4 import BeautifulSoup

# форматирование текста для избежания проблем вывода
def edited(text):
    return text.replace("_", "\_") \
        .replace("*", "\*") \
        .replace("[", "\[") \
        .replace("]", "\]") \
        .replace("(", "\(") \
        .replace(")", "\)") \
        .replace("~", "\~") \
        .replace("`", "\`") \
        .replace(">", "\>") \
        .replace("#", "\#") \
        .replace("+", "\+") \
        .replace("-", "\-") \
        .replace("=", "\=") \
        .replace("|", "\|") \
        .replace("{", "\{") \
        .replace("}", "\}") \
        .replace(".", "\.") \
        .replace("!", "\!")


# проверка если текст состоит из букв, пробелов и цифр
def is_valid(text):
    if all(x.isspace() or x.isalnum() for x in text):
        return True
    return False


# конвертация валют.
def convert(amount: float, input_currency: str, output_currency: str):
    # динамическое заполнение URL
    url = f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={input_currency}&To={output_currency}"

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    # получение конвертированной валюты по актуальному курсу
    converted_amount = soup.find("p", class_="result__BigRate-sc-1bsijpp-1 iGrAod").text.split(".")

    # корректное отображение
    converted_amount = converted_amount[0] + "." + converted_amount[1][:2]

    return converted_amount

