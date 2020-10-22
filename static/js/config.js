/**
 * Created by chenking on 2018/4/5.
 */
function changemenu(id) {

    var  $td = $("#"+id).children('td');
      var name = $td.eq(0).find("input").val();
      var path=$td.eq(1).find("input").val();
      var sortid=$td.eq(2).find("input").val();
      var page=$td.eq(3).find("input").val();
      var visible=$td.eq(4).find("input").val();
      var imgurl=$td.eq(5).find("input").val();
      menu={name:name,path:path,sortid:sortid,page:page,visible:visible,id:id,imgurl:imgurl};
     $.ajax({
    type: 'POST',
    url: '/changemenu',
    data: JSON.stringify(menu),
    contentType: 'application/json; charset=UTF-8',
    dataType: 'json',
    success: function(data) {
        if(data.code==200){
             alert('修改成功');
             window.reload();
        }else {
            alert(data.msg);
        }

    },
    error: function(xhr, type) {
    }
    });
}
function addmenu() {
    var form=$('#formenu').serialize();
    $.post('/addmenu',form,function (data) {
        if(data.code==200){
            alert('插入成功');
            window.reload();
        }else{
            alert('插入失败');
        }

    })
}

//更新节点信息
function changenodetype(id) {
     var  $td = $("#node_"+id).children('td');
      var name = $td.eq(1).find("input").val();
      var imgurl=$td.eq(2).find("input").val();
      nodetype={name:name,imgurl:imgurl,id:id};
    $.post('/changenodetype',nodetype,function (data) {
        if(data.code==200){
            alert('修改成功');
            window.reload();
        }else{
            alert(''+data.msg);
        }
    })

}
//添加节点
function addnodetype() {
    var formnode=$('#nodeform').serialize();
    $.post('/addnodetype',formnode,function (data) {
        if(data.code==200){
            alert("添加成功");
            window.reload();
        }else{
            alert(''+data.msg);
        }
    })
}

//删除节点评分项
function deletenodetype(id) {
     var  $td = $("#node_"+id).children('td');
     nodetype={id:id};
    $.post('/deletenodetype',nodetype,function (data) {
        if(data.code==200){
            alert('删除成功');
            window.reload();
        }else{
            alert(''+data.msg);
        }
    })

}

//更新服务信息
function changeServicetype(id) {
     var  $td = $("#service_"+id).children('td');
      var name = $td.eq(1).find("input").val();
      servicetype={name:name,id:id};
    $.post('/changeServicetype',servicetype,function (data) {
        if(data.code==200){
            alert('修改成功');
            window.reload();
        }else{
            alert(''+data.msg);
        }
    })

}
//添加服务
function addServicetype() {
    var formnode=$('#servicetype').serialize();
    $.post('/addServicetype',formnode,function (data) {
        if(data.code==200){
            alert("添加成功");
            window.reload();
        }else{
            alert(''+data.msg);
        }
    })
}

//删除服务信息
function deleteServicetype(id) {
      var  $td = $("#node_"+id).children('td');
      var name = $td.eq(1).find("input").val();
      ahpconfig={name:name,id:id};
    $.post('/deleteServicetype',ahpconfig,function (data) {
        if(data.code==200){
            alert('删除成功');
            window.reload();
        }else{
            alert(''+data.msg);
        }
    })

}

//删除安全评价信息
function deleteAssessment(id) {
      assessment={id:id};
    $.post('/deleteAssessment',assessment,function (data) {
        if(data.code==200){
            alert('删除成功');
            window.reload();
        }else{
            alert(''+data.msg);
        }
    })

}

//更改安全评价配置
function changeAssessment(id) {
    var $td=$('#assessment_'+id).children('td');
    var element = $td.eq(1).find("input").val();
    var S1 = $td.eq(2).find("input").val();
    var S2 = $td.eq(3).find("input").val();
    var S3 = $td.eq(4).find("input").val();
    var S4 = $td.eq(5).find("input").val();
    var S5 = $td.eq(6).find("input").val();
    assessment = {element:element,S1:S1,S2:S2,S3:S3,S4:S4,S5:S5}
    $.post('/changeAssessment',assessment,function (data) {
        if(data.code==200){
            alert('修改成功');
            window.reload();
        }else{
            alert(''+data.msg)
        }
    })

}
//添加安全评价配置
function addAssessment() {
    var assessment=$('#assessment').serialize();
    $.post('/addAssessment',assessment,function (data) {
        if(data.code==200){
            alert('添加成功');
            window.reload();
        }else if(data.code==300){
            alert('请保证元素控制在11个以内');
            window.reload();
        }
    })

}
//更新AHP评分项
function changejudgement() {
    var judgement=$('#judgement').serialize();
    $.post('/changejudgement',judgement,function (data) {
        if(data.code==200){
            alert('修改成功');
            window.reload();
        }else{
            alert(''+data.msg)
        }
    })

}

/*
//添加AHP评分项
function addjudgement() {
    var formnode=$('#judgement').serialize();
    $.post('/addjudgement',formnode,function (data) {
        if(data.code==200){
            alert("添加成功");
        }else{
            alert(''+data.msg);
        }
    })
}

//删除AHP评分项 未使用

function deletejudgement(id) {
     judgement={id:id};
      var E1thanE2 = $td.eq(1).find("input").val();
      var E1thanE3 = $td.eq(2).find("input").val();
      var E2thanE3 = $td.eq(3).find("input").val();
      var Q1thanQ2 = $td.eq(4).find("input").val();
      var Q1thanQ3 = $td.eq(5).find("input").val();
      var Q1thanQ4 = $td.eq(6).find("input").val();
      var Q2thanQ3 = $td.eq(7).find("input").val();
      var Q2thanQ4 = $td.eq(8).find("input").val();
      var Q3thanQ4 = $td.eq(9).find("input").val();
      var Q5thanQ6 = $td.eq(10).find("input").val();
      var Q5thanQ7 = $td.eq(11).find("input").val();
      var Q5thanQ8 = $td.eq(12).find("input").val();
      var Q5thanQ9 = $td.eq(13).find("input").val();
      var Q6thanQ7 = $td.eq(14).find("input").val();
      var Q6thanQ8 = $td.eq(15).find("input").val();
      var Q6thanQ9 = $td.eq(16).find("input").val();
      var Q7thanQ8 = $td.eq(17).find("input").val();
      var Q7thanQ9 = $td.eq(18).find("input").val();
      var Q8thanQ9 = $td.eq(19).find("input").val();
      var Q10thanQ11 = $td.eq(20).find("input").val();
      ahpconfig={E1thanE2:E1thanE2, E1thanE3:E1thanE3, E2thanE3:E2thanE3, Q1thanQ2:Q1thanQ2, Q1thanQ3:Q1thanQ3, Q1thanQ4:Q1thanQ4, Q2thanQ3:Q2thanQ3, Q2thanQ4:Q2thanQ4, Q3thanQ4:Q3thanQ4, Q5thanQ6:Q5thanQ6, Q5thanQ7:Q5thanQ7, Q5thanQ8:Q5thanQ8, Q5thanQ9:Q5thanQ9, Q6thanQ7:Q6thanQ7, Q6thanQ8:Q6thanQ8, Q6thanQ9:Q6thanQ9, Q7thanQ8:Q7thanQ8, Q7thanQ9:Q7thanQ9, Q8thanQ9:Q8thanQ9, Q10thanQ11:Q10thanQ11};

    $.post('/deletejudgement',judgement,function (data) {
        if(data.code==200){
            alert('删除成功')
        }else{
            alert(''+data.msg)
        }
    })

}
*/