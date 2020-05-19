ip=''
kid='2'
user_id='Luz'
text=''
token=''
puk=''
sq=''
cipher_text=''
cipher_decode=''
$(document).ready(function () {
        var $=jQuery.noConflict();
    init_trans('http://www.hyluz.cn:5000/search_by_kid?kid='+kid,'init_num')
    // init_trans()

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
    $('#liuchen').click(function () {
        // alert('img')
        $(location).attr('href', '/view/img');
    })
    $('#download').click(function () {
        window.location.href = '/static/wasm.rar'
    })

    $('#ceshi1').click(function () {
        url='http://www.hyluz.cn:5000/init_ip?ip='+ip+'&kid='+kid
        data='init_ip'
        trans(url,data)
    })

    $('#get_token').click(function () {
        url='http://www.hyluz.cn:5000/init_token?ip='+ip+'&user_id='+user_id
        data='init_token'
        trans(url,data)
    })
    $('#ceshi2').click(function () {
        url='http://www.hyluz.cn:5000/init_token?ip='+ip+'&user_id='+user_id
        data='init_token'
        trans(url,data)
    })

    $('#get_puk_sq').click(function () {
        url='http://www.hyluz.cn:5000/get_puk_sq?ip='+ip
        data='get_puk_sq'
        trans(url,data)
    })
    $('#ceshi4').click(function () {
        url='http://www.hyluz.cn:5000/get_puk_sq?ip='+ip
        data='get_puk_sq'
        trans(url,data)
    })
    $('#rsa_encode').click(function () {
        $('#cipher_text').text(encode(puk,text))

    })
    $('#token_check_bt').click(function () {
        url='http://www.hyluz.cn:5000/check_token?ip='+ip+'&token='+token+'&user_id='+user_id
        data='check_token'
        // alert(url)
        trans(url,data)
    })
    $('#ceshi3').click(function () {
        url='http://www.hyluz.cn:5000/check_token?ip='+ip+'&token='+token+'&user_id='+user_id
        data='check_token'
        // alert(url)
        trans(url,data)
    })
    $('#server_decode').click(function () {
         cipher_text=cipher_text.replace(/\+/g,"@")
        url='http://www.hyluz.cn:5000/server_decode?ip='+ip+'&sq='+sq+'&cypher='+cipher_text
        data='server_decode'
        trans(url,data)
    })
    $('#ceshi5').click(function () {
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
                // alert(result)
                if(typeof(result)=='string')
                { if(data!='server_decode'){
                    result = result.replace(/\'/g, "\"");}
                    // alert(result)
                    result=$.parseJSON(result)
                }
                // alert(JSON.stringify(result))
                if(data=='init_token'){
                    // alert(result['token'])
                    $('#token').text(result['token'])
                    $('#token3').text(result['token'])
                    $('#res2').text(JSON.stringify(result))
                    token=result['token']
                }else if (data=='get_puk_sq'){
                    $('#puk').text(result['puk'])
                    $('#sq').text(result['sq'])
                    $('#sq6').text(result['sq'])
                    $('#res4').text(JSON.stringify(result))
                    puk=result['puk']
                    sq=result['sq']
                }else if(data=='server_decode'){
                    $('#res5').text(JSON.stringify(result))
                    $('#cipher_decode').text(result['result'])
                }else if(data=='check_token'){
                    $('#res3').text(JSON.stringify(result))
                     $('#token_check').text(result['msg'])
                }else if(data=='init_ip'){
                     $('#res1').text(JSON.stringify(result))
                }

            },
            //请求失败，包含具体的错误信息
            error : function(e){
                alert("未知错误")

            }
        });
}

function init_trans(urll,op){
     $.ajax({
            type : "GET",
            contentType: "application/json;charset=UTF-8",
            url : urll,
            // data:JSON.stringify(data),
            success : function(result) {
                // alert(JSON.parse(result['result']))
                res=JSON.parse(result['result'])
                if(op=='init_num'){
                    var text=''
                    for(var each in res){
                        // alert(each)
                        text+='<div class="panel panel-default"><div class="panel-heading">ip:'+each+' </div>'
                        text+='<table class="table"><th>功能</th><th>剩余使用次数</th><tr><td>token</td><td>'+res[each]['token']+'</td><td><button type="button" class="btn btn-default bt_num"  id="token_'+ip+'">查看</button></td></tr>'
                        text+=' <tr><td>rsa</td><td>'+res[each]['msg']+'</td><td><button type="button" class="btn btn-default bt_num"  id="msg_'+ip+'">查看</button></td></tr>'
                        text+='</table></div>'

                    }
                    $('#gn').html(text)
                }

            $('.bt_num').click(function () {
                    // alert(this.id)
                // alert(this.id.substring(0,5))
                    if(this.id.substring(0,3)=='msg'||this.id.substring(0,5)=='token') {
                        // alert(1)
                        if (this.id.substring(0, 3) == 'msg') {
                            table_trans('http://www.hyluz.cn:5000/msg_sql?kid=' + kid + '&operator=search_all&ip=' + ip, this.id)
                        }else if (this.id.substring(0, 5) == 'token') {
                            // alert(2)
                            table_trans('http://www.hyluz.cn:5000/token_sql?kid=' + kid + '&operator=search_all&ip=' + ip, this.id)
                        }
                    }
                    // alert('good')
                })
            },
            //请求失败，包含具体的错误信息
            error : function(e){
                alert("未知错误")

            }
        });
}


function table_trans(urll,op) {
    $.ajax({
            type : "GET",
            contentType: "application/json;charset=UTF-8",
            url : urll,
            // data:JSON.stringify(data),
            success : function(result) {
                // alert(JSON.stringify(result['result']))
                res=result['result']
                if (op.substring(0, 5) == 'token') {
                    var text='<div class="panel panel-default " ><div class="panel-heading"><h3 class="panel-title" style="margin: 0 auto">表：'+op+'</h3></div>'
                    text+='<div class="panel-body">ip:'+ip+'</div> <table class="table" max-height="800px" style="overflow-y: auto"><th>user_id</th><th>time_code</th><th>token</th>'
                     for(each in res){
                        text+='<tr><td><div style="overflow-y: auto; max-width: 400px;max-height: 60px">'+res[each]['user_id']+'</div></td><td><div style="overflow-y: auto; max-width: 400px;max-height: 60px">'+res[each]['time_code']+'</div></td><td><div style="overflow-y: auto; max-width: 400px;max-height: 60px">'+res[each]['token']+'</div></td></tr>'
                    }
                    text+='</table></div>'
                    $('#table1').html(text)
                }else if (op.substring(0, 3) == 'msg') {
                    var text='<div class="panel panel-default " ><div class="panel-heading"><h3 class="panel-title" style="margin: 0 auto">表：'+op+'</h3></div>'
                    text+='<div class="panel-body">ip:'+ip+'</div><table class="table" ><th>prk</th><th>puk</th><th>sq</th><th>time_code</th>'
                    for(each in res){
                        text+='<tr><td><div style="overflow-y: auto; max-width: 400px;max-height: 60px">'+res[each]['prk']+'</div></td><td><div style="overflow-y: auto; max-width: 400px;max-height: 60px">'+res[each]['puk']+'</div></td><td><div style="overflow-y: auto; max-width: 400px;max-height: 60px">'+res[each]['sq']+'</div></td><td><div style="overflow-y: auto; max-width: 400px;max-height: 60px">'+res[each]['time_code']+'</div></td></tr>'
                    }
                    text+='</table></div>'
                    $('#table1').html(text)
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