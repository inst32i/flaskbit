/**
 * Created by chenking on 2018/5/17.
 */
function createmplate() {
    // 获取所有表单信息，提交到服务器
 var form=$('#formtemplate').serialize();
    $.post('/addtemplate',form,function (data) {
        if(data.code==200){

            window.setTimeout("window.location='"+data.path+"'",1000);
            alert('创建成功');
        }else{
            alert('创建失败');

        }

    })
}