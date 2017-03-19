import React, { Component } from 'react';
import './App.css';

const Header = ({text}) => {
  return (
    <header className="header">
      <h1>{text}</h1>
      <input className="new-todo" placeholder="What needs to be done?" autofocus="" />
    </header>)
}
const TodoList = () => {
  return (
    <section className="main block">
      <input className="toggle-all" id="toggle-all" type="checkbox" />
      <label for="toggle-all">Mark all as complete</label>
      <ul className="todo-list"><li>
        <div className="view">
          <input className="toggle" type="checkbox" />
          <label>jams</label>
          <button className="destroy"></button>
        </div>
        <input className="edit" value="jams" />
      </li><li>
          <div className="view">
            <input className="toggle" type="checkbox" />
            <label>shola</label>
            <button className="destroy"></button>
          </div>
          <input className="edit" value="shola" />
        </li><li>
          <div className="view">
            <input className="toggle" type="checkbox" />
            <label>shope</label>
            <button className="destroy"></button>
          </div>
          <input className="edit" value="shope" />
        </li></ul>
    </section>
  )
}
const Footer = () => {
  return (
    <footer className="footer block" >
      <span className="todo-count"><strong>3</strong> items left</span>
      <ul className="filters">
        <li>
          <a className="selected" href="#/">All</a>
        </li>
        <li>
          <a href="#/active">Active</a>
        </li>
        <li>
          <a href="#/completed">Completed</a>
        </li>
      </ul>

    </footer>

  )
}

function App() {
  return (
    <section className="todoapp">
      <Header text={"Our todos"} />
      <TodoList />
      <Footer />
    </section>
  )
}

export default App;
