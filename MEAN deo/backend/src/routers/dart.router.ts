import express from 'express'
import { DartController } from '../controllers/dart.controller'

const dartRouter = express.Router()

dartRouter.route('/playerExist').post(
    (req,res) => new DartController().playerExist(req,res)
)

dartRouter.route('/playerWins').post(
    (req,res) => new DartController().playerWins(req,res)
)

dartRouter.route('/playerExist_clock').post(
    (req,res) => new DartController().playerExist_clock(req,res)
)

dartRouter.route('/playerWins_clock').post(
    (req,res) => new DartController().playerWins_clock(req,res)
)

dartRouter.route('/getPlayers_x01').get(
    (req,res) => new DartController().getPlayers_x01(req,res)
)

dartRouter.route('/getPlayers_clock').get(
    (req,res) => new DartController().getPlayers_clock(req,res)
)


export default dartRouter