var username = "solomn"
var password = "123456"


function onchallenge(session, method,extra) {
    console.log("onchallenge",method,extra)

    if (method === "wampcra"){
        return autobahn.auth_cra.sign(password,extra.challenge)
    }else{
        throw "don't know how to authenticate using '" + method + "'";
    }
}



var connection = new autobahn.Connection({
    url:'ws://127.0.0.1:8080/ws_for_client',
    realm:'game',

    authmethods:['wampcra'],
    authid:username,
    onchallenge:onchallenge
});




var login = function() {
    connection.open();
};
function create_room() {
    connection.session.call('127.0.0.1.room_operate.create_room.new',[],{operation_data:{"args":[],kwargs:{"game_num":1}}}).then(
      function (res) {
         console.log("Result:", res);
      })
};

function enter_room() {
    connection.session.call('127.0.0.1.room_operate.0.enter',[],{operation_data:{"args":[],kwargs:{}}}).then(
      function (res) {
         console.log("Result:", res);
      }
   );

}

function sit_down() {
    connection.session.call('127.0.0.1.room_operate.0.sit_down',[],{operation_data:{"args":[],kwargs:{position:1}}}).then({
        function (res) {
         console.log("Result:", res);
      }
    })
}

function ready() {
    connection.session.call('127.0.0.1.room_operate.0.ready',[],{operation_data:{"args":[],kwargs:{}}}).then({
        function (res) {
         console.log("Result:", res);
      }
    })
}


