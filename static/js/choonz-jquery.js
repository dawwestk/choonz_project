$(document).ready( function () {
  	//showPlaylistView();
});
 
$(document).ready(function(){
	$('#about-btn').click(function(){
		msgStr = $('#msg').html();
		msgStr = msgStr + " ooo, fancy!";
		$('#msg').html(msgStr);
	})



})

function loadChart(label_info, rating_info){
	var playlist_names = label_info;
	var playlist_ratings = rating_info;

    var ctx = $("#playlist-rating-bar-chart").get(0).getContext("2d");
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
        	labels: playlist_names,
        	datasets: [{
        		label: "Playlist Rating",
            	data: playlist_ratings,
            	backgroundColor: [
	                'rgba(255, 99, 132, 0.2)',
	                'rgba(54, 162, 235, 0.2)',
	                'rgba(255, 206, 86, 0.2)',
	                'rgba(75, 192, 192, 0.2)'
	                ],
        		}
        	]
        },
        options:{
        	responsive: false,
        	scales: {
	            yAxes: [{
	                ticks: {
	                	min:0.0,
	                	max:5.0,
	                    beginAtZero: true
	                }
	            }]
	        }
        }
    });
};
	/*
	var ctx = $('#playlist-rating-bar-chart');
	var myChart = new Chart(ctx, {
	    type: 'bar',
	    data: {
	        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
	        datasets: [{
	            label: '# of Votes',
	            data: [12, 19, 3, 5, 2, 3],
	            backgroundColor: [
	                'rgba(255, 99, 132, 0.2)',
	                'rgba(54, 162, 235, 0.2)',
	                'rgba(255, 206, 86, 0.2)',
	                'rgba(75, 192, 192, 0.2)',
	                'rgba(153, 102, 255, 0.2)',
	                'rgba(255, 159, 64, 0.2)'
	            ],
	            borderColor: [
	                'rgba(255, 99, 132, 1)',
	                'rgba(54, 162, 235, 1)',
	                'rgba(255, 206, 86, 1)',
	                'rgba(75, 192, 192, 1)',
	                'rgba(153, 102, 255, 1)',
	                'rgba(255, 159, 64, 1)'
	            ],
	            borderWidth: 1
	        }]
	    },
	    options: {
	    	responsive: false,
	        scales: {
	            yAxes: [{
	                ticks: {
	                    beginAtZero: true
	                }
	            }]
	        }
	    }
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

