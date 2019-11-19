function Register() {
    var form_data = new FormData();
    var name = document.getElementById('name').value;
    var account = document.getElementById('account').value;
    var password = document.getElementById('password').value;
    var age = document.getElementById('age').value;
    var school = document.getElementById('school').value;
    var email = document.getElementById('email').value;
    var parent = document.getElementById('parent').value;
    var relation = document.getElementById('relation').value;
    var tel = document.getElementById('tel').value;
    var parent_tel = document.getElementById('parent_tel').value;
    var sex = $("#sex option:selected").val();
    form_data.append('name', name);
    form_data.append('account', account);
    form_data.append('password', password);
    form_data.append('tel', tel);
    form_data.append('sex', sex);
    form_data.append('age', age);
    form_data.append('school', school);
    form_data.append('email', email);
    form_data.append('parent', parent);
    form_data.append('relation', relation);
    form_data.append('parent_tel', parent_tel);
    $.ajax({
        url: "/register",
        type: "HTTP",
        method: "POST",
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function(req) {
            console.log(req);
            try{
                var ret = JSON.parse(req);
            } catch(e) {
                var ret = eval("("+ req +")");
            }
            if (Number(ret['status']) != 1) {
                alert(req);
            } else {
                alert("register successfully");
                window.location.replace("/index");
            }
        },
        error: function() {
            alert('register failed');
        }
    })
}

function Login() {
    var form_data = new FormData();
    var account = document.getElementById('account').value;
    var password = document.getElementById('password').value;
    form_data.append('account', account);
    form_data.append('password', password);
    $.ajax({
        url: "/login",
        type: "HTTP",
        method: "POST",
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function(req) {
            console.log(req);
            try{
                var ret = JSON.parse(req);
            } catch(e) {
                var ret = eval("("+ req +")");
            }
            if (Number(ret['status']) != 1) {
                alert(req);
            } else {
                window.location.href="/index";
            }
        },
        error: function() {
            alert('login failed');
        }
    })
}

$(function(){
    M.AutoInit();
});