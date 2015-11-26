
function SQLHelper(type){
	this.SQL = "";
	this.reqValue = "";
	this.table = "";
	this.type = type;
}
var a = new SQLHelper("!23");
console.log(SQLHelper.prototype);


