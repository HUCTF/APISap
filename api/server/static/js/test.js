$(document).ready(function(){
    $("#sub").click(function () {
        // alert('good')
        url='http://127.0.0.1:5000/init_token'
        data={'ip':"2.2.2.2",'user_id':"2"}
        trans(url,data)

    })

});

function trans(urll,dataa) {
    $.ajax({
            type : "GET",
            contentType: "application/json;charset=UTF-8",
            url : urll,
            data:dataa,
            async:false,
            dataType:'json',
            success : function(result) {
                console.log(result['token'])
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
// 设置cookie
function setCookie(name,value)
{
     var Days = 30;
     var exp = new Date();
     exp.setTime(exp.getTime() + Days*24*60*60*1000);
     document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString();
}