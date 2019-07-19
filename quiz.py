from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABdMUmDKU5-UPGK0VcKnsSl6nFBrCBYHaj94IbW2YZuo2BwveVuTkLkyrYicb-JiIDIk2H24R_Ukmyg2aD1GgxSydpcJF5YyO8a6uZsZB1o6622HI0ZfNUQwf-Yoo_zWXMiseYMeGBoSgaAg9yvuBtjWfmyCGov3RXzfZmHCFNIdXKwCNo='


def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
