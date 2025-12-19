import re

def sanitize_collection_name(corpus_name):

    name = corpus_name.strip()
    name = re.sub(r'[^a-zA-Z0-9._-]', '_', corpus_name)
    name = name.lower()
    name = name.strip('_')
    return name

if __name__ == "__main__":
    name = 'The Creation of (Adam)'
    d = sanitize_collection_name(name)
    print(d)