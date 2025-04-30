
$("#id_TaskEnc_select_Custom_Env").on("change", function () {
  var csrfToken = "{{ csrf_token }}";


  var Id = $("#id_TaskEnc_select_Custom_Env option:selected").val();

  $.ajax({
    type: "GET",
    url: '/ConfCen/TaskEnc/' + Id + '/',
    headers: {
      'X-CSRFToken': csrfToken // 使用JavaScript变量添加CSRF令牌
    },

    cache: false,
    dataType: "json",
    data: {

    },
    success: function (msg) {


      editorElement = document.querySelector('.ace_editor');
      ace.edit(editorElement).getSession().setValue(msg.Custom_Env);


    }
  });


});


$('button[name="TaskEnc_exec"]').click(function () {
  alert("11");
  var buttonValue = $(this).val();
  var span = $(this).find("span")
  var button = $(this); // 获取按钮本身

  s = span.text()

  span.attr({ "disabled": true });
  
  span.text(s + "中");
  button.attr("disabled", true);

  $.ajax({
    type: "PUT",
    url: '/ProjManage/Projdep/' + buttonValue + '/TaskEnc_exec/',
    headers: {
      'X-CSRFToken': csrfToken // 使用JavaScript变量添加CSRF令牌
    },

    cache: false,
    dataType: "json",
    data: {
      "action": s,
    },
    success: function (msg) {


      span.attr({ "disabled": false });



      alert("执行成功")
      location.reload(); // 刷新页面


    }
  });

});

