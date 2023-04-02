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


//http://localhost:3000/putTrade?curr=ARP&entry=21,23&tp=12,21&sl=43&side=buy
app.get('/putTrade', function(req, res) {
  // Import the child_process module
  const { spawn } = require('child_process');

  // Parse the entry and tp arrays from the query parameters
  const entryString = req.query.entry || '';
  const tpString = req.query.tp || '';

  const entryArray = entryString.split(',').map(parseFloat);
  const tpArray = tpString.split(',').map(parseFloat);

  console.log('entryArray:', entryArray);
  console.log('tpArray:', tpArray);

  // Spawn a new Python process and pass the arguments
  const pythonArgs = ['./function_caller.py', "put", req.query.curr, JSON.stringify(entryArray), JSON.stringify(tpArray), req.query.sl, req.query.side];
  console.log('Python arguments:', pythonArgs);
  const pythonProcess = spawn('python', pythonArgs);

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Output from Python process: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Error from Python process: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
    // Send a response back to the client when the Python process exits
    if (code === 0) {
      res.json({ status: 'success' });
    } else {
      res.status(500).json({ status: 'error', message: 'An error occurred while processing the request.' });
    }
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
      res.send(result.OrderID);
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


app.get('/getAllTrades', (req, res) => {

  const { spawn } = require('child_process');
  const py = spawn('python3', ['function_caller.py', 'getAllTrades']);

  let outputData = '';

  // Handle the standard output (stdout) from the Python script
  py.stdout.on('data', (data) => {
    outputData += data.toString();
  });

  // Handle the error output (stderr) from the Python script
  py.stderr.on('data', (data) => {
    console.error('Python stderr: ' + data.toString());
  });

  // Send the data back to the client when the Python script is done
py.on('close', (code) => {
  console.log('Python process exited with code ' + code);

  console.log('Raw output data: ', outputData); // Log the raw output data

  try {
    const fixedOutputData = outputData.replace(/'/g, '"');
    const jsonData = JSON.parse(fixedOutputData);
    console.log('Parsed JSON: ', jsonData);
    res.json(jsonData);
  } catch (err) {
    res.status(500).send('Error parsing JSON from Python script: ' + err.message);
  }
});
});
