jQuery(document).ready(function ($) {

	/* Use this js doc for all application specific JS */
	/* intiate calender 
	$("#id_pub_date").fdatepicker(); */
	$("#id_due_date").fdatepicker({ format: 'yyyy-mm-dd'}).fdatepicker("setDate", new Date()+7);  


     
     var urlchunks = window.location.href.split('/');
     var classid = urlchunks[urlchunks.length - 2];
     var apiPath = "/User/Class/api/getAssignmentList/"+classid;
     
 $.ajax({
   url: apiPath,
   
   method: "GET"
 }).done(function(response) {
  try{
    var $dt =  $("#assignmentListDetails").dataTable({
     "aaData": response,
      "aaSorting": [],
     "draw": 1,
     "columnDefs": [
      { "width": "30%", "targets": 0}, {"sClass": "nameClass", "aTargets": [ 0 ] }
    ],
     "aoColumns": [

    {
    "mData":"assignment_name",  
    "sTitle": "Assignment",
    "mRender": function(data, type, val) { 
          if($('#manage').length == 1 || $('#isPeerLeader').length == 1){
            return'<a href="/Class/Assignment/' +val.assignment_id+'/Grade">' + val.assignment_name + '</a>'
          }
          else                      
            return '<a href="/Homework/' +val.assignment_id+ '">' + val.assignment_name + '</a>';             
      }
     },
    {
    "mData":"due_date",
    "sTitle": "Due Date"
     },
     {
    "mData":"total_grade",
    "sTitle": "Grade"
     }]

   });
  }
  catch(TypeError){
    
  }
 });

 
  


/*
   $('#assignmentListDetails').on( 'click', 'td', function () {
      if($('#assignmentListDetails thead tr th').eq($(this).index()).html().trim() == "Assignment Name"){
        
        var row = $(this).parent().find('td').html().trim();
        //alert(row);
         window.location.href="/Homework/"+row;
      }
    });
*/
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

	
	$(".alert-box").delegate("a.close", "click", function(event) {
    event.preventDefault();
	  $(this).closest(".alert-box").fadeOut(function(event){
	    $(this).remove();
	  });
	});


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
