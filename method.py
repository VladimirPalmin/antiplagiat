import re
from collections import Counter
from random import sample
import functools
import PySimpleGUI as sg


def takes(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            if type(e).__name__ == "FileNotFoundError":
                # img = Image.open(r'C:\Users\Anaconda\PycharmProjects\antiplagiat\XVe67dkAi_I.jpg')
                # img.show()
                # print("Был бы ты человеком")
                print("Oops, I can't find your file")
            else:
                print(type(e).__name__)

    return wrapper


def get_text(link):
    """
    This function writes file.text (only .text) into list without any punctuation marks

    type link: str
    param link: the link to your text file
    """
    if link[-3:] == 'txt':
        text_file = open(link, 'r')
        text = text_file.read()
        text = text.lower()  #
        text = re.split(r'\W+', text)  # split the string into words and remove punctuation marks
        text.pop()  # delete last empty item
        text_file.close()
        return text
    else:
        print("I can't read it. Please, use txt format")


def delete_noise(text):
    """
    This function deletes all noises like articles, prepositions and conjunctions, removes ends 's', 'es' and 'ies'
    and converts different forms of be to be
    """
    noises = ['a', 'an', 'the', 'this', 'that',
              'in', 'on', 'at', 'by', 'from',
              'to', 'and', 'but', 'for', 'of', 'or', 'as']
    clear_text = [word for word in text if word not in noises]

    for i in range(len(clear_text)):
        if clear_text[i] in ['is', 'am', 'are', 'was', 'were', 'been']:  # convert different forms of be to be
            clear_text[i] = 'be'
        if len(clear_text[i]) > 2:
            if clear_text[i][-1] == 's':
                if clear_text[i][-2] == 'e':
                    if clear_text[i][-3] == 'i':
                        clear_text[i] = clear_text[i][0:-3] + 'y'  # convert ies to y
                    elif clear_text[i][-3] == 'y':  # don't change yes
                        pass
                    else:
                        clear_text[i] = clear_text[i][0:-2]  # delete 'es'
                else:
                    clear_text[i] = clear_text[i][0:-1]  # delete 's'

    return clear_text


def check_for_cheating(text):
    """
    This function checks russian symbols 'а' and 'с' in the text
    """
    for word in text:
        if (re.search('с', word)) or (re.search('а', word)):
            print("Bad guy, don't use russian symbols")
            break


def get_hashed_shingle(text, shingle_lenh=4):
    """
    This function divides the text into shingles and calculate check sums with CRC32

    param shingle_lenh: shingle length from 3 to 10, the shorter the length, the more accurate the test result
    """
    import binascii
    shingles_check_sum = []  # list of shingles
    for i in range(len(text) - shingle_lenh + 1):
        shingle = text[i: i + shingle_lenh]
        string_shingle = ' '.join(shingle)
        shingles_check_sum.append(binascii.crc32(string_shingle.encode('utf-8')))
    return shingles_check_sum


def get_random_words(text, percent=0.1, rnd_percent=0.7, number_of_rnd_lists=36):
    """
    This function creates a dictionary,sorts words in it in frequency, deletes most and least common words
    and returns array of random words from the dictionary

    percent is a percent of deleted words
    rnd_percent is a percent of original words in new array
    number_of_rnd_lists is a number of arrays of random words
    """
    dictionary = dict(Counter(text))
    barrier = int(len(text) * percent)
    dictionary_sorted = sorted(dictionary, key=lambda x: dictionary[x])
    words = dictionary_sorted[barrier:-barrier]
    rnd_number = int(len(words) * rnd_percent)
    random_words = []
    for i in range(number_of_rnd_lists):
        random_words.append(sample(words, rnd_number))
    return random_words


# @takes
def compare(links):
    """
    This function compares text files and shows parameters of similarity
    """
    shingles = []
    for link in links:
        text = delete_noise(get_text(link))
        check_for_cheating(text)
        shingles_from_text = get_hashed_shingle(text)
        shingles.append(shingles_from_text)
    print('wait a little more...')
    results = []
    number = 1
    for shingles_from_chosen_text in shingles:
        results_for_chosen_text = []
        for i in range(number, len(shingles)):
            count = 0
            shingles_from_another_text = shingles[i]
            for j in range(len(shingles_from_chosen_text)):
                if shingles_from_chosen_text[j] in shingles_from_another_text:
                    count += 1
            result = 2 * count / (len(shingles_from_chosen_text) + len(shingles_from_another_text)) * 100
            results_for_chosen_text.append(result)
        number += 1
        results.append(results_for_chosen_text)
    number_shift = 0
    for i in range(len(shingles)):
        for j in range(len(results[i])):
            print("Percentage of similarity between text " + str(i + 1) +
                  " and text " + str(j + 2 + number_shift), round(results[i][j], 2))
        number_shift += 1


def dialog():
    print("How many files do you want to compare?")
    n = int(input())
    print("Write links to your files with enter")
    links = []
    for i in range(n):
        links.append(input())
    compare(links)


dialog()

# C:\Users\Anaconda\PycharmProjects\small_test.txt
