import { Toast, useToast } from '@components/Toast';
import styled from 'styled-components';

const Wrapper = styled.div`
    position: fixed;
    bottom: 24px;
    right: 24px;
    display: flex;
    flex-direction: column;
    gap: 43px;
    @media (max-width: 768px) {
        top: 7;
        right: 8;
        bottom: auto;
        left: 8;
        z-index: 2;
    }
`;

export const Toasts = () => {
    const { toasts } = useToast();

    return (
        <Wrapper>
            {toasts.map(({ params, component }) => (
                <Toast key={params.id} id={params.id} component={component} duration={params.duration} />
            ))}
        </Wrapper>
    );
};
