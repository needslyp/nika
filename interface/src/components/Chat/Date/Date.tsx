import { useLanguage } from '@hooks/useLanguage';
import styled from 'styled-components';
interface IProps {
    date: string;
}
const Wrapper = styled.div`
    width: 140px;
    margin: auto;
    margin-top: 8px;
    margin-bottom: 16px;
    padding: 6px 10px;
    background: #8fc1cf;
    border-radius: 10px;
    color: black;
    font-weight: 400;
    font-size: 14px;
    line-height: 16px;
`;
const DateInfo = styled.div`
    align-items: center;
    text-align: center;
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
    ru: {
        1: 'Январь',
        2: 'Февраль',
        3: 'Март',
        4: 'Апрель',
        5: 'Май',
        6: 'Июнь',
        7: 'Июль',
        8: 'Август',
        9: 'Сентябрь',
        10: 'Октябрь',
        11: 'Ноябрь',
        12: 'Декабрь',
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
