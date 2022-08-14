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
