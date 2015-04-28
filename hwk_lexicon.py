# Define the lexicon here
LEXI_DICT = {
    "id": ["homework", "hwk", "assignment", "assign",
           "exam", "midterm", "test", "problems", "section", "textbook"],

    "week": ["monday", "mon", "tuesday", "tues", "wednesday",
             "wed", "thurs", "thursday", "friday", "fri", "saturday",
             "sat", "sunday", "sun"],

    "day_modifier": ["tomorrow", "next", "soon"],

    "stop": ["is", "has", "have", "that"],

    "key": ["due", "do", "optional", "mandatory"]

}
# additional descriptors:
# "desc"
# represents the fact that the sentence has
# additional descriptions. Like the homework assignement name


def parse_multi(multi_sentence):
    sentence_list = multi_sentence.split(".")
    return sentence_list
    # for sentence in sentence_list:
    #     yield parse(sentence)


def parse(sentence):
    sentence_list = sentence.lower().split()
    return process(sentence_list, search(sentence_list))


def search(sentence_list):
    associate_word = []
    for word in sentence_list:
        potent_id = compare_with_dict(word)

        try:
            prev = associate_word[-1]
            associate_word.append(process_prev(prev, potent_id))
            if word is 'do':
                associate_word.pop()
                associate_word.append(None)
            if potent_id is 'stop':
                a = check_for_id(associate_word)
                if not type(a) == int:
                    index = associate_word.index('stop')
                    associate_word = change_up_to(associate_word, index)
        except IndexError:
            associate_word.append(potent_id)

    return associate_word


def process_prev(prev, potent_id):
    if potent_id is None and (prev is 'desc' or prev is 'id'):
        return 'desc'

    if potent_id is 'id' and prev is 'id':
        return 'desc'

    return potent_id


def compare_with_dict(word):
    for _id, _words in LEXI_DICT.items():
        if _words.count(word) > 0:
            return _id

    return None


def peek(word, sentence_list):
    a = sentence_list.index(word)
    return sentence_list[a+1]


def process(sentence_list, search_list):
    ids = []
    modifiers = []
    weeks = []
    key = []
    desc = []
    for num in range(0, len(search_list)):
        if search_list[num] is 'id':
            ids.append(sentence_list[num])
        elif search_list[num] is 'day_modifier':
            modifiers.append(sentence_list[num])
        elif search_list[num] is 'week':
            weeks.append(sentence_list[num])
        elif search_list[num] is 'key':
            key.append(sentence_list[num])
        elif search_list[num] is 'desc':
            desc.append(sentence_list[num])

    return (ids, modifiers, weeks, key, desc)


def check_for_id(id_list):
    try:
        return id_list.index('id')
    except ValueError:
        return False


def change_up_to(id_list, index):
    temp_list = id_list
    for i in range(0, index+1):
        if id_list[i] is None:
            temp_list[i] = 'desc'
        else:
            temp_list[i] = id_list[i]

    temp_list[temp_list.index('desc')] = 'id'

    return temp_list
