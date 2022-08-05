import * as React from 'react';
import { connect } from 'react-redux';

export class AboutImpl extends React.Component {
    render() {
        return (
            <div className="about-page-container">
                <div className="about-page">
                    <h1 className="about-page-text">
                        Обучающая диалоговая экспертная система IDESA, разработанный на основе технологии{' '}
                        <a href="http://ims.ostis.net/" className="text">
                            OSTIS
                        </a>{' '}
                        . Обучающая диалоговая экспертная ostis-система IDESA полностью заменяет участие Обучающей
                        диалоговой экспертной системы ЭКО в образовательном процессе по обучению студентов
                        специальностей Белорусского государственного университета информатики и радиоэлектроники
                        интеллектуальным экспертным системам. Новый вариант реализации системы такого класса позволяет
                        расширить круг решаемых задач, устраняет недостатки ранее использованного своего аналога и
                        упрощает и автоматизирует процесс обучения студентов специальностей Белорусского
                        государственного университета информатики и радиоэлектроники в контексте дисциплин, в которых
                        изучаются интеллектуальные экспертные системы.
                    </h1>
                    <h1 className="about-page-text">
                        Разработано{' '}
                        <a href="https://sem.systems/" className="text">
                            Intelligent Semantic Systems LLC
                        </a>
                        , Все права защищены.{' '}
                    </h1>
                </div>
            </div>
        );
    }
}

export const About = connect()(AboutImpl);
