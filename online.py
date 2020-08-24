from search_functoins import find_sentences


def normal_form(query):
    without_unnecessary_spaces = ' '.join([x for x in query.split(' ') if x != ''])
    only_letter_or_number = ''.join(e for e in without_unnecessary_spaces if e.isalnum() or e == ' ').lower()
    return only_letter_or_number


def main():
    query = input("Begin search - enter your text:\n")
    while True:
        if '#' in query:
            query = input("New search - enter your text:\n")
        else:
            normal_query = normal_form(query)
            if len(normal_query) != 0:
                find_sentences(normal_query)
            query += input(query)


main()
