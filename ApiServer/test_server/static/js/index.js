var data_to_server={
    'ip':'2.2.2.2',
    'user_id':'2',
    'token':'',
    'sq':'',
    'cypher':'',
}
var token=''
$(document).ready(function(){
    wasm()
    $('#token').text('you get token: '+getCookie('token'))
    // $("#encode").click(function () { })
    $("#encode_bt").click(function () {
        res=GetEncode('I am front')
        // console.log(res)
        res=JSON.parse(res)
        console.log(res)
        console.log(res['sq'])
        console.log(res['encode_str'])
        data_to_server['sq']=res['sq']
        data_to_server['cypher']=res['encode_str']
        $('#sq').text('sq: '+res['sq'])
        $('#encode_str').text('encode_str: '+res['encode_str'])
    })

     $("#get_msg").click(function () {
         url='/get_server_res'
         data_to_server['token']=getCookie('token')
         trans(url,data_to_server)
         // console.log(res)

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
    const go = new Go();
    let mod, inst;

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
                console.log(result)
                  $('#server_res').text('server_res: '+result['result'])

            },
            //请求失败，包含具体的错误信息
            error : function(e){
                alert("未知错误")

            }
        });
}