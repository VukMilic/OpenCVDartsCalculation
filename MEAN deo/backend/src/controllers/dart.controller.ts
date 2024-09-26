import express from 'express'
import Dart_player_x01Model from '../models/dart_player_x01'
import Dart_player_clockModel from '../models/dart_player_clock'

export class DartController {
    playerExist = (req: express.Request, resp: express.Response) => {
        let name = req.body.name

        let newPlayer = new Dart_player_x01Model({
            name: name,
            wins: 0
        })

        Dart_player_x01Model.findOne({ "name": name })
        .then((player) => {
            if (player)
                resp.json(player)
            else{
                newPlayer.save()
                .then((res)=>{
                    resp.json({ "message": "ok" });
                })
                .catch((err)=>console.log(err))
            }
        })
        .catch((err) => console.log(err))
    }

    playerWins = (req: express.Request, resp: express.Response) => {
        let name = req.body.name

        Dart_player_x01Model.findOne({ "name": name })
            .then((player) => {
                if(player != null){
                    if(player.wins != null)
                        Dart_player_x01Model.updateOne({ "name": player.name }, { $set: { "wins": (player.wins + 1)}})
                            .then(res2 => {

                            })
                            .catch((err)=> console.log(err))
                }
            })
            .catch((err) => console.log(err))
    }

    playerExist_clock = (req: express.Request, resp: express.Response) => {
        let name = req.body.name

        let newPlayer = new Dart_player_clockModel({
            name: name,
            wins: 0
        })

        Dart_player_clockModel.findOne({ "name": name })
        .then((player) => {
            if (player)
                resp.json(player)
            else{
                newPlayer.save()
                .then((res)=>{
                    resp.json({ "message": "ok" });
                })
                .catch((err)=>console.log(err))
            }
        })
        .catch((err) => console.log(err))
    }

    playerWins_clock = (req: express.Request, resp: express.Response) => {
        let name = req.body.name

        Dart_player_clockModel.findOne({ "name": name })
            .then((player) => {
                if(player != null){
                    if(player.wins != null)
                        Dart_player_clockModel.updateOne({ "name": player.name }, { $set: { "wins": (player.wins + 1)}})
                            .then(res2 => {

                            })
                            .catch((err)=> console.log(err))
                }
            })
            .catch((err) => console.log(err))
    }

    getPlayers_x01 = (req: express.Request, resp: express.Response) => {
        Dart_player_x01Model.find({})
            .then((players) => {
                resp.json(players)
            })
            .catch((err) => console.log(err))
    }

    getPlayers_clock = (req: express.Request, resp: express.Response) => {
        Dart_player_clockModel.find({})
            .then((players) => {
                resp.json(players)
            })
            .catch((err) => console.log(err))
    }
}