import styled from 'styled-components';
import { ChatPageWrapper } from '@components/ChatPageWrapper';

export const Wrapper = styled(ChatPageWrapper)`
    grid-template-areas:
        'video chat'
        'robot chat';
    grid-gap: 11px;
    @media (max-width: 768px) {
        grid-template-areas:
            'video video'
            'chat chat';
        grid-gap: 0px;
        min-height: 100%;
        grid-template-rows: 0.38fr 0.62fr;
        background: rgba(151, 206, 157, 0.2);
        backdrop-filter: blur(10px);
    }
`;

export const ChatWrapper = styled.div`
    border-radius: 8px;
    grid-area: chat;
    @media (max-width: 768px) {
        overflow: auto;
        border-radius: 0px;
    }
`;

