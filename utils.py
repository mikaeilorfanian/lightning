import codecs


def read_file_content(filename):
    f = codecs.open(filename, mode='r', encoding='utf-8')
    content = f.read()
    f.close()
    return content
