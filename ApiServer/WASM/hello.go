package main
import (
    "fmt"
    "io/ioutil"
    "net/http"
    "strings"   
    "crypto/rand"  
    "crypto/rsa"  
    "crypto/x509"  
    "encoding/base64"  
    "encoding/pem"  
    "errors"  
)
// "encoding/json"
type sqpuk_s struct {
	code            []byte `json:"code"`
	sq       []byte `json:"sq"`
	puk  []byte `json:"puk"`
}
func RsaEncrypt(sqpuk_ptr *sqpuk_s,origData []byte) ([]byte, error) {  
    //解密pem格式的公钥  
    block, _ := pem.Decode(sqpuk_ptr.puk)  
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
func GetBetweenStr(str, start, end string) string {
    n := strings.Index(str, start)
    if n == -1 {
        n = 0
    } else {
        n = n + len(start) 
    }
    str = string([]byte(str)[n:])
    m := strings.Index(str, end)
    if m == -1 {
        m = len(str)
    }
    str = string([]byte(str)[:m])
    return str
}
func GetData()(sqpuk_ptr *sqpuk_s, err error) {
    var sqpuk_b []byte
    client := &http.Client{}
    resp, err := client.Post("http://39.96.60.14:5000/get_puk_sq","application/x-www-form-urlencoded",strings.NewReader("ip=1.1.1.1"))
    defer resp.Body.Close()
    sqpuk_b, err = ioutil.ReadAll(resp.Body)
    //println(string(sqpuk_b))
    if err != nil {
        fmt.Println(err)
    }
    sqpuk_ptr = &sqpuk_s{}
    sqpuk_c:=strings.Replace(string(sqpuk_b),"'","",-1)
    //err = json.Unmarshal(sqpuk_b, sqpuk_ptr) // JSON to Struct
    sqpuk_ptr.code=[]byte(GetBetweenStr(sqpuk_c,"code: ",","))
    puk1:=strings.Replace(GetBetweenStr(sqpuk_c,"puk: ",","),"\\n","\n",-1)
    //print(puk1)
    sqpuk_ptr.puk=[]byte(strings.Replace(puk1,"\\"," ",-1))
    sqpuk_ptr.sq=[]byte(GetBetweenStr(sqpuk_c,"sq: ",","))
    return sqpuk_ptr, err
    
}
func main() {
	sqpuk, _  := GetData()

	println(string(sqpuk.code))
	println(string(sqpuk.sq))
	println(string(sqpuk.puk))
	jiami:=[]byte("hello")
	data, _ :=RsaEncrypt(sqpuk,jiami)
	println(base64.StdEncoding.EncodeToString(data)) 
}