import * as React from 'react';
import { connect } from 'react-redux';
import { Redirect } from 'react-router';
import { Route, Switch } from 'react-router-dom';
import { About } from './AboutPage';
import { VoiceRecorder } from './VoiceRecorder';
import { Prompt } from './Tips';

import { ScgViewer } from './ScgViewer';

class MainImpl extends React.Component {
    render() {
        return (
            <div className="main">
                <Switch>
                    <Route path="/" exact>
                        <Redirect to="/home" />
                    </Route>
                    <Route path="/home">
                        <div className="central-area">
                            <div className="chat-prompt">
                                <Prompt />
                                <VoiceRecorder />
                            </div>
                            <ScgViewer />
                        </div>
                    </Route>

                    <Route path="/about">
                        <About />
                    </Route>
                </Switch>
            </div>
        );
    }
}

export const AppMain = connect()(MainImpl);
