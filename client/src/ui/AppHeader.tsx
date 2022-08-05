import * as React from 'react';
import { connect } from 'react-redux';
import { NavLink } from 'react-router-dom';

class HeaderImpl extends React.Component {
    render() {
        return (
            <div className="header">
                <h1 className="header-logo-text">IDESA</h1>
                <div className="nav-container">
                    <ul className="nav">
                        <li>
                            <NavLink to="/home">Главная</NavLink>
                        </li>
                        <li>
                            <NavLink to="/about">О нас</NavLink>
                        </li>
                    </ul>
                </div>
            </div>
        );
    }
}

export const AppHeader = connect()(HeaderImpl);
