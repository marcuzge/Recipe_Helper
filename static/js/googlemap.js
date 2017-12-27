function geocoded(){
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      pos = {
        'lat': position.coords.latitude,
        'lng': position.coords.longitude
      };
  //     alert(pos['lat']);
  // var pos = {
  //             'lat': 33,
  //             'lng': -122
  //           }
      $.ajax({
        type: "POST",
        url: "/search",
        contentType: "application/json",
        data: JSON.stringify({location: pos}),
        dataType: "json",
        success: function() {
            window.location.reload(); 
        },
        error: function(err) {
            console.log(err);
        }
      });
  //   }); 
    });
  // function sendloco (loc) {

  //       $.post('/restaurants_nearby',{lat:loc.coords.latitude,lng:loc.coords.longitude}, 
  //           );
  }

  //   navigator.geolocation.getCurrentPosition(sendloco);
}