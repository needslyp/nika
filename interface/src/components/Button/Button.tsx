import { ButtonHTMLAttributes, ReactNode } from 'react';
import styled from 'styled-components';

const HTMLButton = styled.button`
    align-self: center;
    color: white;
    display: block;
    font-weight: 300;
    font-size: 26px;
    line-height: 30px;
    padding: 6px 32px;
    background: #709975;
    border: none;
    border-radius: 25px;
    outline: none;
    cursor: pointer;
    transition: all ease 0.15s;

    &:hover {
        background: #849299;
    }
    @media (max-width: 768px) {
        padding: 5px 27px;
        font-size: 22px;
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
        &:hover {
            background: #709975;
        }
        &:active {
            background: #849299;
        }
    }
`;

interface IProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    children?: ReactNode;
}

export const Button = ({ children, type = 'button', ...restProps }: IProps) => (
    <HTMLButton {...restProps} type={type}>
        {children}
    </HTMLButton>
);
