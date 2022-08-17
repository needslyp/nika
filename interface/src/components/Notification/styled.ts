import styled from 'styled-components';
export const Wrapper = styled.div<{ typeColor: 'warn' | 'error' }>`
    width: 475px;
    position: relative;
    display: flex;
    outline: 3px solid ${(props) => (props.typeColor === 'warn' ? '#F9943B' : '#FC2E20')};
    border-radius: 20px;
    background-color: white;
    @media (max-width: 768px) {
        min-width: 100%;
        width: auto;
        padding: 10px 8px 10px 14px;
    }
`;
export const WrapperIcon = styled.div`
    @media (max-width: 768px) {
        display: flex;
    }
`;
export const Icon = styled.div`
    position: absolute;
    top: -33px;
    left: 32px;
    width: 69px;
    height: 69px;
    @media (max-width: 768px) {
        position: static;
        margin: auto;
        width: 48px;
        height: 48px;
    }
`;
export const WrapperImage = styled.div`
    position: relative;
    overflow: hidden;
    width: 22%;
    border-bottom-left-radius: 15px;
    @media (max-width: 768px) {
        display: none;
    }
`;
export const Image = styled.div`
    position: absolute;
    left: -51px;
    top: 46px;
`;

export const Button = styled.button`
    margin-top: 26px;
    padding: 2px 8px;
    background: #f9943b;
    border-radius: 5px;
    border: 0;
    outline: none;
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 500;
    font-size: 17px;
    line-height: 26px;
    letter-spacing: -0.035em;
    color: #ffffff;
    cursor: pointer;
    @media (max-width: 768px) {
        margin-top: 6px;
        font-size: 10px;
        line-height: 15px;
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
        &:active {
            background: #d05301;
        }
    }
`;
export const ButtonMoreInformation = styled.div`
    display: inline-flex;
    height: 15px;
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 18px;
    letter-spacing: 0.02em;
    cursor: pointer;
    transition: 0.1s;
    &:hover {
        color: #7f848e;
    }
    &:hover path {
        fill: #7f848e;
    }
    @media (max-width: 768px) {
        font-size: 10px;
        line-height: 130%;
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0);

        &:hover {
            color: black;
        }
        &:hover path {
            fill: black;
        }
    }
`;
export const WrapperErrorArrowIcon = styled.div<{ flip: boolean }>`
    width: 9px;
    height: 11px;
    margin-top: 4px;
    transform: rotate(${({ flip }) => (flip ? 180 : 0)}deg);
    @media (max-width: 768px) {
        width: 5px;
        height: 6px;
        margin-top: 4px;
    }
`;
export const ButtonMoreInformationText = styled.div`
    margin-right: 3px;
    text-decoration: underline;

    @media (max-width: 768px) {
        margin-right: 2px;
        text-decoration: underline;
    }
`;
export const MoreInformationText = styled.div`
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 18px;
    letter-spacing: 0.02em;
    margin-top: 6px;
    @media (max-width: 768px) {
        margin-top: 0px;
        font-size: 10px;
        line-height: 130%;
    }
`;
export const CloseWrapper = styled.div`
    width: 39px;
    height: 39px;
    border-radius: 50%;
    position: absolute;
    top: 6px;
    right: 6px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    &:hover {
        background: rgba(186, 134, 102, 0.15);
    }
    @media (max-width: 768px) {
        position: static;
        min-width: 24px;
        max-height: 24px;
        width: 24px;
        height: 24px;
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
        &:hover {
            background: white;
        }
        &:active {
            background: rgba(186, 134, 102, 0.15);
        }
    }
`;
export const WrapperSize = styled.div`
    width: 19px;
    height: 19px;
    @media (max-width: 768px) {
        width: 14px;
        height: 14px;
    }
`;
export const Info = styled.div`
    width: 78%;
    padding: 30px;
    @media (max-width: 768px) {
        width: 100%;
        padding: 0 14px;
    }
`;
export const Title = styled.div`
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 500;
    font-size: 24px;
    line-height: 36px;
    letter-spacing: -0.035em;
    @media (max-width: 768px) {
        font-size: 16px;
        line-height: 24px;
    }
`;
export const Text = styled.div`
    margin-top: 8px;
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 18px;
    letter-spacing: 0.02em;
    @media (max-width: 768px) {
        margin-top: 0;
        font-size: 10px;
        line-height: 130%;
    }
`;
