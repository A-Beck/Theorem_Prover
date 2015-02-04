from parser import Parser

def main():

    parser = Parser()

    while True:
        user_input = raw_input("SkynetBot> ")
        parser.parse(user_input)

if __name__ == '__main__':
    main()
