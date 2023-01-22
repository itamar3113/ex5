import CaesarCipher


class VigenereCipher(CaesarCipher):
    def __init__(self, shifters):
        self.shifters = shifters
        CaesarCipher.__init__(self, shifters[0])

    def encrypt(self, plaintext: str)->str:
        encrypted = ""
        for i in plaintext:
            self.setShifter(self.shifters[i % len(self.shifters)])
            encrypted += self.encryptor.encrypt(i)
        return encrypted


if __name__ == "__main__":
    cipher = VigenereCipher([1,2,3])
    print(cipher.encrypt("abcdefg"))
