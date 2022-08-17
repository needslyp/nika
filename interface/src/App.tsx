import { lazy, useEffect } from "react";
import { Route, Redirect } from "react-router-dom";
import { loadingComponent } from '@components/LoadingComponent';
import { routes } from '@constants';
import { useToast } from '@components/Toast';
import { client } from '@api';

import 'antd/dist/antd.css';
import './assets/main.css';

import { Layout } from 'antd';
const { Header, Content, Footer } = Layout;

import { Notification } from '@components/Notification';
import { HeaderPanel } from "@components/Header";
import { FooterPanel } from "@components/Footer";

const Demo = loadingComponent(lazy(() => import('@pages/Demo')));
const About = loadingComponent(lazy(() => import('@pages/About')));

const DemoRoutes = () => (
    <>
        <Route exact path={routes.MAIN}>
            <Demo />
        </Route>
        <Redirect to={routes.MAIN} />
    </>
);

const AboutRoutes = () => (
    <>
        <Route path={routes.ABOUT}>
            <About />
        </Route>
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
        <Layout>
            <Header>
                <HeaderPanel />
            </Header>
            <Content>
                <ClientNotifications />
                <DemoRoutes />
                <AboutRoutes />
            </Content>
            <Footer>
                <FooterPanel />
            </Footer>
        </Layout>
    );
};
