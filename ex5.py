import json
import os

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


class VigenereCipher(CaesarCipher):
    def __init__(self, shifters):
        super().__init__(shifters[0])
        self.shifters = shifters

    def encrypt(self, plaintext: str) -> str:
        encrypted = ""
        j = 0
        for i in range(len(plaintext)):
            super().setShifter(self.shifters[j % len(self.shifters)])
            encrypted += super().encrypt(plaintext[i])
            if plaintext[i].isalpha():
                j += 1
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
                keys.append(ord(i) - ord('a'))
            else:
                keys.append(ord(i) - ord('A'))
    return VigenereCipher(keys)


def processDirectory(dir_path: str):
    with open(os.path.join(dir_path, "config.json"), 'r') as f:
        instructions_dict = json.load(f)
        for input_file in os.listdir(dir_path):
            name, extension = os.path.splitext(input_file)
            if instructions_dict['mode'] == "decrypt":
                if extension == ".enc":
                    with open(os.path.join(dir_path, input_file), 'r') as encrypted_file:
                        encrypted_content = encrypted_file.read()
                        if instructions_dict['type'] == "Caesar":
                            caesar_input = CaesarCipher(instructions_dict['key'])
                            decrypted_content = caesar_input.decrypt(encrypted_content)
                        if instructions_dict['type'] == "Vigenere":
                            if type(instructions_dict['key']) is str:
                                vigenere_input = getVigenereFromStr(instructions_dict['key'])
                            else:
                                vigenere_input = VigenereCipher(instructions_dict['key'])
                            decrypted_content = vigenere_input.decrypt(encrypted_content)
                        new_filename = name + ".txt"
                        with open(os.path.join(dir_path, new_filename), 'w') as decrypted_file_result:
                            decrypted_file_result.write(decrypted_content)
            else:
                if extension == ".txt":
                    with open(os.path.join(dir_path, input_file), 'r') as decrypted_file:
                        decrypted_content = decrypted_file.read()
                        if instructions_dict['type'] == "Caesar":
                            caesar_input = CaesarCipher(instructions_dict['key'])
                            encrypted_content = caesar_input.encrypt(decrypted_content)
                        if instructions_dict['type'] == "Vigenere":
                            if type(instructions_dict['key']) is str:
                                vigenere_input = getVigenereFromStr(instructions_dict['key'])
                            else:
                                vigenere_input = VigenereCipher(instructions_dict['key'])
                            encrypted_content = vigenere_input.encrypt(decrypted_content)
                        new_filename = name + ".enc"
                        with open(os.path.join(dir_path, new_filename), 'w') as encrypted_file_result:
                            encrypted_file_result.write(encrypted_content)

if __name__ == "__main__":
    processDirectory("Files")

