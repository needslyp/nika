import { useRef } from 'react';
import styled from 'styled-components';
import { ReactComponent as ArrowUp } from '@assets/arrowUp.svg';
import { useBooleanState } from '@hooks/useBooleanState';
import { useClickOutside, useDispatch, useWindowSize } from '@hooks';
import { commonSlice } from '@store/commonSlice';
import { useLanguage } from '@hooks/useLanguage';

const Wrapper = styled.div<{ isRotate: boolean }>`
    position: relative;
    cursor: pointer;
`;
const Header = styled.div`
    display: flex;
    align-items: center;
    gap: 10px;
    @media (max-width: 768px) {
        gap: 6px;
    } ;
`;
const Text = styled.div`
    font-weight: 500;
    font-size: 30px;
    line-height: 35px;
    color: #ffffff;
    @media (max-width: 768px) {
        line-height: 21px;
        font-size: 18px;
    } ;
`;
const Item = styled.div`
    padding: 5px;
    text-align: center;
    font-size: 26px;
    line-height: 30px;
    color: #000000;
    &:hover {
        border-radius: 4px;
        background-color: #e4e0dd;
    }
    &:hover::before {
        border-bottom: 6px solid #e4e0dd;
    }
    @media (max-width: 768px) {
        padding: 2px;
        line-height: 21px;
        font-size: 18px;
    }
`;
const Popup = styled(Item)`
    position: absolute;
    bottom: -7px;
    transform: translate3d(0, 100%, 0);
    left: -3px;
    width: 100%;
    background: #ffffff;
    border-radius: 4px;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.37);
    z-index: 3;
    &::before {
        content: '';
        position: absolute;
        left: 6px;
        top: 0;
        transform: translate3d(0, -100%, 0);
        width: 0;
        height: 0;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-bottom: 6px solid white;
    }
    &:hover::before {
        border-bottom: 6px solid #e4e0dd;
    }
    @media (max-width: 768px) {
        left: -7px;
        bottom: -3px;
        font-size: 18px;
    } ;
`;
const WrapperArrowUp = styled.div<{ isRotate: boolean }>`
    width: 16px;
    height: 9px;
    transition: transform ease 0.3s;
    transform: rotate(${({ isRotate: shouldRotate }) => (shouldRotate ? 0 : 180)}deg);
    @media (max-width: 768px) {
        width: 8px;
        height: 4px;
    }
`;

const languageMap = {
    en: 'English',
    ru: 'Русский',
};
const languageMapMobile = {
    en: 'En',
    ru: 'Ru',
};
const languages = ['en', 'ru'];

export const Language = () => {
    const [opened, close, toggle] = useBooleanState(false);

    const dispatch = useDispatch();
    const hookLanguage = useLanguage();

    const popupRef = useRef<HTMLDivElement>(null);
    const headerRef = useRef<HTMLDivElement>(null);

    useClickOutside([popupRef, headerRef], close);

    const setLanguage = (lang: string) => () => {
        dispatch(commonSlice.actions.setLanguage(lang));
        close();
    };

    const width = useWindowSize() > 768;
    return (
        <Wrapper isRotate={true}>
            <Header onClick={toggle} ref={headerRef}>
                <WrapperArrowUp isRotate={opened}>
                    <ArrowUp />
                </WrapperArrowUp>
                <Text>{width ? languageMap[hookLanguage] : languageMapMobile[hookLanguage]}</Text>
            </Header>
            {opened && (
                <Popup ref={popupRef}>
                    {languages
                        .filter((lang) => lang !== hookLanguage)
                        .map((lang) => (
                            <Item key={lang} onClick={setLanguage(lang)}>
                                {width ? languageMap[lang] : languageMapMobile[lang]}
                            </Item>
                        ))}
                </Popup>
            )}
        </Wrapper>
    );
};
