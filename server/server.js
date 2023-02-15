const express = require('express')

const PORT = 5000

const app = express()

app.get('/',(req,res) => {
    res.send("data is here")
})


app.listen(PORT , () => {
    console.log(`App is listening on port ${PORT}`)
})

