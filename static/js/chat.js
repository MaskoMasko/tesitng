
var app = new Vue({
    el:".komms",
    data:{
        kom3:false,
        sender:"",
        ti:"",
        oni:"",
        nasi:[],
        messes:undefined,
        mess1:"mess1",
        mess2:"mess2"
    }, 
    methods:{
      zaTebe(poruka, cijaJe,sender){
        this.ti = poruka;
        this.kom3 = cijaJe; //ako je true si ti
        this.sender = sender;
        if(cijaJe){
          this.nasi.push({strana:"desno", tekst:poruka});
        }else{
          this.nasi.push({strana:"livo", tekst:poruka, ime:sender});
        }
      }
    }
  })
      // 'use strict';
      var socket = io();
      socket.emit('online');
      
      addEventListener('submit', function(e) {
          e.preventDefault();
          var inputt = document.querySelector('#heil').value;
          if(inputt == ""){
            
          }else{
            socket.emit('message', inputt);
            document.querySelector('#heil').value = '';
          }
        });
  
  
        socket.on('announcements', function(data) {
          var k = data.split("///");
          var poruka = k[0];
          var sender = k[1];
          var cookieSender = getCookie('User');
          // alert(poruka+" "+ sender);
          if (sender == cookieSender){
              var strana = true;
          }else{
              var strana = false;
          }
          app.zaTebe(poruka,strana,sender)
          // ODAVDJE CALLAM
          //masovaFunkcija(poruka,sender,strana);
      });     // OVAKO PRIMAMO STVARI,PRVA JE KAO ID
  
      function getCookie(name) {
          const value = `; ${document.cookie}`;
          const parts = value.split(`; ${name}=`);
          if (parts.length === 2) return parts.pop().split(';').shift();
        }
        document.getElementById("1").innerHTML = "Vibecheck";
        