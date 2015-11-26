var http = require('http');
var xmlWriter = require('xml-writer');
var mysql = require('mysql');
var url = require('url');
var proj4 = require('proj4');
var qs = require('querystring');

var pool = mysql.createPool({
	connectionLimit : 100,
	host : 'localhost',
	user : 'root',
	password : 'ruinpikapika123',
	database : 'service'
});

var makeXmlFile = function(xml,id,cate,loca,name,pos,website,realaddr,phone,pic){
	xml.startElement('info');
	xml.writeElement('id',id);
	xml.writeElement('category',cate);
	xml.writeElement('loca',loca);
	xml.writeElement('name',name);
	xml.writeElement('pos',"{"+pos[1]+","+pos[0]+"}");
	xml.writeElement('website',website);
	xml.writeElement('realaddr',realaddr);
	xml.writeElement('phone',phone);
	xml.endElement();
};
var makeWGS1984 = function (x, y){
  	var first = '+proj=tmerc +lat_0=37.999958 +lon_0=126.999958 +k=1 +x_0=200000 +y_0=500000 +ellps=GRS80 +units=m +no_defs'; //ITRF2000방식
	var second = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs";                          

	return proj4(first, second, [x,y])
}
var makeITRF2000 = function (x, y) {
  	var first = '+proj=tmerc +lat_0=37.999958 +lon_0=126.999958 +k=1 +x_0=200000 +y_0=500000 +ellps=GRS80 +units=m +no_defs'; //ITRF2000방식
	var second = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs";                          

	return proj4(second, first, [x,y])
}
// test 
var server = http.createServer(function (req, res)  {
	pool.getConnection(function (err,con){
		xw = new xmlWriter;
		xw.startDocument('1.0', 'UTF-8');
		console.log("hello")

		var url_parts = url.parse(req.url,true);
		for (var q in url_parts.query)
		{
			console.log(q)
		}
		console.log(""+url_parts.query['category']);
		con.query('select * from LENDSERVICE where CATEGORY = "'+url_parts.query['category']+'" limit 40',function(err,rows){
			if(err) console.error("error : " + err);

			xw.startElement('root');

			for (var i = 0; i < rows.length; i++) {
				var pos = makeWGS1984(rows[i].POSX,rows[i].POSY)

				makeXmlFile(xw,rows[i].ID,rows[i].CATEGORY,rows[i].LOCAL,rows[i].SVC_NM,pos,rows[i].LENTSITE,rows[i].ADDRESS,rows[i].PHONE,"");
			};

			//console.log(xw.toString());
			//console.log(rows);
			xw.endDocument();
			res.write(xw.toString());
			res.end();
		});
		con.release();
	});
});
server.listen(8080);
