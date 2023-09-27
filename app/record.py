from googletrans import Translator

def sentence_compare(list1, list2):
    # find the different words in both lists
    different_words = []
    for i in range(min(len(list1), len(list2))):
        if list1[i] != list2[i]:
            different_words.append(list1[i])

    # add remaining words from longer list, if any
    if len(list1) > len(list2):
        different_words.extend(list1[len(list2):])
    else:
        different_words.extend(list2[len(list1):])

    return different_words

def translate_marathi(different_words):
    # create a Translator object
    translator = Translator(service_urls=['translate.google.com'])

    # define a list of English words
    english_words = different_words

    # create an empty list for the translated words
    marathi_words = {}

    # translate each word in the list and append to the marathi_words list
    for word in english_words:
        translation = translator.translate(word, dest='mr')
        marathi_words.update({word : translation.text})
    return marathi_words