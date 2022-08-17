import * as React from 'react';
import { NavLink } from 'react-router-dom';

export const HeaderPanel = () => {
  return (
    <div className="header">
      <h1 className="header-logo-text">NIKA</h1>
      <div className="nav-container">
        <ul className="nav">
          <li>
            <NavLink to="/demo">Главная</NavLink>
          </li>
          <li>
            <NavLink to="/about">О нас</NavLink>
          </li>
        </ul>
      </div>
    </div>
  );
}
