import React from "react";

const Footer = () => {
  return (
    <footer className="footer block">
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
  );
};
export default Footer;
