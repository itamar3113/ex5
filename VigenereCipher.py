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


if __name__ == "__main__":
    cipher = VigenereCipher([1, 2, 3])
    print("abcdefgz  l?!")
    s = cipher.encrypt("abcdefgz  l?!")
    print(s)
    print(cipher.decrypt(s))