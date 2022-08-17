<<<<<<< HEAD
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import * as redux from 'redux';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';

import { configureStore, Store } from './store';
import { AppContainer } from './App';

import { ServerRoot } from './utils/server';

const store: redux.Store<Store> = configureStore();
const server: ServerRoot = new ServerRoot(process.env.SERVER_API_PATH, store);
server.Start();
=======
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { createGlobalStyle } from 'styled-components';

import { store } from '@store';

import { App } from './App';

const GlobalStyle = createGlobalStyle`
  body {
    margin: 0;
    display: flex;
    font-family: 'Roboto', sans-serif;
    /* For firefox full height */
    height: 100%;
  }
  #content {
    flex-grow: 1;
    display: flex;
  }
  * {
    box-sizing: border-box;
  }
`;
>>>>>>> 92191d324... feat(interface): remake static

ReactDOM.render(
    <Provider store={store}>
        <BrowserRouter>
<<<<<<< HEAD
            <AppContainer />
=======
            <GlobalStyle />
            <App />
>>>>>>> 92191d324... feat(interface): remake static
        </BrowserRouter>
    </Provider>,
    document.getElementById('content'),
);
