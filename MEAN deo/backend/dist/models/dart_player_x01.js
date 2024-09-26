"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const mongoose_1 = __importDefault(require("mongoose"));
const Schema = mongoose_1.default.Schema;
let Dart_player_x01 = new Schema({
    name: {
        type: String
    },
    wins: {
        type: Number
    }
});
exports.default = mongoose_1.default.model("Dart_player_x01Model", Dart_player_x01, "dart_player_x01");
