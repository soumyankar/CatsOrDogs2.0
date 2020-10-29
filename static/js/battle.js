$(document).ready(function() {
  $('#dog').click(function(){
    $.ajax({
			data : {
				selectedModel : $('#dog').val(),
        animalType : 'dog',
        opponentCat : $('#cat').val(),
			},
			type : 'POST',
			url : '/battlehandler'
		}).done(function(data) {
      if(data.gameover){
        $('#errorAlert').text(data.endText).show();
				$('#successAlert').hide();
        $('#step2').fadeOut();
        $('#step3').fadeIn();
        return false;
      }
			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
        selectedModel = data.selectedModel;
        animalType = data.animalType;
				$('#successAlert').text(selectedModel+" "+animalType).show();
				$('#errorAlert').hide();
			}
		});
    // $(this).fadeOut();
  });

  $('#cat').click(function(){
    $.ajax({
			data : {
				selectedModel : $('#cat').val(),
        animalType : 'cat',
        opponentCat : $('#cat').val(),
			},
			type : 'POST',
			url : '/battlehandler'
		}).done(function(data) {
      if(data.gameover){
        $('#errorAlert').text(data.endText).show();
        $('#successAlert').hide();
        $('#step2').fadeOut();
        $('#step3').fadeIn();
        return false;
      }
			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
        selectedModel = data.selectedModel;
        animalType = data.animalType;
				$('#successAlert').text(selectedModel+" "+animalType).show();
				$('#errorAlert').hide();
			}
		});
    // $(this).fadeOut();
  });

	$('form').on('submit', function(event) {
    $.ajax({
      data: {
        name: $('#name').val(),
      },
      type: 'POST',
      url: '/battle'}).done(function(data){
        if(data.gameover){
          $('#errorAlert').fadeOut();
  				$('#successAlert').fadeOut();
          $('#step3').fadeOut();
          $('#battleform').fadeOut();
          $('#instructions').fadeOut();
          $('#thanks').fadeIn();
          return false;
        }
      });
  		event.preventDefault();
    });
	});
