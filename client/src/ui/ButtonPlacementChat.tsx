import * as React from 'react';
import { AudioOutlined, BorderOutlined, SendOutlined } from '@ant-design/icons';
import { Button } from 'antd';
import {Simulate} from "react-dom/test-utils";
import input = Simulate.input;

export interface ButtonPlacementChatProps {
    inputRef?: any;
    inputValue?: string;
    onChange?: (e: any) => void;
    enterMessage?: (e: any) => void;
    sendInputText?: (e: any) => void;
    widgetAudioButton?: string;
    startRecording?: (e: any) => void;
    outlinedType?: string;
    className?: string;
}


function InputWidgetPlacement(props: ButtonPlacementChatProps): React.ReactElement {
    return (
        <input
            ref={props.inputRef}
            value={props.inputValue}
            id="userMessageInput"
            className={props.className}
            type="text"
            placeholder="Введите свое сообщение..."
            onChange={props.onChange}
            onKeyDown={props.enterMessage}
        />
    );

}

function TextButton({ sendInputText }: ButtonPlacementChatProps): React.ReactElement {
    return (
        <Button
            className="recording-button-first"
            icon={<SendOutlined className={'sendOutlinedIcon'} />}
            onClick={sendInputText}
        />
    );
}

export function ButtonPlacementChat(props: ButtonPlacementChatProps): React.ReactElement {
    const { sendInputText, startRecording, widgetAudioButton, outlinedType, ...propsForWidgetPlacement } = props;
    const outlinedButtonIcon =
        outlinedType == 'AudioOutlined' ? (
            <AudioOutlined className={'audioOutlined'} />
        ) : (
            <BorderOutlined className={'borderOutlined'} />
        );

    return (
        <div className="button-placement">
            <InputWidgetPlacement {...propsForWidgetPlacement}/>
            <TextButton sendInputText={sendInputText} />
            <Button
                className={widgetAudioButton}
                name="start"
                value="START"
                shape="circle"
                onClick={startRecording}
                icon={outlinedButtonIcon}
            />
        </div>
    );
}
