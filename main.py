
import requests
import json

alphabet = ['a',
            'b'
            , 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z'
            ]

alphabetPages = [50, 47, 68, 37, 28, 30, 28, 33, 26, 9, 12, 29, 44, 21, 20, 60, 5, 30, 77, 40, 14, 13, 20, 2, 4, 4]
index = 0
for abc in alphabet:
    index = index
    for alphabetPageIndex in range(alphabetPages[index]):
        r = requests.get('https://www.dictionary.com/list/' + abc + '/' + str(alphabetPageIndex + 1))
        # print(json.loads(r.text))

        b = '<script>'

        a = r.text.find(b)
        a = r.text.find(b, a + 1)
        a = r.text.find(b, a + 1)

        # a = r.text.count(b)
        newText = r.text[a:]
        countOfWords = r.text.count("displayForm")
        a = 0

        # countOfWords
        for i in range(countOfWords):
            a = newText.find('{"displayForm"', a + 1)
            b = newText.find('}', a)
            word = json.loads(newText[a:b + 1])

            # get type
            r2 = requests.get('https://www.dictionary.com/browse/' + word["url"])
            definitionString = '''<div class="css-69s207 e1hk9ate3"><span class="css-1b1gas3 e1hk9ate2"><span class="luna-pos">''';
            foundDefinitionString = r2.text.find(definitionString)
            if foundDefinitionString == -1:
                definitionString = '''<div class="css-69s207 e1hk9ate3"><span class="css-1b1gas3 e1hk9ate2"><span class="pos">''';
                foundDefinitionString = r2.text.find(definitionString)

            aa = foundDefinitionString + len(definitionString)
            bb = r2.text.find("<", aa)
            res = r2.text[aa:bb]
            c_type = ""
            if "article" in res:
                c_type = "DET"
            else:
                if res.find(" ") > -1:
                    res = res[:res.find(" ")]
                if res.find(",") > -1:
                    res = res[:res.find(",")]
                match res:
                    case "adjective":
                        c_type = "ADJ"
                    case "adj.":
                        c_type = "ADJ"
                    case "adverb":
                        c_type = "ADV"
                    case "conjunction":
                        c_type = "CNJ"
                    case "auxiliary verb":
                        c_type = "MOD"
                    case "noun":
                        c_type = "N"
                    case "abbreviation":
                        c_type = "N"
                    case "abbr.":
                        c_type = "N"
                    case "n.":
                        c_type = "N"
                    case "pronoun":
                        c_type = "PRO"
                    case "preposition":
                        c_type = "P"
                    case "interjection":
                        c_type = "UH"
                    case "verb":
                        c_type = "V"
                    case _:
                        c_type = "NOPE"

            # print(res)
            # with open("l.text", "w") as f:
            #     f.write(r2.content.encode("utf-8"))
            bPrint = True
            if " " in word["displayForm"]:
                bPrint = False
            if "NOPE" in c_type:
                bPrint = False

            if bPrint:
                print(word["displayForm"] + ":" + c_type)
                # print(',{word:"' + word["displayForm"] + '", type:"' + c_type + '"}')
