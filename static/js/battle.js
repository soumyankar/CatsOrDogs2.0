$(document).ready(function() {
  // This is for choosing a dog
  $(function(){
    $('input[type="radio"]').click(function(){
        if ($(this).is(':checked'))
        {
            if(confirm('Confirm pick?')){
              $.ajax({
                data: {
                  selectedModel: $(this).val(),
                  animalType: 'null',
                },
                type: 'POST',
                url : '/battlesetup'
              }).done(function(data){
                if(data.error){
                  $('#errorAlert').text(data.error).show();
          				$('#successAlert').hide();
                }
                else{
                  catID = data.catID;
                  catName = data.catName;
                  catBreed = data.catBreed;
                  catWeblink = data.catWeblink;
                  dogID = data.dogID;
                  dogName = data.dogName;
                  dogBreed = data.dogBreed;
                  dogWeblink = data.dogWeblink;
          				$('#step2').fadeOut();
                  $('#step3').fadeIn();
                  $('#dog').val(dogID);
                  $('#cat').val(catID);
                  $('#dog-name').html(dogName).show();
                  $('#dog-breed').html(dogBreed).show();
                  $('#dog-picture').attr('src',dogWeblink).show();
                  $('#cat-name').html(catName).show();
                  $('#cat-breed').html(catBreed).show();
                  $('#cat-picture').attr('src',catWeblink).show();
                }
              });
          }
        }
      });
    });
  $('#dog').click(function(){
    // This is when the dog is chosen over the cat.
    $('#successAlert').text("You liked "+$('#dog-name').html()+" over "+$('#cat-name').html()).show();
    $('#errorAlert').hide();
    $('#cat-picture').fadeOut();
    $.ajax({
			data : {
				selectedModel : $('#dog').val(),
        animalType : 'dog',
        opponentCat : $('#cat').val(),
			},
			type : 'POST',
			url : '/battlesetup'
		}).done(function(data) {
      if(data.gameover){
        $('#errorAlert').text(data.endText).show();
				$('#successAlert').hide();
        $('#step3').fadeOut();
        $('#instructions').fadeOut();
        $('#thanks').fadeIn();
        return false;
      }
			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
        catID = data.catID;
        catName = data.catName;
        catBreed = data.catBreed;
        catWeblink = data.catWeblink;
        dogID = data.dogID;
        dogName = data.dogName;
        dogBreed = data.dogBreed;
        dogWeblink = data.dogWeblink;
        $('#cat').val(catID);
        $('#cat-name').html(catName).show();
        $('#cat-breed').html(catBreed).show();
        $('#cat-picture').attr('src',catWeblink).fadeIn();
			}
		});
    // $(this).fadeOut();
  });

  $('#cat').click(function(){
    // This function is for when cat is selected
    $('#successAlert').text("You liked "+$('#cat-name').html()+" over "+$('#dog-name').html()).show();
    $('#errorAlert').hide();
    $('#cat-picture').fadeOut();
    $.ajax({
			data : {
				selectedModel : $('#dog').val(),
        animalType : 'cat',
        opponentCat : $('#cat').val(),
			},
			type : 'POST',
			url : '/battlesetup'
		}).done(function(data) {
      if(data.gameover){
        $('#errorAlert').text(data.endText).show();
        $('#successAlert').fadeOut();
        $('#step3').fadeOut();
        $('#instructions').fadeOut();
        $('#thanks').fadeIn();
        return false;
      }
			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
        catID = data.catID;
        catName = data.catName;
        catBreed = data.catBreed;
        catWeblink = data.catWeblink;
        dogID = data.dogID;
        dogName = data.dogName;
        dogBreed = data.dogBreed;
        dogWeblink = data.dogWeblink;
        $('#cat').val(catID);
        $('#cat-name').html(catName).show();
        $('#cat-breed').html(catBreed).show();
        $('#cat-picture').attr('src',catWeblink).fadeIn();
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
      url: '/commitlabrat' // fix this1
    }).done(function(data){
        if(data.labrat){
          console.log("Today's labrat = "+data.labrat);
          $('#step1').fadeOut();
          $('#step2').fadeIn();
          return false;
        }
      });
  		event.preventDefault();
    });
	});
