<h1>Your Idiot Boss v1</h1>

<h2>This is v1 of the program.</h2>

<h2>Your idiot boss fell for a phishing exploit and had his private RSA key stolen from his laptop. All 1,000 of your customer files were encrypted using your boss’ public/private key pair so that information is in danger. You have been tasked with decrypting the existing files and then RE-encrypting them with a new key.</h2>

# My Idiot Boss - Starter Code

This repo contains the code you will use at the outset of the "My Idiot Boss" assignment.

* `user_profiles` contains 1,000 encrypted files that were encrypted with the **old** public/private key pair
* `old_private_key.pem` is an encoded version of the private key from the original encryption
* `new_public_key.pem` is an encoded version of the public key you will use to re-encrypt the file data