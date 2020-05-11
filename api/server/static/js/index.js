
$(document).ready(function(){
    wasm()
    $('#token').text('you get token: '+getCookie('token'))
    // $("#encode").click(function () { })
    $("#encode_bt").click(function () {
        res=GetEncode('I am front')
        console.log(res)
    })

});

// 读取cookie
function  wasm() {
     if (!WebAssembly.instantiateStreaming) {
        // polyfill
        WebAssembly.instantiateStreaming = async (resp, importObject) => {
            const source = await (await resp).arrayBuffer();
            return await WebAssembly.instantiate(source, importObject);
        };
    }

    // const go = new Go();
    // let mod, inst;
    // WebAssembly.instantiateStreaming(fetch("/static/encode.wasm", {
    //   headers: {
    //     "Content-Type": "application/wasm",
    //      },
    // }),go.importObject).then(
    //     async result => {
    //         mod = result.module;
    //         inst = result.instance;
    //         await go.run(inst);
    //     }
    // );
    const go = new Go();
    let mod, inst;
  // var importObject = {
  //       imports: {
  //         imported_func: function(arg) {
  //           console.log(arg);
  //         }
  //       }
  //     };

      fetch('/static/encode.wasm').then(response =>
        response.arrayBuffer()
      ).then(bytes =>
        WebAssembly.instantiate(bytes, go.importObject)
      ).then(
          async result =>
    {
        mod = result.module;
        inst = result.instance;
        await
        go.run(inst);
    }
      );

    function encode_str() {

    }
}

function getCookie(cname)
{
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i=0; i<ca.length; i++)
  {
    var c = ca[i].trim();
    if (c.indexOf(name)==0) return c.substring(name.length,c.length);
  }
  return "";
}
function trans(urll,dataa) {
    $.ajax({
            type : "GET",
            contentType: "application/json;charset=UTF-8",
            url : urll,
            data:dataa,
            async:false,
            dataType:'json',
            success : function(result) {
                setCookie('token',result['token'])
                alert('good')
                 window.location.href = '/index';
            },
            //请求失败，包含具体的错误信息
            error : function(e){
                alert("未知错误")

            }
        });
}