
const mongoose = require('mongoose');

const clientOptions = { serverApi: { version: '1', strict: true, deprecationErrors: true } };
const uri = "mongodb+srv://localuser:KhhmeiIHkmJcWOM2@aiexperimental.wqc5lk5.mongodb.net/?retryWrites=true&w=majority&appName=AIExperimental";


const connectDB = async () => {
  try {
    // Create a Mongoose client with a MongoClientOptions object to set the Stable API version
    await mongoose.connect(uri, clientOptions);
    await mongoose.connection.db.admin().command({ ping: 1 });
    console.log("Pinged your deployment. You successfully connected to MongoDB!");
    return mongoose
  } catch (err) {
    throw new Error(err)
  }
}

module.exports = connectDB;
