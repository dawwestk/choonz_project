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
			if(data.status){
				$('#add_song_title').val("");
				$('#add_song_artist').val("");
				$('#add_song_spotify_link').val("");
				$('#add_song_other_link').val("");
				showAddSongPopUp(data.message);
			} else {
				alert(data.message);
			}
		})
	})

	$('#edit_playlist_save_changes').click(function(){
		var playlistSlug
		playlistSlug = $(this).attr('data-playlistSlug');
		var playlist_name
		playlist_name = $('#edit_name').val();
		var playlist_description
		playlist_description = $('#edit_description').val();
		var playlist_tags
		playlist_tags = $('#tags').val();

		$.post('', {'playlist_slug': playlistSlug, 'playlist_name': playlist_name, 'playlist_description': playlist_description, 'playlist_tags': playlist_tags}, function(data){
			if(data.status){
				showAddSongPopUp(data.message);
			} else {
				alert(data.message);
			}
		})

	})

	$('#tag-search-input').keyup(function() {
		var query;
		query = $(this).val();

		if(query){
			$.get('/choonz/suggest_tag/', {'suggestion': query}, function(data){
				$('#tag-listing').html(data);
			})
		}
	})

	$('#playlist-search-input').keyup(function() {
		var query;
		query = $(this).val();
		$('#playlist-listing').css('display', 'inline-block');

		if(query){
			$.get('/choonz/suggest_playlist/', {'suggestion': query}, function(data){
				$('#playlist-listing').html(data);
			})
		} else {
			$('#playlist-listing').css('display', 'none');
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
	var tagInput = $('#tags');
	var currentTags = tagInput.val();
	var clickedTag = $(this).text();

	// Check if tag already on the list
	if (currentTags.includes(clickedTag)) {
		// Already featured
		//alert("Cannot add tags more than one");
		output = currentTags.replace(clickedTag + ', ', '');
		tagInput.val(output);
	} else {
		var output = currentTags + clickedTag + ', ';
		tagInput.val(output);
	}
})

$(document).on("click", '#remove-song-btn', function(e){
	var parentLI = $(this).parent();
	var buttonToHide = $(this);
	var playlistSlug
	playlistSlug = $(this).attr('data-playlistSlug');
	var songSlug
	songSlug = $(this).attr('data-songSlug');

	var confirmation = false;
	if (confirm("Are you sure you want to remove this song?")) {
		confirmation = true;
		$.post('remove_song/', {'playlist_slug': playlistSlug, 'song_slug': songSlug, 'confirmed': confirmation}, function(data){
			if(data.status){
				showAddSongPopUp(data.message);
				parentLI.css('text-decoration', 'line-through');
				buttonToHide.hide();
			} else {
				alert(data.message);
			}
		})
	} else {
		confirmation = false;
	    return 0;
	}

})

function showAddSongPopUp(text) {
  // Get the snackbar DIV
  var x = document.getElementById("addSongPopUp");
  x.innerHTML = text;

  // Add the "show" class to DIV
  x.className = "show";

  // After 3 seconds, remove the show class from DIV
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
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

