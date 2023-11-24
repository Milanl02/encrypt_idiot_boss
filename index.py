from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import base64
import os

# Helper method to convert bytes to strings
def utf8(s: bytes):
    return str(s, 'utf-8')

# Obtain a copy of the old_private_key from the old_private_key.pem file:
def obtain_old_private_key(file_name):
    with open (file_name, 'rb') as file:
        old_private_key_data = file.read()
        old_private_key = serialization.load_pem_private_key(old_private_key_data, password=None, backend=default_backend())
    return old_private_key

# Obtain a copy of the new_public_key from the new_public_key.pem file:
def obtain_new_public_key(file_name):
    with open (file_name, 'rb') as file:
        new_public_key_data = file.read()
        new_public_key = serialization.load_pem_public_key(new_public_key_data, backend=default_backend())
    return new_public_key

# Use the old_private_key to decrypt customer files in the user_profiles directory:
def decrypt_message(msg, key):
    decrypted_msg = key.decrypt(
        base64.b64decode(msg), 
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_msg

# Use the new_public_key to encrypt the customer data:
def encrypt_message(msg, key):
    encrypted_msg = base64.b64encode(key.encrypt(
        msg, 
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ))

    return encrypted_msg

# Save the newly-encrypted data into a file in a directory named new_user_profiles:
def store_new_encrypted_data(directory_name, file_name, encrypted_message):
    with open(f'{directory_name}/{file_name}', 'wb') as file:
        file.write(encrypted_message)

def main():
    # Obtain a copy of the old_private_key:
    old_private_key = obtain_old_private_key('old_private_key.pem')
    # Obtain a copy of the new_public_key:
    new_public_key = obtain_new_public_key('new_public_key.pem')

   # Create a directory named new_user_profiles:
    directory_name = 'new_user_profiles'
    create_directory = os.mkdir(directory_name)

    # Use the old_private_key to decrypt ALL of the customer files in the user_profiles directory:
    # Directory Name:
    name_of_directory = 'user_profiles'

    for fn in os.listdir(name_of_directory):
        path_of_file = os.path.join(name_of_directory, fn)
        with open(path_of_file, 'rb') as file:
            encrypted_data = file.read()

        # Use the old_private_key to decrypt the customer data:
        decrypted_msg = decrypt_message(encrypted_data, old_private_key)

        # Use the new_public_key to encrypt the customer data:
        encrypted_msg = encrypt_message(decrypted_msg, new_public_key)

        # Save the newly-encrypted data into a file in a directory named new_user_profiles:
        store_new_encrypted_data(directory_name, fn, encrypted_msg)

    print(f"All files in '{name_of_directory}' directory have been decrypted and re-encrypted with a new key! Files were saved in a new directory called '{directory_name}'.")

if __name__ == "__main__":
    main()