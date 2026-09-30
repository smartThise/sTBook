var Nav = (function($) {
	var my = {};
	var path;

	function updateUI()
	{
		var body = $("#navPanel").find(".breadcrumb");
		body.empty();
		for (var i = 0; i < path.length - 1; i++) {
			body.append($("<li><a href=\"" + path[i]["href"] + "\">" + path[i]["name"] + "</a></li>"));
		}
		if (path.length > 0)
			body.append($("<li class=\"active\">" + path[path.length - 1]["name"] + "</li>"));
	}

	my.init = function(data)
	{
		path = data;
		updateUI();
	}

	my.goBack = function()
	{
		path.pop();
		updateUI();
	}

	my.GoForward = function(name, href)
	{
		var newNode = [];
		newNode["name"] = name;
		newNode["href"] = href;
		path.push(newNode);
		updateUI();
	}

	return my;

}) (jQuery);
