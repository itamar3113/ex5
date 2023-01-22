from CaesarCipher import CaesarCipher
import json
import os


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
                            a = CaesarCipher(instructions_dict['key'])
                            decrypted_content = a.decrypt(encrypted_content)
                        if instructions_dict['type'] == "Vigenere":
                            if type(instructions_dict['key']) is str:
                                a = getVigenereFromStr(instructions_dict['key'])
                            else:
                                a = VigenereCipher(instructions_dict['key'])
                            decrypted_content = a.decrypt(encrypted_content)
                        new_filename = name + ".txt"
                        with open(os.path.join(dir_path, new_filename), 'w') as decrypted_file_result:
                            decrypted_file_result.write(decrypted_content)
            else:
                if extension == ".txt":
                    with open(os.path.join(dir_path, input_file), 'r') as decrypted_file:
                        decrypted_content = decrypted_file.read()
                        if instructions_dict['type'] == "Caesar":
                            a = CaesarCipher(instructions_dict['key'])
                            encrypted_content = a.encrypt(decrypted_content)
                        if instructions_dict['type'] == "Vigenere":
                            if type(instructions_dict['key']) is str:
                                a = getVigenereFromStr(instructions_dict['key'])
                            else:
                                a = VigenereCipher(instructions_dict['key'])
                            encrypted_content = a.encrypt(decrypted_content)
                        new_filename = name + ".enc"
                        with open(os.path.join(dir_path, new_filename), 'w') as encrypted_file_result:
                            encrypted_file_result.write(encrypted_content)

