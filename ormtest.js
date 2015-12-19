var Sequelize = require('sequelize')
var mysql = require('mysql')


var sequelize = new Sequelize('service', 'root','ruinpikapika123')

var Project = sequelize.define('LENDSERVICE',{
	ID        :	{ type : Sequelize.INTEGER    , 	primaryKey: true , 	autoIncrement: true },
	SVC_ID    :	{ type : Sequelize.STRING 	},
	SVC_NM    :	{ type : Sequelize.STRING 	},
	CATEGORY  :	{ type : Sequelize.STRING 	},
	LOCAL     :	{ type : Sequelize.STRING	},
	POSX      :	{ type : Sequelize.DOUBLE	},
	POSY      :	{ type : Sequelize.DOUBLE 	},
	LENTSITE  :	{ type : Sequelize.TEXT     },
	ADDRESS   :	{ type : Sequelize.STRING	},
	PHONE     :	{ type : Sequelize.STRING	}
}); 

sequelize.sync();
var connect = mysql.createConnection({
	host 	: "localhost",
	port	: 3306,
	user	: "root",
	passwaord : "ruinpikapika123",
	database  : "service"
});

connect.connect();

connect.query("SELECT * FROM LENDSERVICE", function(err, row) {
		
})
/*
console.log(Project);
Project.findAll().then(function(test){
	console.log("hello")
})

*/
/*
Project.findById(1).success(function(project) {
	console.log('sucess')
})
*/

