

function b64toBlob(b64Data, contentType, sliceSize) {
    contentType = contentType || '';
  sliceSize = sliceSize || 512;

  var byteCharacters = window.atob(b64Data);
  var byteArrays = [];

  for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
        var slice = byteCharacters.slice(offset, offset + sliceSize);

        var byteNumbers = new Array(slice.length);
        for (var i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }

        var byteArray = new Uint8Array(byteNumbers);

        byteArrays.push(byteArray);
  }

  var blob = new Blob(byteArrays, {type: contentType});
  return blob;
}


function AddSlideImgBlobData(element, blob) {
    var url = URL.createObjectURL(blob);
    var li = document.createElement("li");
    var au = document.createElement('img');
    au.src = url;
    li.appendChild(au);
    element.appendChild(li);
}

function AddSlideImgBase64(element, data) {
    var li = document.createElement("li");
    var au = document.createElement('img');
    au.setAttribute('src', 'data:image/png;base64,' + data);
    li.appendChild(au);
    // li.setAttribute('class', 'active');
    element.appendChild(li);
}


function IndexSlide() {
    var num = 3;
    var form_data = new FormData();
    form_data.append('num', num);
    $.ajax({
        url: "/index/display",
        type: "HTTP",
        method: "POST",
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function(req) {
            var ret = JSON.parse(req);
            if (ret['status'] != 1) {
                alert('get images error');
                return;
            } else {
                var imgs = ret['imgs'];
                var index_slide = document.getElementById('index_slide');
                for (var i = 0;i < imgs.length; i++) {
                    // AddSlideImgBlobData(index_slide, b64toBlob(imgs[i]));
                    AddSlideImgBase64(index_slide, imgs[i]);
                }
                $('.slider').slider({full_width: true});
            }
        },
        error: function() {
            alert('register failed');
        }
    })
}

function IsLogin() {
    $("#register_btn").hide();
    $("#login_btn").text("个人");
    $("#login_btn").attr("href", "/personal");
}

function NotLogin() {
    $("#register_btn").show();
    $("#login_btn").text("登陆");
    $("#login_btn").attr("href", "/login");
}

function GetCookie(name) {
    var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
 
    if(arr=document.cookie.match(reg))
 
        return unescape(arr[2]);
    else
        return null;
}

$(function() {
    M.AutoInit();
    var x = document.cookie;
    var token = GetCookie('token');
    var account = GetCookie('account');
    if ((token != null) && (account != null)) {
        IsLogin();
    } else {
        NotLogin();
    }
});
