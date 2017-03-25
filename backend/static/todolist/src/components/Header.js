import React from "react";

const Header = ({ text, addTodo }) => {
  return (
    <header className="header">
      <h1>{text}</h1>
      <input
        className="new-todo"
        placeholder="What needs to be done?"
        autofocus=""
        onKeyPress={(e)=>{
            if(e.key=== "Enter"){
                addTodo(e.target.value);
                e.target.value = ""
            }
        }}
      />
    </header>
  );
};

export default Header;
