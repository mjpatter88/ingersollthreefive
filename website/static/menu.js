jQuery(function($){
  $( '.menu-btn' ).click(function(){
      $('.responsive-menu').toggleClass('expand')
  })
})

jQuery(function($){
  $( '.gallery1' ).click(function(){
      $('.container-slideshow').toggleClass('container-slideshow-expand')
  })
})


$(window).load(function(){
		var pages = $('.container-slideshow li'), current=0;
		var currentPage,nextPage;

		$('.container-slideshow .button').click(function(){
			currentPage= pages.eq(current);
			if($(this).hasClass('prevButton'))
			{

				if (current <= 0)
					current=pages.length-1;
				else
					current=current-1;
			}
			else
			{
				if (current >= pages.length-1)
					current=0;
				else
					current=current+1;
			}
			nextPage = pages.eq(current);	
			currentPage.hide();	
			nextPage.show();		
		});
});
