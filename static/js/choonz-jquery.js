 $(document).ready( function () {
  			showPlaylistView();
		});
 
$(document).ready(function(){
	$('#about-btn').click(function(){
		msgStr = $('#msg').html();
		msgStr = msgStr + " ooo, fancy!";
		$('#msg').html(msgStr);
	})
})

/*
$('p').hover(
	function() {
		$(this).css('color', 'blue');
	},
	function() {
		$(this).css('color', 'black');
});
*/

// Profile Views
function showPlaylistView() {
	$('#rated-playlists-view').hide();
	$('#edit-profile-view').hide();
	$('#playlist-view').show();
}

function showRatedPlaylistsView() {
	$('#playlist-view').hide();
	$('#edit-profile-view').hide();
	$('#rated-playlists-view').show();
}

function showEditProfileView() {
	$('#playlist-view').hide();
	$('#rated-playlists-view').hide();
	$('#edit-profile-view').show();
}

function createNewPlaylistView() {
	window.location.href = "choonz/add_playlist/";
}


