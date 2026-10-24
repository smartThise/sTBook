var NavBar = (function($) {

	var my = {};

	my.init = function()
	{
		setupUI();
	};

	return my;

	function setupUI()
	{
		var first = true;
		$("#navBarMenuLogout").click(logout);
		$("#navBarSelectPrivateCourseModal").find("#okButton").click(selectPrivateCourseSubmit);
		//setupDatePicker($("#navBarCreateCourseModal").find("#inputStartDate"));
		//setupDatePicker($("#navBarCreateCourseModal").find("#inputEndDate"));
		$("#navBarCreateCourseModal").on("shown.bs.modal", function() {
			if (first) {
				$("#navBarCreateCourseModal").find("#inputStartDate").DatePicker( {	
					flat: true,
					date: new Date(),
					calendars: 1,
					starts: 1
				});
				$("#navBarCreateCourseModal").find("#inputEndDate").DatePicker( {	
					flat: true,
					date: new Date(),
					calendars: 1,
					starts: 1
				});
				first = false;
			}
		});
		$("#navBarCreateCourseModal").find("#createButton").click(createCourseSubmit);
		$("#navBarModifyProfileModal").on("show.bs.modal", loadProfileForModify);
		$("#navBarModifyProfileModal").find("#saveButton").click(saveModifiedProfile);
		$("#navBarSelectPublicCourseModal").on("show.bs.modal", loadPublicCourse);
	}

	function logout()
	{
		$.post("user.php", {
			"action" : "logout"
		}, 
		function(data)
		{
			top.location="index.shtml";
		});
	} 

	function selectPrivateCourseSubmit()
	{
		$.post("course.php", {
			"action" : "selectprivatecourse",
			"code": $("#navBarSelectPrivateCourseModal").find("#code").val()
		},
		function(jdata)
		{
			var data = eval(jdata);
			if (data["error"] != 0) {
				alert(data["errorMessage"]);
				return;
			}
			alert("You have successfully selected this course, enjoy it!");
		});
	}

	function createCourseSubmit()
	{
		var modal = $("#navBarCreateCourseModal");
		$.post("course.manage.php", {
			"action" : "createcourse", 
			"name" : modal.find("#inputCourseName").val(),
			"name_in_course" : modal.find("#inputNameInCourse").val(),
			"start_date" : modal.find("#inputStartDate").DatePickerGetDate("Y-m-d"),
			"end_date" : modal.find("#inputEndDate").DatePickerGetDate("Y-m-d"),
			"course_type" : (modal.find("#inputPublicCourse").prop("checked") ? 0 : 1)
		},
		function(jdata)
		{
			var data = eval(jdata);
			if (data["error"] != 0) {
				alert(data["errorMessage"]);
				return;
			}
			alert("Course has been created.");
		});
	
	}

	function loadProfileForModify()
	{
		var modal = $("#navBarModifyProfileModal");
		$.post("user.php", {
			action : "getprofile"
		}, function(jdata) {
			var data = eval(jdata);
			if (data["error"] != 0) {
				alert(data["errorMessage"]);
				return;
			}
			var userProfile = data["userProfile"]
			modal.find("#inputEmail").val(userProfile["email"]);
			modal.find("#inputNickname").val(userProfile["nickname"]);
			modal.find("#inputHideEmail")[0].checked = !!userProfile["hideEmail"];
		});
	}

	function saveModifiedProfile()
	{
		var modal = $("#navBarModifyProfileModal");
		var param = {
			action : "saveprofile",
			nickname : modal.find("#inputNickname").val().trim(),
			hide_email : modal.find("#inputHideEmail").attr("checked") ? 1 : 0,
		};
		var oldPass = modal.find("#inputOldPassword").val();
		var newPass = modal.find("#inputNewPassword").val();
		if ((oldPass == "" && newPass != "") || (oldPass != "" && newPass == "")) {
			alert("You must give both the old password and new password to change your password");
			return false;
		}
		if (oldPass != "") {
			param["old_password"] = oldPass;
			param["new_password"] = newPass;
		}
		$.post("user.php", param, function(jdata) {
			var data = eval(jdata);
			if (data["error"] != 0) {
				alert(data["errorMessage"]);
				return;
			}
			alert("Your profile has been updated.");
		});
	}

	function loadPublicCourse()
	{
		var modal = $("#navBarSelectPublicCourseModal");
		var tbody = modal.find("tbody");
		tbody.empty();
		$.post("course.php", {
			action : "listpubliccourse"
		}, function(jdata) {
			var data = eval(jdata);
			if (data["error"] != 0) {
				alert(data["errorMessage"]);
				return;
			}
			var list = data["courseList"];
			if (list.length > 0) {
				for (var i = 0; i < list.length; i++) {
					var tr = $("<tr/>");
					var td = $("<td><a course-id=\"" + list[i]["id"] + "\" href=\"#\"><span class=\"glyphicon glyphicon-plus\"></span></a></td>");
					td.find("a").click(selectPublicCourse);
					tr.append(td);
					tr.append("<td>" + list[i]["name"] + "</td>");
					tr.append("<td>" + list[i]["ownerName"] + "</td>");
					var startDate = list[i]["startDate"].replace(/-/g, ".");
					var endDate = list[i]["endDate"].replace(/-/g, ".");
					tr.append("<td>" + startDate + "-" + endDate + "</td>");
					tbody.append(tr);
				}
			} else {
				tbody.append("<tr><td colspan=\"4\">No available course.</td></tr>");
			}
		});
	}

	function selectPublicCourse()
	{
		$.post("course.php", {
			action : "selectpubliccourse",
			course_id : $(this).attr("course-id")
		}, function(jdata) {
			var data = eval(jdata);
			if (data["error"] != 0) {
				alert(data["errorMessage"]);
				return;
			}
			alert("You have successfully select this course.");
			self.location.reload();
		});
	}

}) (jQuery);
