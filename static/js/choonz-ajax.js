$(document).ready(function(){
	$('#like_btn').click(function(){
		var playlistIdVar
		playlistIdVar = $(this).attr('data-playlistid');

		// url of get request
		// then parameters
		// then anonymous function to handle returned data
		$.get('/choonz/like_playlist/', {'playlist_id': playlistIdVar}, function(data){
			$('#like_count').html(data);
			$('#like_btn').hide();
		})
	})

	$('#tags-input').keyup(function() {
		var query;
		query = $(this).val();

		if(query){
			$.get('/choonz/suggest/', {'suggestion': query}, function(data){
				$('#tag-listing').html(data);
			})
		} else {
			$('#tag-suggestions').empty();
		}
		
	})

	$('.choonz-page-add').click(function() {
		var playlistid = $(this).attr('data-playlistid');
		var title = $(this).attr('data-title');
		var url = $(this).attr('data-url');
		var clickedButton = $(this);

		$.get('/choonz/search_add_page/', {'playlist_id': playlistid, 'title': title, 'url': url}, function(data){
			$('#page-listing').html(data);
			clickedButton.hide();
		})

	})
	
})

