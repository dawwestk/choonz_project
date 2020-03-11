// stopping caching while developing
$.ajaxSetup({
    cache: false
});

$(document).ready(function(){

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
				$('#edit-song-list').append(generateNewSongListingForEditPage(data.new_slug, song_title, song_artist, playlistSlug));
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

		if(!query){
			query = '*';	// display all tags again
		}
		$.get('/choonz/suggest_tag/', {'suggestion': query}, function(data){
			$('#tag-listing').html(data);
		})
	})

	$('#playlist-search-input').keyup(function() {
		var query = $(this).val();
		$.get('/choonz/suggest_playlist/', {'suggestion': query}, function(data){
			$('#playlist-listing').html(data);
		})
	})

	$('#spotify-add-song-search').click(function(){
		var query = $('#spotify-search-query').val();
		var playlistSlug = $(this).attr('data-playlistSlug');
		$.post('/choonz/search_spotify/', {'query': query}, function(data){
			
			for(var i = 0; i < data.results.length; i++) {
				$('#spotify-search-results').append(generateSpotifySearchResultForEditPage(data.results[i].track_name, data.results[i].artist_name, data.results[i].link, data.results[i].album_image, playlistSlug));
			};
		})
	})

	$('#spotify-search-query').keydown(function(e){
		if (e.which == 13) {
			$('#spotify-add-song-search').click();
		}
	})

	$('#filter-button').click(function() {
		var tags = $('#tags').val();
		var creator = $('#creator').val();
		var createdDate = $('#created-date').val();
		$.get('/choonz/filter_playlists/', {'tags': tags, 'creator': creator, 'createdDate': createdDate}, function(data){
			$('#playlist-listing').html(data);
		})
	})

	$('#remove-filter-button').click(function() {
		$('#tags').val('');
		$('#creator').val('');
		$('#created-date').val('');
		$.get('/choonz/filter_playlists/', {'tags': '', 'creator': '', 'createdDate': ''}, function(data){
			$('#playlist-listing').html(data);
		})
	})

	$('#delete-playlist-button').click(function(){
		var buttons = $('#playlist-delete-buttons');
		if(buttons.css('display', 'none')){
			buttons.css('display', 'inline-block');
		}
	})

	$('#cancel-delete-playlist').click(function(){
		var buttons = $('#playlist-delete-buttons');
		buttons.css('display', 'none');
	})
	
})

// separated from document.ready as the tag-suggestions are added/updated AFTER the DOM model is created
$(document).on("click", ".tag-suggestion", function(e) {
	var clickedTag = $(this).text();
	addTagToList(clickedTag);
})

$(document).on("click", '#add-new-tag', function(e){
	var tagText = $('#tag-search-input').val();
	if(!(tagText == '')){
		$.post('/choonz/suggest_tag/', {'tag_text': tagText}, function(data){
			if(data.status){
				$('#tag-search-input').val("");
				showAddSongPopUp(data.message);
				addTagToList(tagText);
			} else {
				showAddSongPopUp(data.message);
			}
		})
	} else {
		showAddSongPopUp("Invalid create-tag string");
	} 
})

function addTagToList(tagToInsert){
	var clickedTag = tagToInsert;
	var tagInput = $('#tags');
	var currentTags = tagInput.val();

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
}

$(document).on("keydown", '.add-url-to-song', function(e){
	if (e.which == 13) {
	    var url_type = $(this).attr('data-urlType');
	    var song_slug = $(this).attr('data-songSlug');
	    var url = $(this).val();
	    var linkToSpotify = null;
	    var linkOther = null;
	    if(url_type == "spotify"){
	    	linkToSpotify = url;
	    	linkOther = '';
	    } else if(url_type == "other"){
	    	linkOther = url;
	    	linkToSpotify = '';
	    }
	    //alert("calling get with linkToSpotify = " + linkToSpotify + "\nlinkOther = " + linkOther + "\nsong slug = " + song_slug);

	    $.get('add_song/', {'song_slug': song_slug, 'link_to_spotify': linkToSpotify, 'link_other': linkOther}, function(data){
	    })
	}
})

