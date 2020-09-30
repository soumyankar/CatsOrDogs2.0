function validate() {

   if( document.inputform.name.value == "" ) {
      alert( "Please provide Animal's name!" );
      document.myForm.name.focus() ;
      return false;
   }
   if( document.inputform.breed.value == "" ) {
      alert( "Please provide Animal's Breed!" );
      document.inputform.breed.focus() ;
      return false;
   }
   if( document.inputform.rating.value == "" ) {
      alert( "Please provide a rating" );
   document.inputform.rating.focus() ;
   return false;
   }
   if( document.inputform.weblink.value == "" ) {
      alert( "Please provide a weblink for the image" );
   document.inputform.weblink.focus() ;
   return false;
   }
   if( document.inputform.animaltype.value == "-1" ) {
   alert( "Please provide animal type!" );
   return false;
}
return( true );
}
