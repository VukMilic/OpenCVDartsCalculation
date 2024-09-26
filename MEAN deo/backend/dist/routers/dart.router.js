"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const dart_controller_1 = require("../controllers/dart.controller");
const dartRouter = express_1.default.Router();
dartRouter.route('/playerExist').post((req, res) => new dart_controller_1.DartController().playerExist(req, res));
dartRouter.route('/playerWins').post((req, res) => new dart_controller_1.DartController().playerWins(req, res));
dartRouter.route('/playerExist_clock').post((req, res) => new dart_controller_1.DartController().playerExist_clock(req, res));
dartRouter.route('/playerWins_clock').post((req, res) => new dart_controller_1.DartController().playerWins_clock(req, res));
dartRouter.route('/getPlayers_x01').get((req, res) => new dart_controller_1.DartController().getPlayers_x01(req, res));
dartRouter.route('/getPlayers_clock').get((req, res) => new dart_controller_1.DartController().getPlayers_clock(req, res));
exports.default = dartRouter;
