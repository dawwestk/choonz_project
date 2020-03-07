$(document).ready( function () {
	var url = 'choonz/';
	if (window.location.href.indexOf(url + "profile/") > -1) {
    	showPlaylistView();
    }
    if(window.location.href.indexOf("my") > -1){
    	loadMyStatsPage();
    }

	$('#about-btn').click(function(){
		msgStr = $('#msg').html();
		msgStr = msgStr + " ooo, fancy!";
		$('#msg').html(msgStr);
	})


	// Profile View Buttons
	$('#view-playlists-button').click(function(){
		showPlaylistView();
	})
	$('#view-rated-playlists-button').click(function(){
		showRatedPlaylistsView();
	})
	$('#edit-profile-button').click(function(){
		showEditProfileView();
	})

	// My Stats Buttons
	$('#view-tables-button').click(function(){
		loadMyStatsPage();
	})
		
})

function loadCharts(bar_label_info, bar_data, bar_average, line_date_info, line_data, line_names){
	loadRatingChart(bar_label_info, bar_data, bar_average);
	loadUserChart(line_date_info, line_data, line_names);
	showChartsView();
}

function loadRatingChart(label_info, rating_info, average_rating){
	//alert(label_info);
	//alert(rating_info);
	//alert(average_rating);
	
	var playlist_names = label_info;
	var playlist_ratings = rating_info;
	var num_ratings = rating_info.length;
	
	var ave_line = [];
	var i;
	for(i = 0; i < num_ratings; i++){
		ave_line[i] = average_rating;
	}
	
    var ctx = $("#playlist-rating-bar-chart").get(0).getContext("2d");
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
        	datasets: [{
        		label: "Playlist Rating",
            	data: playlist_ratings,
            	backgroundColor: [
	                'rgba(255, 99, 132, 0.2)',
	                'rgba(54, 162, 235, 0.2)',
	                'rgba(255, 206, 86, 0.2)',
	                'rgba(75, 192, 192, 0.2)'
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
        		},
        		{
        			label: "Average Rating",
        			data: ave_line,
        			type: 'line',
        			fill: false,
        			borderColor: ['rgba(54, 162, 235, 1)'],
        			borderDash: [20, 5]
        		}
        	],
        	labels: playlist_names
        },
        options:{
        	responsive: false,
        	scales: {
	            yAxes: [{
	                	ticks: {
	                	min:0.0,
	                	max:5.0,
	                    beginAtZero: true,
	                	},
	                	scaleLabel: {
					        display: true,
					        labelString: 'Stars Rating'
					    }
	           		}],
	           	xAxes: [{
	           		scaleLabel: {
				        display: true,
				        labelString: 'Playlist Name'
				    }
	           	}]
	        }
        }
    });
}

function loadUserChart(date_info, rating_info, name_info){
	var rating_dates = date_info;
	var playlist_ratings = rating_info;
	var playlist_names = name_info;
	
    var ctx = $("#user-line-chart").get(0).getContext("2d");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
        	datasets: [{
        			label: "User Ratings Over Time",
        			data: playlist_ratings,
        			type: 'line',
        			fill: false,
        			borderColor: ['rgba(54, 162, 235, 1)'],
        			borderDash: [20, 5]
        		}
        	],
        	labels: rating_dates
        },
        options:{
        	responsive: false,
        	scales: {
	            yAxes: [{
	                	ticks: {
	                	min:0.0,
	                	max:5.0,
	                    beginAtZero: true,
	                	},
	                	scaleLabel: {
					        display: true,
					        labelString: 'Stars Rating'
					    }
	           		}],
	           	xAxes: [{
	           		scaleLabel: {
				        display: true,
				        labelString: 'User Activity'
				    }
	           	}]
	        },
	        tooltips: {
	        	callbacks: {
		            title: function(tooltipItem, data) {
			          return data['labels'][tooltipItem[0]['index']];
			        },
			        label: function(tooltipItem, data) {
			          return playlist_names[tooltipItem['index']] + " - " + data['datasets'][0]['data'][tooltipItem['index']];
			        },
	        	}
	        }
        }
    });
}

// MyStats Views
function loadMyStatsPage() {
	$('#chart-view').hide();
	$('#table-view').show();
}

function showChartsView(){
	$('#chart-view').show();
	$('#table-view').hide();
}

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

