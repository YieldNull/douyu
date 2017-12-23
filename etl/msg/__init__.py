def parse_raw(parser, line):
    first_space = line.find(' ')
    second_space = line.find(' ', first_space + 1)

    rid = line[:first_space]
    timestamp = line[first_space + 1:second_space]
    msg = line[second_space + 1:len(line) - 1]

    try:
        doc = parser.parse(msg)
    except AttributeError as e:
        return None

    doc.update({'roomID': rid, 'time': timestamp})

    return doc
