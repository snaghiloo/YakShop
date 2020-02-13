document.addEventListener('submit',function(e){
  e.preventDefault();
  var param1 = document.getElementById('first').value;
  var param2 = document.getElementById('last').value;
  var param3 = document.getElementById('name').value;
  var newUrl = 'http://127.0.0.1:5000/yak-shop/order/13'; 
  var xhr = new XMLHttpRequest();
        xhr.open("POST", newUrl, true);
		xhr.setRequestHeader("content-type", "application/json");
        xhr.onload = () => {
            if (xhr.status === 201) {
                var res = JSON.parse(xhr.response);
              console.log(res)
              document.getElementById('result').innerHTML = 'Successful!';
            }
			else if (xhr.status === 206) {
                var res = JSON.parse(xhr.response);
              console.log(res)
              document.getElementById('result').innerHTML = 'Partial Successful!';
            }
            else {
                var error = JSON.parse(xhr.response);
               console.log(error);
               document.getElementById('result').innerHTML = 'Failure!';
            }
        };
        xhr.send(JSON.stringify({customer:param3, order:{milk: param1,skins:param2}}));
})