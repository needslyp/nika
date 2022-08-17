import { InputHTMLAttributes, useRef, useState } from 'react';
import styled from 'styled-components';

const getBorderColor = (isFocused?: boolean, isError?: boolean) => {
    if (isError) return '#FF0000';
    if (isFocused) return '#97CE9D';
    return '#000000';
};

const Wrapper = styled.div<{ isFocused?: boolean; isError?: boolean }>`
    border-radius: 10px;
    border: 1px solid #000000;
    background-color: #fff;
    padding: 8px 14px;
    border-color: ${({ isFocused, isError }) => getBorderColor(isFocused, isError)};
    transition: border-color ease 0.15s;
    &:hover {
        border-color: ${({ isError }) => (isError ? '#FF0000' : '#97CE9D')};
    }
    @media (max-width: 768px) {
        padding: 8px 12px;
    }
`;

const StyledInput = styled.input`
    display: block;
    box-shadow: none;
    outline: none;
    border: none;
    font-family: 'Roboto';
    font-style: normal;
    font-weight: 300;
    font-size: 18px;
    line-height: 21px;
    color: #000000;
    &::placeholder {
        color: #9a9a9a;
    }
    @media (max-width: 768px) {
        font-size: 16px;
    }
`;

const Error = styled.div`
    color: #ff0000;
    margin-top: 10px;
`;

interface IProps extends InputHTMLAttributes<HTMLInputElement> {
    error?: string;
    className?: string;
}

export const Input = ({ error, className, ...restInputProps }: IProps) => {
    const [isFocused, setIsFocused] = useState(false);

    const inputRef = useRef<HTMLInputElement>(null);

    const onFocus = () => setIsFocused(true);
    const onBlur = () => setIsFocused(false);

    return (
        <Wrapper className={className} isFocused={isFocused} isError={!!error}>
            <StyledInput {...restInputProps} ref={inputRef} onFocus={onFocus} onBlur={onBlur} type="text" />
            {error && <Error>{error}</Error>}
        </Wrapper>
    );
};