$(document).on("focusin", '.add-url-to-song', function(e){
	if($(this).val() == "~ insert here ~"){
		$(this).val("");
	}
})

$(document).on("focusout", '.add-url-to-song', function(e){
	if($(this).val() == ""){
		$(this).val("~ insert here ~");
	}
})

$(document).on("click", '.remove-song-button', function(e){
	var slug = $(this).attr('data-songSlug');
	var parentLI = $('#' + slug)
	var confirmButton = $('#confirm-remove-' + slug);
	confirmButton.css('display', 'inline-block');
	var cancelButton = $('#cancel-remove-' + slug);
	cancelButton.css('display', 'inline-block');
	$(this).css('display', 'none');
	
})

$(document).on("click", '.cancel-song-remove', function(e){
	var slug = $(this).attr('data-songSlug');
	$(this).css('display', 'none');
	var parentLI = $('#' + slug)
	var removeButton = $('#remove-song-' + slug);
	removeButton.css('display', 'inline-block');
	var confirmButton = $('#confirm-remove-' + slug);
	confirmButton.css('display', 'none');
	
})

$(document).on("click", '.confirm-song-remove', function(e){
	var slug = $(this).attr('data-songSlug');
	var parentLI = $('#' + slug)
	var titleAndArtist = $('.title-and-artist-' + slug);
	var confirmButton = $(this);
	var cancelButton = $('#cancel-remove-' + slug);
	var playlistSlug = $(this).attr('data-playlistSlug');
	var songSlug = $(this).attr('data-songSlug');
	var undoButton = $('#undo-remove-' + slug);

	$.post('remove_song/', {'playlist_slug': playlistSlug, 'song_slug': songSlug, 'confirmed': true}, function(data){
		if(data.status){
			showAddSongPopUp(data.message);
			titleAndArtist.css('text-decoration', 'line-through');
			confirmButton.hide();
			cancelButton.hide();
			undoButton.show();

		} else {
			alert(data.message);
		}
	})

})

$(document).on("click", '.undo-song-remove', function(e){
	var slug = $(this).attr('data-songSlug');
	var parentLI = $('#' + slug)
	var titleAndArtist = $('.title-and-artist-' + slug);
	var playlistSlug = $(this).attr('data-playlistSlug');
	var song_title = $(this).attr('data-songTitle');
	var song_artist = $(this).attr('data-artistName');
	var link_to_spotify = $(this).attr('data-linkToSpotify');
	var link_other = $(this).attr('data-linkOther');

	var removeButton = $('#remove-song-' + slug);
	removeButton.css('display', 'inline-block');

	$.post('add_song/', {'playlist_slug': playlistSlug, 'song_title': song_title, 'song_artist': song_artist, 'link_to_spotify': link_to_spotify, 'link_other': link_other}, function(data){
		if(data.status){
			$('#add_song_title').val("");
			$('#add_song_artist').val("");
			$('#add_song_spotify_link').val("");
			$('#add_song_other_link').val("");
			titleAndArtist.css('text-decoration', 'none');
			showAddSongPopUp(data.message);
		} else {
			alert(data.message);
		}
	})
	$(this).css('display', 'none');
})

