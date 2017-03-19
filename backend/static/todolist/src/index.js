import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import "./index.css";

ReactDOM.render(<App todos={window.all_todos} />, document.getElementById("root"));
