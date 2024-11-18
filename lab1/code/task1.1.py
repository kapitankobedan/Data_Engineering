# Варианты 4, 14, 24, …
# Подсчитайте количество, а также долю всех слов, длина которых превышает 4 символа (>4).


def read_file():
    with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab1\data\first_task.txt", encoding="utf-8") as file:
        return file.readlines()


def text_to_words(lines):
    words = []

    for line in lines:
        _line = (line
                 .replace("'", "")
                 .replace("?", "")
                 .replace("!", "")
                 .replace(".", "")
                 .replace(",", "")
                 .replace("-", " ")
                 .lower().strip())
        words += _line.split(" ")

    return words

def find_words(words):
    four_words = 0
    total_words = 0
    for word in words:
        total_words += 1
        if len(word) > 4:
            four_words += 1
    fraction_four_words = round(((four_words / total_words) * 100), 2)
    result = (f"Слова с длиной более 4 символов: {four_words}\n"
              f"Доля таких слов: {fraction_four_words}%")
    with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab1\result\result1.1.2.txt", "w", encoding="utf-8") as file:
        file.write(result)


def calc_freq(words):
    word_freq = {}
    for word in words:
        if len(word) == 0:
            continue
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    return sorted(word_freq.items(), key=lambda x: x[1], reverse=True)


def write_to_first_file(stat):
    with open(r"C:\Users\Данила\PycharmProjects\DE_labs\lab1\result\result1.1.1.txt", "w", encoding="utf-8") as file:
        for key, val in stat:
            file.write(f"{key}:{val}\n")
print('Отсортированный список всех слов записан в файл result1.1.1.txt')

print('Статистика по словам, превышающим 4 символа, записана в файл result1.1.2.txt')

lines = read_file()
words = text_to_words(lines)
word_freq = calc_freq(words)
write_to_first_file(word_freq)
find_words(words)
