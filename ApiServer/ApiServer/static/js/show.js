ip=''
kid=''
user_id=''
text=''
token=''
puk=''
sq=''
cipher_text=''
cipher_decode=''
$(document).ready(function () {
    var $=jQuery.noConflict();
    ip=$('#ip').text()
    kid=$('#kid').text()
    user_id=$('#user_id').text()
    text=$('#text').text()

    $('button').click(function () {
        ip=$('#ip').text()
        kid=$('#kid').text()
        user_id=$('#user_id').text()
        text=$('#text').text()
        token=$('#token').text()
        puk=$('#puk').text()
        sq=$('#sq').text()
        cipher_text=$('#cipher_text').text()
        cipher_decode=$('#cipher_decode').text()
    })

    $('#get_token').click(function () {
        url='http://www.hyluz.cn:5000/init_token?ip='+ip+'&user_id='+user_id
        data='init_token'
        trans(url,data)
    })
       $('#get_puk_sq').click(function () {
        url='http://www.hyluz.cn:5000/get_puk_sq?ip='+ip
        data='get_puk_sq'
        trans(url,data)
    })
     $('#rsa_encode').click(function () {
        $('#cipher_text').text(encode(puk,text))

    })
     $('#server_decode').click(function () {
         cipher_text=cipher_text.replace(/\+/g,"@")
        url='http://www.hyluz.cn:5000/server_decode?ip='+ip+'&sq='+sq+'&cypher='+cipher_text
        data='server_decode'
        trans(url,data)
    })



});

function trans(urll,data) {
     $.ajax({
            type : "GET",
            contentType: "application/json;charset=UTF-8",
            url : urll,
            // data:JSON.stringify(data),
            success : function(result) {
                alert(result)
                if(typeof(result)=='string')
                { if(data!='server_decode'){
                    result = result.replace(/\'/g, "\"");}
                    alert(result)
                    result=$.parseJSON(result)
                }
                // alert(result['puk'])
                if(data=='init_token'){
                    // alert(result['token'])
                    $('#token').text(result['token'])
                    token=result['token']
                }else if (data=='get_puk_sq'){
                    $('#puk').text(result['puk'])
                    $('#sq').text(result['sq'])
                    puk=result['puk']
                    sq=result['sq']
                }else if(data=='server_decode'){
                    $('#cipher_decode').text(result['result'])
                }

            },
            //请求失败，包含具体的错误信息
            error : function(e){
                alert("未知错误")

            }
        });
}

function encode(PUBLIC_KEY,strr) {
    PUBLIC_KEY = PUBLIC_KEY.replace(/\\n/g, "");
    // alert(strr)
    // alert(PUBLIC_KEY)
    var encrypt = new JSEncrypt();
    encrypt.setPublicKey(PUBLIC_KEY);
    var encrypted = encrypt.encrypt(strr);
    console.log('加密后数据:%o', encrypted);
    return encrypted

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
function setCookie(name,value)
{
     var Days = 30;
     var exp = new Date();
     exp.setTime(exp.getTime() + Days*24*60*60*1000);
     document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString();
}