import * as React from 'react';
import { connect } from 'react-redux';
import '../../assets/main.css';

class TipsImpl extends React.Component<any, any> {
    constructor(props) {
        super(props);
        this.state = {
            tips: [{ text: 'Привет!' }],
        };
    }

    render() {
        return (
            <div className="prompt">
                {this.state.tips.map((tip) => (
                    <div className="prom-1" key={tip.text} >
                        <p className="prompt-text">{tip.text}</p>
                    </div>
                ))}
            </div>
        );
    }
}

const mapStateToProps = (state) => ({ chat: state.ui.chat });

export const Prompt = connect(mapStateToProps)(TipsImpl);
