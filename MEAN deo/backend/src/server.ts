import express from 'express';
import cors from 'cors';
import mongoose from 'mongoose';
import dartRouter from './routers/dart.router';

const app = express();
app.use(cors())
app.use(express.json())

mongoose.connect('mongodb://127.0.0.1:27017/darts')
const conn = mongoose.connection
conn.once('open', ()=>{
    console.log("connection successful")
})

const router = express.Router()

router.use('/dart', dartRouter)

app.use('/', router)
app.listen(4000, () => console.log(`Express server running on port 4000`));
