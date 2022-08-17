import { PropsWithChildren } from 'react';
import styled from 'styled-components';
import { ReactComponent as ButtonIconGreen } from '@assets/icon/callButtonGreen-icon.svg';
import { ReactComponent as ButtonIconRed } from '@assets/icon/callButtonRed-icon.svg';

type Color = 'red' | 'green';

const ButtonCall = styled.button<{ typeColor: Color }>`
    width: 100%;
    display: flex;
    justify-content: center;
    margin-bottom: 19px;
    border: 0;
    background: ${(props) => (props.typeColor === 'green' ? '#7ba970' : '#cf703a')};
    border-radius: 10px;
    cursor: pointer;
    &:hover {
        background: ${(props) => (props.typeColor === 'green' ? '#5a8350' : '#a6592e')};
    }
`;
const ButtonCallIcon = styled.div`
    align-self: center;
    padding: 20px 0;
`;

const ButtonCallText = styled.div`
    margin-left: 15px;
    align-self: center;
    font-family: 'Roboto';
    font-style: normal;
    font-weight: 400;
    font-size: 22px;
    line-height: 26px;
    color: #ffffff;
`;

interface IProps {
    type?: Color;
    onClick?: () => void;
}

export const DialogButton = ({ type = 'green', children, onClick }: PropsWithChildren<IProps>) => (
    <ButtonCall typeColor={type} onClick={onClick}>
        <ButtonCallIcon>
            {type === 'green' && <ButtonIconGreen />}
            {type === 'red' && <ButtonIconRed />}
        </ButtonCallIcon>
        <ButtonCallText>{children}</ButtonCallText>
    </ButtonCall>
);
