from CaesarCipher import CaesarCipher


class VigenereCipher(CaesarCipher):
    def __init__(self, shifters):
        super().__init__(shifters[0])
        self.shifters = shifters

    def encrypt(self, plaintext: str) -> str:
        encrypted = ""
        for i in range(len(plaintext)):
            super().setShifter(self.shifters[i % len(self.shifters)])
            encrypted += super().encrypt(plaintext[i])
        return encrypted

    def decrypt(self, ciphertext: str) -> str:
        reversedShifters = []
        for i in self.shifters:
            reversedShifters.append(-i)
        decryptor = VigenereCipher(reversedShifters)
        return decryptor.encrypt(ciphertext)


def getVigenereFromStr(keyString: str) -> VigenereCipher:
    keys = []
    for i in keyString:
        if i.isalpha():
            if i.islower:
                keys.append(ord(i)-ord('a'))
            else:
                 keys.append(ord(i)-ord('A'))
    return VigenereCipher(keys)


if __name__ == "__main__":
    keys = "b?1c d"
    cipher = getVigenereFromStr(keys)
    print("abcdefgz  l?!")
    s = cipher.encrypt("abcdefgz  l?!")
    print(s)
    print(cipher.decrypt(s))
