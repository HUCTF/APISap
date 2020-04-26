package main
import (
    "fmt"
    "io/ioutil"
    "net/http"
    "strings"
)
func GetData() {
    client := &http.Client{}
    resp, err := client.Post("http://39.96.60.14:5000/get_puk_sq","application/x-www-form-urlencoded",strings.NewReader("ip=1.1.1.1"))
    defer resp.Body.Close()
    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        fmt.Println(err)
    }
    fmt.Println(string(body))
}
func main() {
	fmt.Printf("hello, world\n")
	GetData()
}