$(document).on("click", '.add-from-spotify', function(e){
	var song_title = $(this).attr('data-songTitle');
	var song_artist = $(this).attr('data-artistName');
	var link_to_spotify = $(this).attr('data-linkToSpotify');
	var playlistSlug = $(this).attr('data-playlistSlug');
	var link_other = null;
	$(this).css('display', 'none');

	$.post('add_song/', {'playlist_slug': playlistSlug, 'song_title': song_title, 'song_artist': song_artist, 'link_to_spotify': link_to_spotify, 'link_other': link_other}, function(data){
		if(data.status){
			$('#edit-song-list').append(generateNewSongListingForEditPage(data.new_slug, song_title, song_artist, playlistSlug, link_to_spotify, link_other));
			showAddSongPopUp(data.message);
			$(this).css('display', 'none');
		} else {
			alert(data.message);
		}
	})
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

function generateSpotifySearchResultForEditPage(track_name, artist_name, link, track_album_image, playlistSlug){
	//alert(link);
	var search_result_html = `
		<li class="choonz-list-group-item">
			<div class="choonz-row-border">
				<div class="col-md-6">
					<span><strong>${track_name}</strong> by ${artist_name}</span>
				</div>
				<div class="col-md-3">
					<a href="${link}">Listen on Spotify</a>
					<img width=30 height=30 src="${track_album_image}"/>
				</div>
				<div class="col-md-3">
					<a class="btn btn-info add-from-spotify" data-songTitle="${track_name}" data-artistName="${artist_name}" data-linkToSpotify="${link}" data-playlistSlug=${playlistSlug}>Add to Playlist</a>
				</div>
			</div>
		</li>`
    
    return search_result_html;
}

function generateNewSongListingForEditPage(slug, title, artist, playlistSlug, link_spotify, link_other){
	
	var new_song_html = `
	  <li class="choonz-row choonz-vertical-center" id="${slug}">
	<div class="col-md-9 title-and-artist-${slug}">
		<div class="row">
			<div class="col-md-6">
				<h5 class="centred-left-indent-5">${title}</h5>
			</div>
			<div class="col choonz-vertical-center">
				<strong>Spotify URL </strong>`;
	
	if(link_spotify){
		var first_input = `<input class="choonz-form-control add-url-to-song" data-urlType="spotify" data-songSlug="${slug}" data-playlistSlug="${playlistSlug}" type="text" value="${link_spotify}" />`;
	} else {
		var first_input = `<input class="choonz-form-control add-url-to-song" data-urlType="spotify" data-songSlug="${slug}" data-playlistSlug="${playlistSlug}" type="text" value="~ insert here ~" />`;
	}

	var middle = `</div>
		</div>
		<div class="row">
			<div class="col-md-6">
				<span class="centred-left-indent-10">by ${artist}</span>
			</div>
			<div class="col choonz-vertical-center">
				<strong>Other Link : </strong>`;

    if(link_other){
    	var second_input = `<input class="choonz-form-control add-url-to-song" data-urlType="other" data-songSlug="${slug}" data-playlistSlug="${playlistSlug}" type="text" value="${link_other}" />`;
    } else {
    	var second_input = `<input class="choonz-form-control add-url-to-song" data-urlType="other" data-songSlug="${slug}" data-playlistSlug="${playlistSlug}" type="text" value="~ insert here ~" />`;
    }
                
	var end = `  
                </div>
		</div>
	</div>
	<div class="col-md-3 choonz-vertical-center">
		<div class="choonz-col">
			<button class="btn btn-danger remove-song-button" type="button" id="remove-song-${slug}" data-songSlug="${slug}">Remove</button>
			<button class="btn btn-danger confirm-song-remove" type="button" id="confirm-remove-${slug}" data-songSlug="${slug}" data-playlistSlug="${playlistSlug}">Confirm</button>
			<button class="btn btn-secondary cancel-song-remove" type="button" id="cancel-remove-${slug}" data-songSlug="${slug}" data-playlistSlug="${playlistSlug}">Cancel</button>
			<button class="btn btn-secondary undo-song-remove" type="button" id="undo-remove-${slug}" data-songSlug="${slug}" data-songTitle="${title}" data-artistName="${artist}" data-linkToSpotify="${link_spotify}" data-linkOther="${link_other}" data-playlistSlug="${playlistSlug}">Undo Song Remove</button>
		</div>
	</div>
</li>
	`;
	var full = new_song_html + first_input + middle + second_input + end;
	return full;
}


/*

	Helper methods used to verify POST requests using CSRF token

*/

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

