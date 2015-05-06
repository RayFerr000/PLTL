jQuery(document).ready(function ($) {

	/* Use this js doc for all application specific JS */
	/* intiate calender 
	$("#id_pub_date").fdatepicker();
	$("#id_due_date").fdatepicker({ format: 'yyyy-mm-dd'}).fdatepicker("setDate", new Date()+7);  
*/
 	console.log("before");
     
     var urlchunks = window.location.href.split('/');
     var classid = urlchunks[urlchunks.length - 2];
     var apiPath = "/User/Class/api/getAssignmentList/"+classid;

 $.ajax({
   url: apiPath,
   
   method: "GET"
 }).done(function(response) {
  console.log(classid+"-------------"+response);
  $("#assignmentListDetails").dataTable({
   "aaData": response,
   "aoColumns": [{
  "mData":"due_date",
  "sTitle": "Due Date"
   },  
   
   {
  "mData":"assignment_name",
  "sTitle": "Assignment Name"
   },
   {
  "mData": "assignmentfile",
  "mRender": function ( url, type, full )  {
    return "<a href='#' onclick='window.open(\"/"+url+"\")'>"+url+"</a></li>";
  },
  "sTitle": "Assignment File"
   },{
  "mData": "pub_date",
  "sTitle": "Publish Date"
   }]
 });
 });

    console.log("after");
	/* TABS --------------------------------- */
	/* Remove if you don't need :) */

	function activateTab($tab) {
		var $activeTab = $tab.closest('dl').find('a.active'),
				contentLocation = $tab.attr("href") + 'Tab';
				
		// Strip off the current url that IE adds
		contentLocation = contentLocation.replace(/^.+#/, '#');

		//Make Tab Active
		$activeTab.removeClass('active');
		$tab.addClass('active');

    //Show Tab Content
		$(contentLocation).closest('.tabs-content').children('li').hide();
		$(contentLocation).css('display', 'block');
	}

  $('dl.tabs dd a').on('click', function (event) {
    activateTab($(this));
  });

	if (window.location.hash) {
		activateTab($('a[href="' + window.location.hash + '"]'));
		//$.foundation.customForms.appendCustomMarkup();
	}

	/* ALERT BOXES ------------ */
	$(".alert-box").delegate("a.close", "click", function(event) {
    event.preventDefault();
	  $(this).closest(".alert-box").fadeOut(function(event){
	    $(this).remove();
	  });
	});


	
  /*  var currentDate = new Date();
    $('#id_due_date').fdatepicker({
        inline: true,
        showOtherMonths: true,
        dayNamesMin: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
        dateFormat: "yy-mm-dd"
    });
    
    $("#id_due_date").fdatepicker("setDate", currentDate); */


	/* DROPDOWN NAV ------------- */

	var lockNavBar = false;
	$('.nav-bar a.flyout-toggle').on('click', function(e) {
		e.preventDefault();
		var flyout = $(this).siblings('.flyout');
		if (lockNavBar === false) {
			$('.nav-bar .flyout').not(flyout).slideUp(500);
			flyout.slideToggle(500, function(){
				lockNavBar = false;
			});
		}
		lockNavBar = true;
	});
  if (!Modernizr.touch) {
    $('.nav-bar>li.has-flyout').hover(function() {
      $(this).children('.flyout').show();
    }, function() {
      $(this).children('.flyout').hide();
    })
  }


  
  
});
