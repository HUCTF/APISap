package main  
import (  
    "crypto/rand"  
    "crypto/rsa"  
    "crypto/x509"  
    "encoding/base64"  
    "encoding/pem"  
    "errors"  
    "fmt"  
) 
var publicKey = []byte(`  
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDfw1/P15GQzGGYvNwVmXIGGxea
8Pb2wJcF7ZW7tmFdLSjOItn9kvUsbQgS5yxx+f2sAv1ocxbPTsFdRc6yUTJdeQol
DOkEzNP0B8XKm+Lxy4giwwR5LJQTANkqe4w/d9u129bRhTu/SUzSUIr65zZ/s6TU
GQD6QzKY1Y8xS+FoQQIDAQAB
-----END PUBLIC KEY-----    
`)  
func RsaEncrypt(origData []byte) ([]byte, error) {  
    //解密pem格式的公钥  
    block, _ := pem.Decode(publicKey)  
    if block == nil {  
        return nil, errors.New("public key error")  
    }  
    // 解析公钥  
    pubInterface, err := x509.ParsePKIXPublicKey(block.Bytes)  
    if err != nil {  
        return nil, err  
    }  
    // 类型断言  
    pub := pubInterface.(*rsa.PublicKey)  
    //加密  
    return rsa.EncryptPKCS1v15(rand.Reader, pub, origData)  
} 
func main() {  
    data, _ := RsaEncrypt([]byte("hello world"))  
    fmt.Println(base64.StdEncoding.EncodeToString(data))  

} 