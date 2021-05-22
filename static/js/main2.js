var commApp = new Vue({
    el:"#commApp",
    data:{
    comms:[
    {
        user:"Ivan",
        comm:"great pic"
    },
    {
        user:"Ivana",
        comm:"great inage"
    },
    {
        user:"Petar",
        comm:"fk u"
    },
    {
        user:"Boban",
        comm:"Nice cock bro!"
    },
    {
        user:"Morty",
        comm:"nice one mazte"
    },
    ],
    kom:false,
    objaviKom:false,
    prazan1:"",
    prazan:[],
    },
methods:{
    zaKom(){
    this.kom = true;
    },
    subKom(){
        if(this.prazan1 != ""){

            this.objaviKom=true;
            this.prazan.push(this.prazan1)
            this.prazan1 = "";
        }else{
            
        }
    },
}
})
var zaNav = new Vue({
el:".nav",
data:{
    profile:false,
    activity:false,
},
methods:{
    zaProfil(){
        this.profile = true;
    },
    zaProfDrp(){
        this.profile= false;
    },
    zaActy(){
        this.activity = true;
    },
    zaActyDrp(){
        this.activity = false;
    }
}
})