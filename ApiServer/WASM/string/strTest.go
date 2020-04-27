package main

import (
	"syscall/js"
)

func StrTest(this js.Value, i []js.Value) interface{} {
	str1 := i[0].String()
	str2 := i[1].String()
	println("wasm str1:",str1)
	println("wasm str2:",str2)
	
	return "wasm return string"
}



func registerCallbacks() {
	js.Global().Set("StrTest", js.FuncOf(StrTest))
}

func main() {
	c := make(chan struct{}, 0)
	println("WASM Go Initialized")
	// register functions
	registerCallbacks()
	<-c
}