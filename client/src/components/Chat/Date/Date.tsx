import { useLanguage } from '@hooks/useLanguage';
import styled from 'styled-components';
interface IProps {
    date: string;
}
const Wrapper = styled.div`
    width: 105px;
    margin: auto;
    margin-top: 8px;
    margin-bottom: 16px;
    padding: 2px 10px;
    background: #daeddc;
    border-radius: 3px;
    color: #707070;
    font-weight: 400;
    font-size: 14px;
    line-height: 16px;
    @media (max-width: 768px) {
        width: 91px;
        padding: 2px 9px;
        font-size: 12px;
        line-height: 14px;
    }
`;
const DateInfo = styled.div`
    align-items: center;
`;

const months = {
    en: {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'Mai',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December',
    },
    de: {
        1: 'Januar',
        2: 'Februar',
        3: 'Marsch',
        4: 'April',
        5: 'Kann',
        6: 'Juni',
        7: 'Juli',
        8: 'August',
        9: 'September',
        10: 'Oktober',
        11: 'November',
        12: 'Dezember',
    },
};

export const Date = ({ date }: IProps) => {
    const hookLanguage = useLanguage();
    const [year, month, day] = date.toString().split('.');
    const currentMonth = months[hookLanguage];

    return (
        <>
            <Wrapper>
                <DateInfo>{`${currentMonth[Number(month)]} ${day} ${year}`}</DateInfo>
            </Wrapper>
        </>
    );
};
