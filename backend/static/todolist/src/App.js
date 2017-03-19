import React, { Component } from "react";
import Header from "./components/Header";
import TodoList from "./components/TodoList";
import Footer from "./components/Footer";
import "./App.css";

class App extends Component {
  constructor() {
    super();
    this.state = {
      todos: []
    };
    var that = this;
    this.addTodo = text => {
      let oldTodos = this.state.todos;
      // var response = fetch("/add_todo/", {
      //   method: "post",
      //   headers: {
      //     "Content-Type": "application/json"
      //   },
      //   body: JSON.stringify({ content: "hello world" })
      // });
      // response
      //   .then(function(data) {
      //     return data.json();
      //   })
      //   .then(data => {
      //     that.setState({ todos: data });
      //   });
      oldTodos.push({ id: 1, content: text, completed: false });
      this.setState({ todos: oldTodos });
      // this.setState(function(prevState, props){
      //   prevState.todos = oldTodos
      //   return prevState;
      // })
    };
  }
  componentDidMount() {
    this.setState({ todos: this.props.todos || [] });
    // this.setState(function(prevState, props) {
    //   // return {...prevState, ...props}
    //   prevState.todos = props.todos || [];
    //   return prevState;
    // });
  }
  render() {
    return (
      <section className="todoapp">
        <Header addTodo={this.addTodo} text={"Our todos"} />
        <section className="main block">
          <input className="toggle-all" id="toggle-all" type="checkbox" />
          <label for="toggle-all">Mark all as complete</label>
          <TodoList items={this.state.todos} />
        </section>
        <Footer />
      </section>
    );
  }
}

export default App;
