from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
# Break it into multiple lines to fit the standards
message = b'gAAAAABc-TXUyheBme9ilvLbUsFnUZrSe7oucsmuGuEVqJ0fGLJ1aNrrx2wV-' \
          b'DLOSYksmf54qhs926SSbi4ui4xnVhZbTb65JteEpldDXKgoUnTKyFs_' \
          b'C28aIsZtNh7aOvA886GgEMqU7tPptN20VvkmKYsdjqq5Qlk7ELMdhu-oNeyZv6IRkTY='


def main():
    f = Fernet(key)
    print(f.decrypt(message).decode("utf-8"))


if __name__ == "__main__":
    main()
