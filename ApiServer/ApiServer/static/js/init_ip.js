$(document).ready(function(){
    $("#regs").click(function () {
        alert('good')
        // show_url='/api/v1/show_id'

        id="2222"
        trans(show_url)
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
            },
            //请求失败，包含具体的错误信息
            error : function(e){
                alert("未知错误")

            }
        });
}