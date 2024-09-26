"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.DartController = void 0;
const dart_player_x01_1 = __importDefault(require("../models/dart_player_x01"));
const dart_player_clock_1 = __importDefault(require("../models/dart_player_clock"));
class DartController {
    constructor() {
        this.playerExist = (req, resp) => {
            let name = req.body.name;
            let newPlayer = new dart_player_x01_1.default({
                name: name,
                wins: 0
            });
            dart_player_x01_1.default.findOne({ "name": name })
                .then((player) => {
                if (player)
                    resp.json(player);
                else {
                    newPlayer.save()
                        .then((res) => {
                        resp.json({ "message": "ok" });
                    })
                        .catch((err) => console.log(err));
                }
            })
                .catch((err) => console.log(err));
        };
        this.playerWins = (req, resp) => {
            let name = req.body.name;
            dart_player_x01_1.default.findOne({ "name": name })
                .then((player) => {
                if (player != null) {
                    if (player.wins != null)
                        dart_player_x01_1.default.updateOne({ "name": player.name }, { $set: { "wins": (player.wins + 1) } })
                            .then(res2 => {
                        })
                            .catch((err) => console.log(err));
                }
            })
                .catch((err) => console.log(err));
        };
        this.playerExist_clock = (req, resp) => {
            let name = req.body.name;
            let newPlayer = new dart_player_clock_1.default({
                name: name,
                wins: 0
            });
            dart_player_clock_1.default.findOne({ "name": name })
                .then((player) => {
                if (player)
                    resp.json(player);
                else {
                    newPlayer.save()
                        .then((res) => {
                        resp.json({ "message": "ok" });
                    })
                        .catch((err) => console.log(err));
                }
            })
                .catch((err) => console.log(err));
        };
        this.playerWins_clock = (req, resp) => {
            let name = req.body.name;
            dart_player_clock_1.default.findOne({ "name": name })
                .then((player) => {
                if (player != null) {
                    if (player.wins != null)
                        dart_player_clock_1.default.updateOne({ "name": player.name }, { $set: { "wins": (player.wins + 1) } })
                            .then(res2 => {
                        })
                            .catch((err) => console.log(err));
                }
            })
                .catch((err) => console.log(err));
        };
        this.getPlayers_x01 = (req, resp) => {
            dart_player_x01_1.default.find({})
                .then((players) => {
                resp.json(players);
            })
                .catch((err) => console.log(err));
        };
        this.getPlayers_clock = (req, resp) => {
            dart_player_clock_1.default.find({})
                .then((players) => {
                resp.json(players);
            })
                .catch((err) => console.log(err));
        };
    }
}
exports.DartController = DartController;
