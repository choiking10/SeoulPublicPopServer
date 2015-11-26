/*
	sppsql.js
	SeoulPublicPop project server
	Created by 최윤호 on 2015. 11. 26 (thr)

	퍼블릭 팝의 sql처리 관련 루틴을 모아논 모듈

	각각의 필요로하는 구조는 json파일의 형태로 type.json으로 저장되어 있다.
*/

var mysql = require('mysql');

//sppsql 클래스의 생성자
function sppsql() {

	//mysql의 커넥션 풀을 생성한다. 
	var sqlpool = mysql.createPool( {
		connectionLimit : 100,
		host : 'localhost',
		user : 'root',
		password : 'ruinpikapika123',
		database : 'service'
	});	//private value

	this.QVT = {
		
	}
}
// @param type 		: 	요청한 쿼리의 타입 종류
// @param parameter	: 	해당 타입에 대한 파라미터, 딕셔너리로 들어옴
// @param result 	: 	요청한 쿼리에 대한 콜백 함수. 필요한 정보에 대한
//						결과물이 배열로 들어옴( 내부에 딕셔너리로 값이
//						들어있음)

sppsql.connectdb = function(type, parameter ,callback) {
	
	var sqlquery = "";

	switch(type) {
	case 'subdetail':
		break;
	case 'detail':
		break;
	case 'mapinfo':
		break;
	case 'localinfo':
		break;
	default :
		console.log('unknown type : '+type+')');
	}


	sqlpool.getConnection(function(objErr,con) {
		if(objErr) {
			console.log("database connection error! in sppsql.connectdb");
			console.trace();
		}

		con.query(sqlquery,function(err,rows) {
			if(err) {
				console.log("sql query is wrong! error : " err);
			}

			var result = [];
			for(var i = 0; i < rows.length; i++) {
				result.append(rows[i]);
			callback(result);
			con.release();
		});
	}
}

module.exports = sppsql;

