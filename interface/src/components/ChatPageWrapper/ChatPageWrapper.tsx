import styled from 'styled-components';

export const ChatPageWrapper = styled.div`
    padding: 18px 22px;
    max-height: calc(100vh - 98px);
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    flex-grow: 1;
    @media (max-width: 768px) {
        padding: 0;
        grid-template-rows: auto 1fr;
    }
`;
