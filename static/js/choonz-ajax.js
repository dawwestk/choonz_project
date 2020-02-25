// stopping caching while developing
$.ajaxSetup({
    cache: false
});

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

	$('#tag-search-input').keyup(function() {
		var query;
		query = $(this).val();

		if(query){
			$.get('/choonz/suggest/', {'suggestion': query}, function(data){
				$('#tag-listing').html(data);
			})
		}//else {
		//	$('#tag-suggestion-list').empty();
		//}
		// ^ Else only needed if we move from vertical list layout of tag suggestions
		
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

// separated from document.ready as the tag-suggestions are added/updated AFTER the DOM model is created
$(document).on("click", ".tag-suggestion", function(e) {
	var currentTags = $('#tags').val();
	var clickedTag = $(this).text();

	// Check if tag already on the list
	if (currentTags.includes(clickedTag)) {
		// Already featured
		//alert("Cannot add tags more than one");
		output = currentTags.replace(clickedTag + ', ', '');
		$('#tags').val(output);
	} else {
		var output = currentTags + clickedTag + ', ';
		$('#tags').val(output);
	}
})

