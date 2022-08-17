<<<<<<< HEAD
import * as React from 'react';
import 'antd/dist/antd.css';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';

import * as store from './store';
import { Layout } from 'antd';
import { AppHeader } from './ui/AppHeader';
import { AppMain } from './ui/AppMain';
import '../assets/main.css';
import '../assets/spinner.css';
const { Header, Content, Footer } = Layout;

interface AppContainerProps {
    store?: store.Store;
}

function mapStateToProps(state: store.Store): any {
    return {
        store: state,
    };
}

export class AppContainerImpl extends React.Component<AppContainerProps, any> {
    private renderMainUI(): React.ReactNode {
        return (
            <Layout>
                <Header>
                    <AppHeader />
                </Header>
                <Content>
                    <AppMain />
                </Content>
                <Footer>
                    <span className="copyright">
                        Авторское право © Intelligent Semantic Systems LLC, Все права защищены
                    </span>
                </Footer>
            </Layout>
        );
    }

    private renderLoader(msg: string): React.ReactNode {
        return (
            <div className="loader-container">
                <div className="loader-vertical-center">
                    <div className="loader"></div>
                    <div className="loader-text">{msg}</div>
                </div>
            </div>
        );
    }

    private renderImpl(): React.ReactNode {
        const uiState: store.ui.State = this.props.store.ui;
        if (uiState.mode === store.ui.Mode.MainUI) return this.renderMainUI();

        return this.renderLoader(uiState.initMessage);
    }

    render(): React.ReactNode {
        return this.renderImpl();
    }
}

export const AppContainer = withRouter(connect(mapStateToProps)(AppContainerImpl) as any);
=======
import { lazy, useEffect } from 'react';
import { Route, Redirect } from 'react-router-dom';
import styled from 'styled-components';
import { routes } from '@constants';
import { loadingComponent } from '@components/LoadingComponent';
import { ToastProvider, useToast } from '@components/Toast';
import { Toasts } from '@components/Toasts';
import { client } from '@api';
import { Notification } from '@components/Notification';
import { Language } from '@components/Language';

const Demo = loadingComponent(lazy(() => import('@pages/Demo')));

const Wrapper = styled.div`
    width: 100%;
    background-color: #fff;
    display: flex;
    flex-direction: column;
`;

const Header = styled.div`
    background: rgba(68, 96, 89, 0.7);
    backdrop-filter: blur(10px);
    height: 98px;
    flex-shrink: 0;
    padding: 0 21px;
    display: flex;
    justify-content: space-between;
    @media (max-width: 768px) {
        position: absolute;
        top: 0;
        width: 100%;
        height: 43px;
        padding: 0 16px;
        background: linear-gradient(
            180deg,
            #4f7953 9.3%,
            rgba(96, 138, 100, 0.69) 56.54%,
            rgba(90, 120, 92, 0.31) 79.22%,
            rgba(84, 104, 86, 0) 100%
        );
        z-index: 2;
    }
`;

const Logo = styled.div`
    display: flex;
    align-items: center;
    color: white;
    font-weight: 500;
    font-size: 32px;
    line-height: 38px;
    @media (max-width: 768px) {
        padding-top: 11px;
        align-items: flex-start;
        line-height: 23px;
        font-size: 20px;
    }
`;
const LanguageWrapper = styled.div`
    display: flex;
    align-items: center;
    @media (max-width: 768px) {
        padding-top: 11px;
        align-items: flex-start;
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
    }
`;

const DemoRoutes = () => (
    <>
        <Route path={routes.DEMO}>
            <Demo />
        </Route>
        <Redirect to={routes.DEMO} />
    </>
);

const ClientNotifications = () => {
    const { addToast } = useToast();

    useEffect(() => {
        const onOpen = () => {
            console.log('::open::');
        };
        const onError = () => {
            const params = { id: 'netError', duration: 2000 };
            addToast(<Notification type="error" title="Connection lost" />, params);
        };
        client.addEventListener('open', onOpen);
        client.addEventListener('error', onError);

        return () => {
            client.removeEventListener('open', onOpen);
            client.removeEventListener('error', onError);
        };
    }, [addToast]);

    return null;
};

export const App = () => {
    return (
        <ToastProvider>
            <ClientNotifications />
            <Wrapper>
                <Header>
                    <Logo>IDESA</Logo>
                    <LanguageWrapper>
                        <Language />
                    </LanguageWrapper>
                </Header>
                <DemoRoutes />
            </Wrapper>
            <Toasts />
        </ToastProvider>
    );
};
>>>>>>> 92191d324... feat(interface): remake static
