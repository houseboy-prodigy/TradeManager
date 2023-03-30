// import express JS module into app
// and creates its variable.
var express = require('express');
var app = express();

// Creates a server which runs on port 3000 and
// can be accessed through localhost:3000
app.listen(3000, function() {
	console.log('server running on port 3000');
} )

app.get('/name', callName);

function callName(req, res) {

	// Use child_process.spawn method from
	// child_process module and assign it
	// to variable spawn
	var spawn = require("child_process").spawn;

	// Parameters passed in spawn -
	// 1. type_of_script
	// 2. list containing Path of the script
	// and arguments for the script

	// E.g : http://localhost:3000/name?curr=Mike&entry=Will
	// so, first name = Mike and last name = Will
	var process = spawn('python',["./function_caller.py",
							req.query.curr,
							req.query.entry,
							req.query.tp,
							req.query.sl,
							req.query.side]);

	console.log('here')
	// Takes stdout data from script which executed
	// with arguments and send this data to res object

	console.log('here2')
	process.stdout.on('data', function(data) {
		res.send(data.toString());
	} )
}

//http://localhost:3000/currStatus?curr=C31
app.get('/currStatus', getPositionStatus);
function getPositionStatus(req, res) {
       // Use child_process.spawn method from
    // child_process module and assign it
    // to variable spawn
    var spawn = require("child_process").spawn;

    // Parameters passed in spawn -
    // 1. type_of_script
    // 2. list containing Path of the script
    // and arguments for the script
    var process = spawn('python3', ["./function_caller.py", "get", req.query.curr]);


    process.stdout.on('data', function(data) {
        console.log('Data received from Python script:', data.toString());
        res.setHeader('Content-Type', 'application/json');
        res.send(data.toString());
    });

    // Add an event listener for stderr data
    process.stderr.on('data', function(data) {
        console.error('Error from Python script:', data.toString());
    });

    process.on('exit', function(code) {
        console.log('Python script exited with code:', code);
    });

    process.on('error', function(err) {
        console.log('Failed to start Python script:', err);
    });
}


//http://localhost:3000/putTrade?curr=Cuu&entry=ava&tp=bfa&sl=afc&side=buy
app.get('/putTrade', function(req, res) {
  // Import the child_process module
  const { spawn } = require('child_process');



  // Spawn a new Python process and pass the arguments
  const pythonProcess = spawn('python', ['./function_caller.py', "put", req.query.curr,req.query.entry, req.query.tp,
  req.query.sl, req.query.side]);

  // Handle the output from the Python process
  pythonProcess.stdout.on('data', (data) => {
    // Convert the JSON string to an object
    const result = JSON.parse(data);
    if (result.status === 'success') {
      // Send the CustomerID value in the response
      res.send(result.CustomerID);
    } else {
      // Send an error response with the error message
      res.status(500).send(result.message);
    }
  });

  // Handle errors from the Python process
  pythonProcess.stderr.on('data', (data) => {
    console.error(`Error from Python process: ${data}`);
    res.status(500).send('Error executing Python function');
  });

  // Handle the Python process completing
  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
  });
});

//http://localhost:3000/enterTrade?curr=ARB&tp=0.941,0.950,0.959,0.978,1.006&sl=0.904&entry=0.932,0.920&side=buy
app.get('/enterTrade', function(req, res) {
  // Import the child_process module
  const { spawn } = require('child_process');

  // Spawn a new Python process and pass the arguments
  const pythonProcess = spawn('python', ['./function_caller.py', "entry", req.query.curr,req.query.entry, req.query.tp,
  req.query.sl, req.query.side]);

  // Handle the output from the Python process
  pythonProcess.stdout.on('data', (data) => {
    // Convert the JSON string to an object
    const result = JSON.parse(data);
    if (result.status === 'success') {
      // Send the tradeObj value in the response
      res.send(result.tradeObj);
      return; // Return to prevent sending another response
    } else {
      // Send an error response with the error message
      res.status(500).send(result.message);
      return; // Return to prevent sending another response
    }
  });

  // Handle errors from the Python process
  pythonProcess.stderr.on('data', (data) => {
    console.error(`Error from Python process: ${data}`);
    res.status(500).send('Error executing Python function');
  });

  // Handle the Python process completing
  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
  });
});


