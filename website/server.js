const express = require('express');
const mongoose = require('mongoose');
const app = express();
const ejs = require('ejs');

app.set('view engine', 'ejs');

mongoose.connect('mongodb+srv://vasco:rootadmin@bethub.24hpv.mongodb.net/BetHub?retryWrites=true&w=majority')

const gamesSchema = {
    game_id: String,
    home: String,
    away: String,
    v1: String,
    x: String,
    v2: String,
    percentage: String
}

const Game = mongoose.model('Game', gamesSchema);


app.get('/', (req, res) => {
   Game.find({}, function(err, games) {
       res.render('index', {
           gamesList: games
       })
   })
})

app.listen(4000, function() {
    console.log('server is running');
})