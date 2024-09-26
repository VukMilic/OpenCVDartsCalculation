"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const mongoose_1 = __importDefault(require("mongoose"));
const Schema = mongoose_1.default.Schema;
let Dart_player_clock = new Schema({
    name: {
        type: String
    },
    wins: {
        type: Number
    }
});
exports.default = mongoose_1.default.model("Dart_player_clockModel", Dart_player_clock, "dart_player_clock");
