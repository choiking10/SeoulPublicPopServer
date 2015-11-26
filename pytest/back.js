'use strict';
var forever = require('forever');

/*
var child = new (forever.Monitor)('test.js');

child.on( "exit", function() {
  console.log( 'app.js has exited!' );
} );
child.on( "restart", function() {
  console.log( 'app.js has restarted.' );
} );
child.on( 'watch:restart', function( info ) {
  console.error( 'Restarting script because ' + info.file + ' changed' );
} );
*/
//child.start();
//forever.startServer(child);
forever.startDaemon("test.js");

//You can catch other signals too
process.on( 'SIGINT', function() {
  console.log( "\nGracefully shutting down \'node forever\' from SIGINT (Ctrl-C)" );
  // some other closing procedures go here
  process.exit();
} );

process.on( 'exit', function() {
  console.log( 'About to exit \'node forever\' process.' );
} );

//Sometimes it helps...
process.on( 'uncaughtException', function( err ) {
  console.log( 'Caught exception in \'node forever\': ' + err );
} );
