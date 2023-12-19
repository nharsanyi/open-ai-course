import tiktoken

if __name__ == '__main__':
    enc = tiktoken.get_encoding("p50k_base")

    print(len(enc.encode("TikToken Tokenizer Example")))