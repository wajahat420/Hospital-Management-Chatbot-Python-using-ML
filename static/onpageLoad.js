function pageLoad(){
	html = 
	`
	<div class="col-md-12 p-0">
	<h4 onclick="showDetails(1)"><i class="fa fa-angle-down" style="font-size:24px;color: white;padding: 2px;"></i> Greeting</h4>
	<ul class="d-none" id="h4-1">
		<li>Greet</li>
		<li>Asking name</li>
	</ul>
	<h4 onclick="showDetails(1)"><i class="fa fa-angle-down" style="font-size:24px;color: white;padding: 2px;"></i> Appointments</h4>
		<ul class="d-none" id="h4-1">
			<li>Ask about available Doctor</li>
			<li>Timing of Doctors</li>
		</ul>
	<h4 onclick="showDetails(2)"><i class="fa fa-angle-down" style="font-size:24px;color: white;padding-right: 10px;"></i>Doctor</h4>
		<ul class="d-none" id="h4-2">
			<li>Take Multiple Appointments</li>
			<li>Reject Appointment</li>
		</ul>
	
	<h4 onclick="showDetails(3)"><i class="fa fa-angle-down" style="font-size:24px;color: white;padding-right: 10px;"></i>Lab Details</h4>
		<ul class="d-none" id="h4-3">
			<li>Take Multiple Appointments</li>
			<li>Reject Appointment</li>
		</ul>
	</div>
	<h4 onclick="showDetails(1)"><i class="fa fa-angle-down" style="font-size:24px;color: white;padding: 2px;"></i> Meet Patient</h4>
	<ul class="d-none" id="h4-1">
		<li>Ask to meet patient</li>
		<li>People allowed to go inside</li>
		<li>Way towards Room of patient</li>
	</ul>
	<h4 onclick="showDetails(1)"><i class="fa fa-angle-down" style="font-size:24px;color: white;padding: 2px;"></i>Laboratory</h4>
	<ul class="d-none" id="h4-1">
		<li>Opening and Closing</li>
		<li>Tests available</li>
		<li>Report available</li>
	</ul>
	<h4 onclick="showDetails(1)"><i class="fa fa-angle-down" style="font-size:24px;color: white;padding: 2px;"></i>Ending Greeting</h4>
	<ul class="d-none" id="h4-1">
		<li>Ending Greeting</li>
	</ul>

	`
	$(".side-right").append(html);

	html = 
	`
		<ul class="list-group">
			<li  id="home" class="list-group-item active">	<a href="http://localhost:5050/">Home</a></li>
			<li   id="doctors" class="list-group-item">		<a href="http://localhost:5050/doctors">Doctors</a></li >
			<li id="lab" class="list-group-item">		<a href="http://localhost:5050/lab">Laboratory</a></li>
			<li  id="instructions" class="list-group-item">		<a href="http://localhost:5050/instructions">Instructions</a></li>
		</ul>
	`
	$(".side-left").append(html);

}
