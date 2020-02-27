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

	$('#add_song_btn').click(function(){
		var playlistSlug
		playlistSlug = $(this).attr('data-playlistSlug');

		var song_title
		var song_artist
		var link_to_spotify
		var link_other
		// song title and artist name cannot be blank
		if($('#add_song_title').val() == ''){
			alert("Song title cannot be blank...");
			return -1;
		} else {
			song_title = $('#add_song_title').val();
		}
		if($('#add_song_artist').val() == ''){
			alert("Artist cannot be blank...");
			return -1;
		} else {
			song_artist = $('#add_song_artist').val();
		}

		// links to spotify/elsewhere can be left blank
		if($('#add_song_spotify_link').val() != ''){
			link_to_spotify = $('#add_song_spotify_link').val();
		}
		if($('#add_song_other_link').val() != ''){
			link_other = $('#add_song_other_link').val();
		}

		// url of get request
		// then parameters
		// then anonymous function to handle returned data
		$.post('add_song/', {'playlist_slug': playlistSlug, 'song_title': song_title, 'song_artist': song_artist, 'link_to_spotify': link_to_spotify, 'link_other': link_other}, function(data){
			if(data >= 0){
				clearAddSongInputs();
				alert("Song added successfully");
			} else {
				alert("Could not add song. Please check the information you have provided and try again.");
			}
		})
	})

	$('#tag-search-input').keyup(function() {
		var query;
		query = $(this).val();

		if(query){
			$.get('/choonz/suggest/', {'suggestion': query}, function(data){
				$('#tag-listing').html(data);
			})
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

function clearAddSongInputs(){
	$('#add_song_title').val("");
	$('#add_song_artist').val("");
	$('#add_song_spotify_link').val("");
	$('#add_song_other_link').val("")
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

