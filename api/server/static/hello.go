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
	"syscall/js"
    "sync"
)
// "encoding/json"
type sqpuk_s struct {
	code            []byte `json:"code"`
	sq       []byte `json:"sq"`
	puk  []byte `json:"puk"`
}
var wg sync.WaitGroup
var sqpuk_login *sqpuk_s
func RsaEncrypt(sqpuk_ptr *sqpuk_s,origData []byte)([]byte,error){  
    //解密pem格式的公钥  
    print(string(sqpuk_ptr.puk) )
    block, _ := pem.Decode(sqpuk_ptr.puk)  
    if block == nil {  
        println("public key error")
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
func GetData()(sqpuk_ptr *sqpuk_s) {
    var sqpuk_b []byte
    client := &http.Client{}
    resp, err := client.Post("http://www.hyluz.cn:5000/get_puk_sq","application/x-www-form-urlencoded",strings.NewReader("ip=2.2.2.2"))
    defer resp.Body.Close()
    sqpuk_b, err = ioutil.ReadAll(resp.Body)
    if err != nil {
        fmt.Println("err",err)
    }
    sqpuk_ptr = &sqpuk_s{}
    sqpuk_c:=strings.Replace(string(sqpuk_b),"'","",-1)
    println(sqpuk_c)
  //  println(string(sqpuk_c))
    //err = json.Unmarshal(sqpuk_b, sqpuk_ptr) // JSON to Struct
   // sqpuk_ptr.code=[]byte(GetBetweenStr(sqpuk_c,`code: `,","))//暴力读取json
    puk1:=strings.Replace(GetBetweenStr(sqpuk_c,`puk: `,`,`),"\\n","\n",-1)
    sqpuk_ptr.puk=[]byte(strings.Replace(puk1,"\\"," ",-1))
    //println(string(sqpuk_ptr.puk))

    sqpuk_ptr.sq=[]byte(GetBetweenStr(sqpuk_c,`sq: `,`,`))
   // println(string(sqpuk_ptr.sq))
    println("puk:",string(sqpuk_ptr.puk))
    println("sq",string(sqpuk_ptr.sq))
    return sqpuk_ptr
    
}
func GetEncode(this js.Value, i []js.Value) interface{} {
    // println("into func1")
    // println("js string:",i[0].String())
    jiami:=[]byte(i[0].String())
    println("jiami",jiami)
    sqpuk:=sqpuk_login
    data, _  :=RsaEncrypt(sqpuk,jiami)
    println(data)
    //println("sq",string(sqpuk.sq))
    println("encode_str",base64.StdEncoding.EncodeToString(data))
    encode_str:=base64.StdEncoding.EncodeToString(data)
    println(encode_str)
    encode_str=strings.Replace(encode_str,"+","@",-1)
	json:="{"+`"sq":`+`"`+string(sqpuk.sq)+`","encode_str":"`+encode_str+`"}` //暴力构造json
	json=strings.Replace(json," ","",-1)
	go main()
	return json
}

func registerCallbacks() {
	js.Global().Set("GetEncode", js.FuncOf(GetEncode))
}

func main(){
	c := make(chan struct{}, 0)
	println("WASM Go Reload.")
	sqpuk_login=GetData()
	// println(sqpuk_login.sq)
	// println(sqpuk_login.puk)

	// register functions
    registerCallbacks()
    <-c

}