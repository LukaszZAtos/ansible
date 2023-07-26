package main

import (
        "crypto/aes"
        "crypto/cipher"
        "encoding/base64"
        "fmt"
        "os"
)

// Hardcoded salt for encryption and decryption
const hardcodedSalt = "297b77dabbd077213a9e854b85730441"

func generateKey(salt string) []byte {
        key := []byte(hardcodedSalt + salt)
        hashKey := make([]byte, 32)
        copy(hashKey, key)
        return hashKey
}

func encryptToken(token, salt string) string {
        key := generateKey(salt)
        block, err := aes.NewCipher(key)
        if err != nil {
                fmt.Println("Error creating AES cipher:", err)
                os.Exit(1)
        }

        cipherText := make([]byte, aes.BlockSize+len(token))
        iv := cipherText[:aes.BlockSize]
        // Use the same IV used for encryption
        copy(iv, hardcodedSalt)

        cfb := cipher.NewCFBEncrypter(block, iv)
        cfb.XORKeyStream(cipherText[aes.BlockSize:], []byte(token))

        return base64.StdEncoding.EncodeToString(cipherText)
}

func decryptToken(encryptedToken string) string {
        key := generateKey("") // Empty salt for decryption
        block, err := aes.NewCipher(key)
        if err != nil {
                fmt.Println("Error creating AES cipher:", err)
                os.Exit(1)
        }

        decodedCipherText, err := base64.StdEncoding.DecodeString(encryptedToken)
        if err != nil {
                fmt.Println("Error decoding base64:", err)
                os.Exit(1)
        }

        iv := decodedCipherText[:aes.BlockSize]
        // Use the same IV used for encryption
        copy(iv, hardcodedSalt)

        decodedCipherText = decodedCipherText[aes.BlockSize:]

        cfb := cipher.NewCFBDecrypter(block, iv)
        cfb.XORKeyStream(decodedCipherText, decodedCipherText)

        return string(decodedCipherText)
}

func main() {
        if len(os.Args) < 3 {
                fmt.Println("Usage: encrypt_decrypt.go <encrypt|decrypt> <token>")
                os.Exit(1)
        }

        action := os.Args[1]
        token := os.Args[2]

        if action == "encrypt" {
                encryptedToken := encryptToken(token, hardcodedSalt)
                fmt.Println("Encrypted Token:", encryptedToken)
        } else if action == "decrypt" {
                decryptedToken := decryptToken(token)
                fmt.Println("Decrypted Token:", decryptedToken)
        } else {
                fmt.Println("Invalid action. Use 'encrypt' or 'decrypt'.")
                os.Exit(1)
        }
}
