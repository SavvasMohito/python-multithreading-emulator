const express = require("express");
const app = express();

app.use(express.json());

app.post("/posts", (req, res) => {
  //console.log(JSON.stringify(req.body));
  console.log(req.headers["authorization"]);
  console.log(req.body);
  res.send("ACCESS GRANTED! TOKEN IS VALID.");
});

const port = process.env.PORT || 3333;
app.listen(port, () => console.log("Resource Server running on port " + port));
