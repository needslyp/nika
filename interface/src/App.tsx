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
