const express = require("express");
const app = express();

app.use(express.json());

app.get("/callback", (req, res) => {
  //console.log(JSON.stringify(req.body));
  console.log(req);
  res.send(req.url);
});

const port = process.env.PORT || 3333;
app.listen(port, () => console.log("Resource Server running on port " + port));
