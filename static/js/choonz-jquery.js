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

	// Playlist Page buttons
	$('#show-update-rating-fields').click(function(){
		$('#stars').prop('readonly', false);
		$('#comment').removeAttr('readonly');
		$('#hidden-submit-rating-update').css('display', 'inline-block');
		$('#hidden-cancel-rating-update').css('display', 'inline-block');
		$(this).css('display', 'none');
	})

	$('#hidden-cancel-rating-update').click(function(){
		$(this).css('display', 'none');
		$('#hidden-submit-rating-update').css('display', 'none');
		$('#show-update-rating-fields').css('display', 'inline-block');	
		$('#stars').prop('readonly', true);
		$('#comment').prop('readonly', true);
	})

	// Options for star ratings
	var update = {
	    max_value: 5,
	    step_size: 0.5,
	    initial_value: 0,
	    selected_symbol_type: 'utf8_star', // Must be a key from symbols
	    cursor: 'default',
	    readonly: false,
	    change_once: false, // Determines if the rating can only be set once
	    ajax_method: 'POST',
	}

	var mini_rating = {
	    max_value: 5,
	    step_size: 0.1,
	    initial_value: 0,
	    selected_symbol_type: 'utf8_star', // Must be a key from symbols
	    cursor: 'default',
	    readonly: true,
	    change_once: false, // Determines if the rating can only be set once
	    ajax_method: 'POST',
	}

	$('.rate').rate(update);
	$('.rate').on('change', function(ev, data){
		var stars = $('.rate').rate('getValue');
        $('#stars-input').val(stars);
    });

	$('.min-rating').rate(mini_rating);

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
        			label: "Given Ratings Over Time",
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
	$('#chart-view').css('display', 'none');
	$('#table-view').css('display', 'block');
}

function showChartsView(){
	$('#chart-view').css('display', 'block');
	$('#table-view').css('display', 'none');
}

// Profile Views
function showPlaylistView() {
	$('#rated-playlists-view').css('display', 'none');
	$('#edit-profile-view').css('display', 'none');
	$('#playlist-view').css('display', 'block');
}

function showRatedPlaylistsView() {
	$('#playlist-view').css('display', 'none');
	$('#edit-profile-view').css('display', 'none');
	$('#rated-playlists-view').css('display', 'block');
}

function showEditProfileView() {
	$('#playlist-view').css('display', 'none');
	$('#rated-playlists-view').css('display', 'none');
	$('#edit-profile-view').css('display', 'block');
}

function createNewPlaylistView() {
	window.location.href = "choonz/add_playlist/";
}

