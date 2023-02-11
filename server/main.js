const express = require('express');
const path = require("path");

const app = express();
app.use(express.static('public'));

const PORT = process.env.PORT || 6969;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}...`);
});