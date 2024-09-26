import mongoose from "mongoose";


const Schema = mongoose.Schema

let Dart_player_clock = new Schema({
    name:{
        type: String
    },
    wins:{
        type: Number
    }
})


export default mongoose.model("Dart_player_clockModel", Dart_player_clock, "dart_player_clock")
