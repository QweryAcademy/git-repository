import React from "react";

const TodoItem = ({ todo }) => {
  return (
    <li>
      <div className="view">
        <input className="toggle" type="checkbox" checked={todo.completed} />
        <label>{todo.content}</label>
        <button className="destroy" />
      </div>
      <input className="edit" value={todo.content} />
    </li>
  );
};

const TodoList = ({ items }) => {
    const newItems = items.map(function(element, index){
        // var key = element + index;
        return <TodoItem key={`${element}${index}`} todo={element}  />
    })
  return (
    <ul className="todo-list">
        {newItems}
      </ul>
  );
};

export default TodoList;
