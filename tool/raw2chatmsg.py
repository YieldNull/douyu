import sys
import os
from danmu.msg import RegexParser

if __name__ == '__main__':
    parent = sys.argv[1]
    output = sys.argv[2]

    parser = RegexParser()

    fout = open(output, 'w', encoding='utf-8', buffering=1024 * 1024 * 10)
    fout.write('roomID\tbroomID\tts\tusername\tcontent\tuserlevel\tbadgename\tbadgelv\n')

    amount = 0
    error = 0

    for path in os.listdir(parent):
        if path.endswith('.txt'):
            with open(os.path.join(parent, path), 'r', encoding='utf-8', buffering=1024 * 1024 * 10) as f:
                for line in f:
                    amount += 1

                    first_space = line.find(' ')
                    second_space = line.find(' ', first_space + 1)

                    rid = line[:first_space]
                    timestamp = line[first_space + 1:second_space]
                    msg = line[second_space + 1:len(line) - 1]

                    try:
                        doc = parser.parse(msg)
                    except Exception as e:
                        error += 1
                        continue

                    doc.update({'roomID': rid, 'ts': timestamp})

                    if doc['type'] == 'chatmsg':
                        fout.write(
                            '{roomID}\t{broomID}\t{ts}\t{username}\t{content}\t{userlevel}\t{badgename}\t{badgelv}\n'
                                .format(**doc))

    fout.close()

    print('Amount:%d. Error:%d. Fraction:%f%%.' % (amount, error, error * 100 / amount))
