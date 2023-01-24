import json
import os

NUM_OF_LETTERS = 26

class CaesarCipher:
    def __init__(self, key):
        self.key = key

    #encrypt a given strin by Caesar code according to the key of the class.
    # @param plaintext - the string to encrypt.
    # @return - encrypted string.  
    def encrypt(self, plaintext: str) -> str:
        encrypted = ""
        for i in plaintext:
            if i.isalpha():
                if i.islower():
                    encrypted += chr((ord(i) - ord('a') +
                                     self.key) % NUM_OF_LETTERS + ord('a'))
                else:
                    encrypted += chr((ord(i) - ord('A') +
                                     self.key) % NUM_OF_LETTERS + ord('A'))
            else:
                encrypted += i
        return encrypted

    #decrypt a given strin by Caesar code accordong to the key of the class.
    # @param ciphertext - the string to decrypt. 
    # @return - decrypted string.
    def decrypt(self, ciphertext: str) -> str:
        decryptor = CaesarCipher(-self.key)
        return decryptor.encrypt(ciphertext)

    #change the class's key
    def setKey(self, shifter):
        self.key = shifter


class VigenereCipher(CaesarCipher):
    def __init__(self, keys):
        super().__init__(keys[0])
        self.keys = keys

    # encrypt a given strin by Vigener code according to the class's list of keys.
    # @param plaintext - the string to encrypt.
    # @return - encrypted string.
    def encrypt(self, plaintext: str) -> str:
        encrypted = ""
        keyIndex = 0
        for i in range(len(plaintext)):
            super().setKey(self.keys[keyIndex % len(self.keys)])
            encrypted += super().encrypt(plaintext[i])
            if plaintext[i].isalpha():
                keyIndex += 1
        return encrypted

    # decrypt a given strin by Vigener code according to the class's list of keys.
    # @param plaintext - the string to decrypt.
    # @return - decrypted string.
    def decrypt(self, ciphertext: str) -> str:
        reversedShifters = []
        for i in self.keys:
            reversedShifters.append(-i)
        decryptor = VigenereCipher(reversedShifters)
        return decryptor.encrypt(ciphertext)

# Extract from given text list of keys for a Vigenere code.
# @param keyString - the given text.
# @return - VigenereCipher with list of keys according to the given text.
def getVigenereFromStr(keyString: str) -> VigenereCipher:
    keys = []
    for i in keyString:
        if i.isalpha():
            if i.islower:
                keys.append(ord(i) - ord('a'))
            else:
                keys.append(ord(i) - ord('A'))
    return VigenereCipher(keys)

# Encrypt/decrypt file from give directory according to instructions in the configuration file in the directory.
# the file contain the wanted action(encrypt/decrypt), wanted code(Caesar/Vigenere), and key to the code.
# In case of encryption encrypt all the .txt files and save it in .enc files.
# In case of decryption decrypt all the .enc files and save it in .txt files.
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

