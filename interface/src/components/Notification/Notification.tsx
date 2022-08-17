import { PropsWithChildren, ReactNode, useState } from 'react';
import { useLanguage } from '@hooks/useLanguage';
import { ReactComponent as CloseIcon } from '@assets/notification/errorClose-icon.svg';
import { ReactComponent as ArrowIcon } from '@assets/notification/errorArrowMoreInformation.svg';
import { ReactComponent as ErrorImageOrange } from '@assets/notification/errorImageOrange.svg';
import { ReactComponent as ErrorImageRed } from '@assets/notification/errorImageRed.svg';
import { ReactComponent as ErrorBasic } from '@assets/notification/errorBasic.svg';
import { ReactComponent as WarningBasic } from '@assets/notification/warningBasic.svg';
import {
    ButtonMoreInformation,
    ButtonMoreInformationText,
    Button,
    CloseWrapper,
    Icon,
    Image,
    Info,
    MoreInformationText,
    Title,
    Wrapper,
    WrapperImage,
    Text,
    WrapperErrorArrowIcon,
    WrapperIcon,
    WrapperSize,
} from './styled';

const defaultIcons = {
    error: <ErrorBasic />,
    warn: <WarningBasic />,
} as const;

const textMoreInfo = {
    en: 'more information',
    ru: 'Больше информации',
};

export interface IProps {
    title?: string;
    text?: string;
    additionalText?: string;
    icon?: ReactNode;
    type?: 'warn' | 'error';
    textButton?: string;
    onClose?: () => void;
    onButtonClick?: () => void;
}

export const Notification = ({
    title,
    text,
    type = 'warn',
    icon = defaultIcons[type],
    onButtonClick,
    onClose,
    textButton,
    additionalText,
}: PropsWithChildren<IProps>) => {
    const [showTextError, setShowTextError] = useState(false);

    const onMoreInfoClick = () => setShowTextError((prev) => !prev);
    const hookLanguage = useLanguage();

    return (
        <Wrapper typeColor={type}>
            <WrapperIcon>
                <Icon>{icon}</Icon>
            </WrapperIcon>
            <WrapperImage>
                <Image>
                    {type === 'error' && <ErrorImageRed />}
                    {type === 'warn' && <ErrorImageOrange />}
                </Image>
            </WrapperImage>
            <Info>
                <Title>{title}</Title>
                <Text>
                    {text}{' '}
                    {additionalText && (
                        <ButtonMoreInformation onClick={onMoreInfoClick}>
                            <ButtonMoreInformationText>{textMoreInfo[hookLanguage]}</ButtonMoreInformationText>
                            <WrapperErrorArrowIcon flip={!showTextError}>
                                <ArrowIcon />
                            </WrapperErrorArrowIcon>
                        </ButtonMoreInformation>
                    )}
                </Text>
                {textButton && <Button onClick={onButtonClick}>{textButton}</Button>}

                {showTextError && <MoreInformationText>{additionalText}</MoreInformationText>}
            </Info>
            <CloseWrapper onClick={onClose}>
                <WrapperSize>
                    <CloseIcon />
                </WrapperSize>
            </CloseWrapper>
        </Wrapper>
    );
};
