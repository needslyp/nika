import styled from 'styled-components';
export const Wrapper = styled.div<{ typeColor: 'warn' | 'error' }>`
    width: 475px;
    position: relative;
    display: flex;
    outline: 3px solid ${(props) => (props.typeColor === 'warn' ? '#F9943B' : '#FC2E20')};
    border-radius: 20px;
    background-color: white;
`;
export const WrapperIcon = styled.div`
`;
export const Icon = styled.div`
    position: absolute;
    top: -33px;
    left: 32px;
    width: 69px;
    height: 69px;
`;
export const WrapperImage = styled.div`
    position: relative;
    overflow: hidden;
    width: 22%;
    border-bottom-left-radius: 15px;
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
    font-family: 'Roboto';
    font-style: normal;
    font-weight: 500;
    font-size: 17px;
    line-height: 26px;
    letter-spacing: -0.035em;
    color: #ffffff;
    cursor: pointer;
`;
export const ButtonMoreInformation = styled.div`
    display: inline-flex;
    height: 15px;
    font-family: 'Roboto';
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
`;
export const WrapperErrorArrowIcon = styled.div<{ flip: boolean }>`
    width: 9px;
    height: 11px;
    margin-top: 4px;
    transform: rotate(${({ flip }) => (flip ? 180 : 0)}deg);
`;
export const ButtonMoreInformationText = styled.div`
    margin-right: 3px;
    text-decoration: underline;
`;
export const MoreInformationText = styled.div`
    font-family: 'Roboto';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 18px;
    letter-spacing: 0.02em;
    margin-top: 6px;
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
`;
export const WrapperSize = styled.div`
    width: 19px;
    height: 19px;
`;
export const Info = styled.div`
    width: 78%;
    padding: 30px;
`;
export const Title = styled.div`
    font-family: 'Roboto';
    font-style: normal;
    font-weight: 500;
    font-size: 24px;
    line-height: 36px;
    letter-spacing: -0.035em;
`;
export const Text = styled.div`
    margin-top: 8px;
    font-family: 'Roboto';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 18px;
    letter-spacing: 0.02em;F
`;
