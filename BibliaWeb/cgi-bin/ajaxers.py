
AjaxStuff = """
    function AxLookup()
    {
        var ajax = new XMLHttpRequest();
        ajax.onreadystatechange = function(){
            if(this.readyState == 4 && this.status == 200){
                var ele = document.getElementById('xbook');
                ele.innerHTML = "";
                var sigma = ele.innerHTML + this.responseText;
                ele.innerHTML = sigma;
            }
        };
        var raw = "";
        var ele = document.getElementById('id_sierra');
        raw += ele.value;
        raw += "|";
        var ele = document.getElementById('id_verse');
        raw += ele.value;
        raw += "|";
        var ele = document.getElementById('id_book');
        raw += ele.value;
        ajax.open("GET", "sierra.py?xlookup2=" + raw, true);
        ajax.send();
    }
    function AxBookmark(verse, zid)
    {
        var ajax = new XMLHttpRequest();
        ajax.onreadystatechange = function(){
            if(this.readyState == 4 && this.status == 200){
                var ele = document.getElementById(zid); //"xbkmrk");
                var sigma = ele.innerHTML + this.responseText;
                ele.innerHTML = sigma;
            }
        };
        ajax.open("GET", "sierra.py?xbkmrk=" + verse, true);
        ajax.send();
    }
    function AxVerse(sierra_num)
    {
        var ajax = new XMLHttpRequest();
        ajax.onreadystatechange = function(){
            if(this.readyState == 4 && this.status == 200){
                var ele = document.getElementById("xbook");
                ele.innerHTML = this.responseText;
            }
        };
        ajax.open("GET", "sierra.py?xrecall=" + sierra_num, true);
        ajax.send();
    }
    function AxBook(xbook)
    {
        var ajax = new XMLHttpRequest();
        ajax.onreadystatechange = function(){
            if(this.readyState == 4 && this.status == 200){
                var ele = document.getElementById("xbook");
                ele.innerHTML = this.responseText;
            }
        };
        ajax.open("GET", "sierra.py?xbook=" + xbook, true);
        ajax.send();
    }
    function AxMenu(xopt)
    {
        var ajax = new XMLHttpRequest();
        ajax.onreadystatechange = function(){
            if(this.readyState == 4 && this.status == 200){
                var ele = document.getElementById("zbooks");
                ele.innerHTML = this.responseText;
            }
        };
        ajax.open("GET", "sierra.py?xmenu=" + xopt, true);
        ajax.send();
    }
    function Ax(req, eleID)
    {
        var ajax = new XMLHttpRequest();
        ajax.onreadystatechange = function(){
            if(this.readyState == 4 && this.status == 200){
                var ele = document.getElementById(eleID);
                ele.innerHTML = this.responseText;
            }
        };
        ajax.open("GET", "sierra.py" + req, true);
        ajax.send();
    }
    function AxVal(req, inID, outID)
    {
        var ajax = new XMLHttpRequest();
        ajax.onreadystatechange = function(){
            if(this.readyState == 4 && this.status == 200){
                var ele = document.getElementById(outID);
                ele.innerHTML = this.responseText;
            }
        };
        var data = document.getElementById(inID).value;
        if(data == null || data.length == 0) {
            data = "none";
        }
        ajax.open("GET", "sierra.py" + req + data, true);
        ajax.send();
    }
"""

class Chunk:
    ''' Eliminate browser-based HTML parsing, in favor of
    a hidden, textual, DOM element. '''
    def __init__(self, chunkid='chunk'):
        self.chunkid = chunkid
        self.chunk_clear = '''
function ChunkClear() {
    ele = document.getElementById('{self.chunkid}');
    if(ele != null) {
        ele.innerTEXT = '';
    }
}'''
        self.chunk_nelem = '''
function ChunkNelem() {
    var items = ChunkList();
    if(items === null) {
       return null;
    }
    return items.length;
} '''
        self.chunk_list = '''
function ChunkList() {
    var chunk = document.getElementById('{self.chunkid}');
    var items = chunk.innerTEXT;
    if(items == null) {
       return null;
    }
    var cols = items.split('|');
    return cols;
}'''
        self.chunk_delete = '''
function ChunkDelete(value) {
    var chunk = document.getElementById('{self.chunkid}');
    var items = chunk.innerTEXT;
    if(items == null) {
       return; // NEED TO ChunkClear, PLEASE
    }
    var cols = ChunkList();
    chunk.innerTEXT = '';
    for(ss=0;ss < cols.length;ss++) {
        if(ss != value) {
            var row = cols[ss];
            if(row != null) {
                ChunkAppend(row);
            }
        }
    }
    ChunkRedraw();
}'''
        self.chunk_append = '''
function ChunkAppend(...values) {
    if(values == null || values.length == 0) {
        return;
    }
    var nelem = ChunkNelem();
    var chunk = document.getElementById('{self.chunkid}');
    if(chunk.innerTEXT == null) {
        chunk.innerTEXT = values;
    } else {
        chunk.innerTEXT += '|';
        chunk.innerTEXT += values;
    }
}'''

    def fout(self, string):
        return string.replace('{self.chunkid}', self.chunkid)

    def get_html(self):
        return f"<div hidden id='{self.chunkid}'></div>"
    
    def get_script(self):
##        script = self.fout(self.chunk_clear)
##        script += self.fout(self.chunk_list)
##        script += self.fout(self.chunk_nelem)
##        script += self.fout(self.chunk_delete)
##        script += self.fout(self.chunk_append)
##        return script
        return ''
