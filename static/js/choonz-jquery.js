$(document).ready( function () {
  	showPlaylistView();

	$('#about-btn').click(function(){
		msgStr = $('#msg').html();
		msgStr = msgStr + " ooo, fancy!";
		$('#msg').html(msgStr);
	})


})

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
    ctx.css('display', 'block');
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
    ctx.css('display', 'block');
}
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

