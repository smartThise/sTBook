$(document).ready(init);

MathJax.Hub.Config({
	tex2jax: {
		inlineMath: [ ['$','$'], ["\\(","\\)"] ],
		displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
		processEscapes: true,
		processEnvironments: true
	},
	// Center justify equations in code and markdown cells. Elsewhere
	// we use CSS to left justify single line equations in code cells.
	displayAlign: 'center',
	"HTML-CSS": {
		styles: {'.MathJax_Display': {"margin": 0}},
		linebreaks: { automatic: true }
	}
});

function init()
{
	checkLogin();
	initComponents();
	setupUI();
}

function checkLogin()
{
	$.post(
		"user.php",
		{
			"action" : "checklogin"
		},
		function(data)
		{
			var islogin = eval(data)["islogin"];
			if (!islogin) {
				top.location="index.shtml";
			}
		}
	);
}

function setupUI()
{
	var problemId = getQueryStringRegExp("id");
	if (problemId == "") {
		top.location="index.shtml";
		return;
	}
	$.post(
		"problem.php",
		{
			"action" : "text",
			"problem_id" : problemId
		},
		function(data)
		{
			var json_data = eval(data);
			if (json_data["error"] == 0) {
				$("#problemName").text(json_data["name"]);
				$("#problemText").append($(json_data["text"]));
				MathJax.Hub.Typeset($("#problemText")[0]);
				if (!json_data["legacy"]) hljs.highlightAll();
				// $("#problemSubmitButton").click(function() {
				// 	SubmitPanel.show(problemId, json_data["name"]);
				// });
			}
		}
	);

}

function initComponents()
{
	NavBar.init();
	// SubmitPanel.init();
	Nav.init([{"name" : "My Courses"}]);
}


function getQueryStringRegExp(name)
{
	var reg = new RegExp("(^|\\?|&)"+ name +"=([^&]*)(\\s|&|$)", "i");
	if (reg.test(location.href)) return unescape(RegExp.$2.replace(/\+/g, " ")); return "";
};
