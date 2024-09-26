import mongoose from "mongoose";


const Schema = mongoose.Schema

let Dart_player_x01 = new Schema({
    name:{
        type: String
    },
    wins:{
        type: Number
    }
})


export default mongoose.model("Dart_player_x01Model", Dart_player_x01, "dart_player_x01")
