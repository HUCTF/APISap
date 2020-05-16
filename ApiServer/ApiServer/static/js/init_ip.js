$(document).ready(function(){
    $("#regs").click(function () {
        alert('gg')

        trans('/view/show')
        alert('no')
        // alert('good')
        // ip=$('#ip').val()
        // mm=$('#mm').val()
        // ip="2.2.2.2"
        // trans(show_url)
    })
});

function trans(urll,data={}) {
     $.ajax({
            type : "POST",
            contentType: "application/json;charset=UTF-8",
            url : urll,
            data:JSON.stringify(data),
            success : function(result) {
                alert(result)
                window.location.href= '/view/show'
            },
            //请求失败，包含具体的错误信息
            error : function(e){
                alert("未知错误")

            }
        });
}