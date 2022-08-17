import { InputHTMLAttributes, PropsWithChildren } from 'react';
import styled from 'styled-components';

const Wrapper = styled.div`
    display: flex;
    align-items: center;
`;

const VisibleCheckbox = styled.div<{ isChecked?: boolean }>`
    border: 1px solid black;
    width: 24px;
    height: 24px;
    border-radius: 6px;
    margin-right: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: -1;
    transition: all ease 0.15s;
    background-color: #fff;
    &:hover {
        cursor: pointer;
    }
    &::before {
        content: '';
        width: 18px;
        height: 18px;
        transform: scale(${({ isChecked }) => (isChecked ? 1 : 0)});
        border-radius: 6px;
        background-color: #709975;
        transition: all ease 0.15s;
    }
    @media (max-width: 768px) {
        width: 21px;
        height: 21px;
        &::before {
            width: 15px;
            height: 15px;
        }
    }
`;

const Text = styled.label`
    font-family: 'Roboto';
    font-weight: 300;
    font-size: 18px;
    z-index: 2;
    line-height: 21px;
    &:hover {
        cursor: pointer;
    }
    @media (max-width: 768px) {
        font-size: 16px;
    }
`;

const StyledInput = styled.input`
    margin: 0;
    width: 24px;
    height: 24px;
    border: none;
    position: absolute;
    opacity: 0;
    &::placeholder {
        color: #9a9a9a;
    }
    &:hover {
        cursor: pointer;
    }
`;

interface IProps extends InputHTMLAttributes<HTMLInputElement> {
    className?: string;
}

export const Checkbox = ({ className, children, ...restInputProps }: PropsWithChildren<IProps>) => (
    <Wrapper className={className}>
        <StyledInput {...restInputProps} id="myCheckbox" type="checkbox" />
        <VisibleCheckbox isChecked={restInputProps.checked} />
        <Text htmlFor="myCheckbox">{children}</Text>
    </Wrapper>
);
