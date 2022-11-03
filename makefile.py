from cryptography.fernet import Fernet

class safeHello(object):

    def __init__(self):
        pass

    def load_key(self):
        """
        Loads the key from the current directory named `key.key`
        """
        return open("make.key", "rb").read()

    def decrypt(self):
        key = self.load_key()
        f = Fernet(key)
        decrypted_encrypted = f.decrypt()

    def encrypt(self,filename, key):
        """
        Given a filename (str) and key (bytes), it encrypts the file and write it
        """
        f = Fernet(key)
        with open(filename, "rb") as file:
            # read all file data
            file_data = file.read()
        # encrypt data
        encrypted_data = f.encrypt(file_data)
        # write the encrypted file
        with open(filename, "wb") as file:
            file.write(encrypted_data)

    def decrypt(self):
        """
        Given a filename (str) and key (bytes), it decrypts the file and write it
        """
        key = self.load_key()
        name = 'letsfoit.txt'
        f = Fernet(key)
        with open(name, "rb") as file:
            # read the encrypted data
            encrypted_data = file.read()
        # decrypt data

        decrypted_data = (f.decrypt(encrypted_data)).split()

        return decrypted_data

if __name__ == "__main__":

    sf = safeHello()
    '''
    key = sf.load_key()
    f = Fernet(key)
    name = 'letsfoit.txt'
    #message = "634b944da99b0c00016f4c02 fb43171f-1aad-4418-8577-0ce672b308c6 SepactMfdst1114".encode()
    #encrypted = f.encrypt(message)
    #print(encrypted)


    #filename = 'reado.txt.rtf'
    h = sf.decrypt(name,key)
    print(h)
    '''
    #decrpyted = (f.decrypt(encrypted)).split()
    #str = str(decrpyted[0], encoding='utf-8')

