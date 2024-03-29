NUM_OF_LETTERS = 26

class CaesarCipher:
    def __init__(self, shifter):
        self.shifter = shifter

    def encrypt(self, plaintext: str) -> str:
        encrypted = ""
        for i in plaintext:
            if i.isalpha():
                if i.islower():
                    encrypted += chr((ord(i) - ord('a') +
                                     self.shifter) % NUM_OF_LETTERS + ord('a'))
                else:
                    encrypted += chr((ord(i) - ord('A') +
                                     self.shifter) % NUM_OF_LETTERS + ord('A'))
            else:
                encrypted += i
        return encrypted

    def decrypt(self, ciphertext: str) -> str:
        decryptor = CaesarCipher(-self.shifter)
        return decryptor.encrypt(ciphertext)

    # todo check if ligall
    def setShifter(self, shifter):
        self.shifter = shifter
